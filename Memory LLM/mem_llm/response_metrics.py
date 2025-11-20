"""
Response Metrics Module
=======================

Tracks and analyzes LLM response quality metrics including:
- Response latency
- Confidence scoring
- Knowledge base usage
- Source tracking
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ChatResponse:
    """
    Comprehensive response object with quality metrics

    Attributes:
        text: The actual response text
        confidence: Confidence score 0.0-1.0 (higher = more confident)
        source: Response source ("knowledge_base", "model", "tool", "hybrid")
        latency: Response time in milliseconds
        timestamp: When the response was generated
        kb_results_count: Number of KB results used (0 if none)
        metadata: Additional context (model name, temperature, etc.)
    """

    text: str
    confidence: float
    source: str
    latency: float
    timestamp: datetime
    kb_results_count: int = 0
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate metrics after initialization"""
        # Ensure confidence is in valid range
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")

        # Validate source
        valid_sources = ["knowledge_base", "model", "tool", "hybrid"]
        if self.source not in valid_sources:
            raise ValueError(f"Source must be one of {valid_sources}, got {self.source}")

        # Ensure latency is positive
        if self.latency < 0:
            raise ValueError(f"Latency cannot be negative, got {self.latency}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatResponse":
        """Create ChatResponse from dictionary"""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

    def get_quality_label(self) -> str:
        """Get human-readable quality label"""
        if self.confidence >= 0.90:
            return "Excellent"
        elif self.confidence >= 0.80:
            return "High"
        elif self.confidence >= 0.65:
            return "Medium"
        elif self.confidence >= 0.50:
            return "Low"
        else:
            return "Very Low"

    def is_fast(self, threshold_ms: float = 1000.0) -> bool:
        """Check if response was fast (< threshold)"""
        return self.latency < threshold_ms

    def __str__(self) -> str:
        """Human-readable string representation"""
        return (
            f"ChatResponse(text_length={len(self.text)}, "
            f"confidence={self.confidence:.2f}, "
            f"source={self.source}, "
            f"latency={self.latency:.0f}ms, "
            f"quality={self.get_quality_label()})"
        )


class ResponseMetricsAnalyzer:
    """Analyzes and aggregates response metrics over time"""

    def __init__(self):
        self.metrics_history: List[ChatResponse] = []

    def add_metric(self, response: ChatResponse) -> None:
        """Add a response metric to history"""
        self.metrics_history.append(response)

    def get_average_latency(self, last_n: Optional[int] = None) -> float:
        """Calculate average latency for last N responses"""
        metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history
        if not metrics:
            return 0.0
        return sum(m.latency for m in metrics) / len(metrics)

    def get_average_confidence(self, last_n: Optional[int] = None) -> float:
        """Calculate average confidence for last N responses"""
        metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history
        if not metrics:
            return 0.0
        return sum(m.confidence for m in metrics) / len(metrics)

    def get_kb_usage_rate(self, last_n: Optional[int] = None) -> float:
        """Calculate knowledge base usage rate (0.0-1.0)"""
        metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history
        if not metrics:
            return 0.0
        kb_used = sum(1 for m in metrics if m.kb_results_count > 0)
        return kb_used / len(metrics)

    def get_source_distribution(self, last_n: Optional[int] = None) -> Dict[str, int]:
        """Get distribution of response sources"""
        metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history
        distribution = {}
        for metric in metrics:
            distribution[metric.source] = distribution.get(metric.source, 0) + 1
        return distribution

    def get_summary(self, last_n: Optional[int] = None) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history

        if not metrics:
            return {
                "total_responses": 0,
                "avg_latency_ms": 0.0,
                "avg_confidence": 0.0,
                "kb_usage_rate": 0.0,
                "source_distribution": {},
                "fast_response_rate": 0.0,
            }

        fast_responses = sum(1 for m in metrics if m.is_fast())

        return {
            "total_responses": len(metrics),
            "avg_latency_ms": round(self.get_average_latency(last_n), 2),
            "avg_confidence": round(self.get_average_confidence(last_n), 3),
            "kb_usage_rate": round(self.get_kb_usage_rate(last_n), 3),
            "source_distribution": self.get_source_distribution(last_n),
            "fast_response_rate": round(fast_responses / len(metrics), 3),
            "quality_distribution": self._get_quality_distribution(metrics),
        }

    def _get_quality_distribution(self, metrics: List[ChatResponse]) -> Dict[str, int]:
        """Get distribution of quality labels"""
        distribution = {}
        for metric in metrics:
            quality = metric.get_quality_label()
            distribution[quality] = distribution.get(quality, 0) + 1
        return distribution

    def clear_history(self) -> None:
        """Clear all metrics history"""
        self.metrics_history.clear()


def calculate_confidence(
    kb_results_count: int, temperature: float, used_memory: bool, response_length: int
) -> float:
    """
    Calculate confidence score based on multiple factors

    Args:
        kb_results_count: Number of KB results used
        temperature: Model temperature setting
        used_memory: Whether conversation memory was used
        response_length: Length of response in characters

    Returns:
        Confidence score between 0.0 and 1.0
    """
    base_confidence = 0.50

    # KB contribution (0-0.35)
    if kb_results_count > 0:
        kb_boost = min(0.35, 0.10 + (kb_results_count * 0.05))
        base_confidence += kb_boost

    # Memory contribution (0-0.10)
    if used_memory:
        base_confidence += 0.10

    # Temperature factor (lower temp = higher confidence)
    # Temperature usually 0.0-1.0, we give 0-0.15 boost
    temp_factor = (1.0 - min(temperature, 1.0)) * 0.15
    base_confidence += temp_factor

    # Response length factor (very short = lower confidence)
    # Penalize very short responses (< 20 chars)
    if response_length < 20:
        base_confidence *= 0.8
    elif response_length < 50:
        base_confidence *= 0.9

    # Ensure confidence stays in valid range
    return max(0.0, min(1.0, base_confidence))
