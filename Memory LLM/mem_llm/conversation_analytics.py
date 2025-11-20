import csv
import io
import json
from collections import Counter
from datetime import datetime
from typing import Dict

from .analytics.topic_extractor import TopicExtractor


class ConversationAnalytics:
    """Analyze conversation patterns and provide insights"""

    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.topic_extractor = TopicExtractor()

    def get_conversation_stats(self, user_id: str) -> Dict:
        """
        Get comprehensive conversation statistics

        Returns:
            {
                "total_messages": int,
                "user_messages": int,
                "assistant_messages": int,
                "avg_message_length": float,
                "total_conversations": int,
                "first_interaction": str,
                "last_interaction": str,
                "most_active_day": str,
            }
        """
        data = self.memory.load_memory(user_id)
        conversations = data.get("conversations", [])

        if not conversations:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "avg_message_length": 0.0,
                "total_conversations": 0,
                "first_interaction": None,
                "last_interaction": None,
                "most_active_day": None,
            }

        total_conversations = len(conversations)
        # Each interaction has 1 user message
        user_messages_count = total_conversations
        # Each interaction has 1 bot response
        assistant_messages_count = total_conversations
        total_messages = user_messages_count + assistant_messages_count

        total_length = 0
        days_counter = Counter()
        first_interaction = None
        last_interaction = None

        for conv in conversations:
            # Length calculation
            user_msg = conv.get("user_message", "")
            bot_msg = conv.get("bot_response", "")
            total_length += len(user_msg) + len(bot_msg)

            # Date tracking
            timestamp_str = conv.get("timestamp")
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str)
                    day_name = dt.strftime("%A")
                    days_counter[day_name] += 1

                    if first_interaction is None or dt < first_interaction:
                        first_interaction = dt
                    if last_interaction is None or dt > last_interaction:
                        last_interaction = dt
                except (ValueError, TypeError):
                    pass

        avg_length = total_length / total_messages if total_messages > 0 else 0.0
        most_active_day = days_counter.most_common(1)[0][0] if days_counter else None

        return {
            "total_messages": total_messages,
            "user_messages": user_messages_count,
            "assistant_messages": assistant_messages_count,
            "avg_message_length": round(avg_length, 2),
            "total_conversations": total_conversations,
            "first_interaction": (first_interaction.isoformat() if first_interaction else None),
            "last_interaction": (last_interaction.isoformat() if last_interaction else None),
            "most_active_day": most_active_day,
        }

    def get_topic_distribution(self, user_id: str, top_n: int = 10) -> Dict[str, int]:
        """
        Extract and count topics from conversations
        """
        data = self.memory.load_memory(user_id)
        conversations = data.get("conversations", [])

        if not conversations:
            return {}

        messages = []
        for conv in conversations:
            messages.append(conv.get("user_message", ""))
            # Optionally include bot responses too

        return self.topic_extractor.extract_topics(messages, top_n)

    def get_engagement_metrics(self, user_id: str) -> Dict:
        """
        Calculate user engagement metrics

        Returns:
            {
                "engagement_score": float,  # 0-100
                "avg_session_length": float,  # minutes (estimated)
                "active_days": int,
                "interactions_per_active_day": float
            }
        """
        data = self.memory.load_memory(user_id)
        conversations = data.get("conversations", [])

        if not conversations:
            return {
                "engagement_score": 0.0,
                "avg_session_length": 0.0,
                "active_days": 0,
                "interactions_per_active_day": 0.0,
            }

        # Group by day
        interactions_by_day = {}
        for conv in conversations:
            timestamp_str = conv.get("timestamp")
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str)
                    date_key = dt.date().isoformat()
                    if date_key not in interactions_by_day:
                        interactions_by_day[date_key] = []
                    interactions_by_day[date_key].append(dt)
                except (ValueError, TypeError):
                    pass

        active_days = len(interactions_by_day)
        total_interactions = len(conversations)

        # Calculate session length (approximate)
        # If interactions are within 30 mins, consider same session
        total_session_minutes = 0
        total_sessions = 0

        for day, times in interactions_by_day.items():
            times.sort()
            if not times:
                continue

            current_session_start = times[0]
            current_session_end = times[0]
            total_sessions += 1

            for i in range(1, len(times)):
                diff = (times[i] - times[i - 1]).total_seconds() / 60
                if diff > 30:  # New session
                    session_duration = (
                        current_session_end - current_session_start
                    ).total_seconds() / 60
                    # Minimum 1 min
                    total_session_minutes += max(1, session_duration)

                    current_session_start = times[i]
                    current_session_end = times[i]
                    total_sessions += 1
                else:
                    current_session_end = times[i]

            # Add last session of the day
            session_duration = (current_session_end - current_session_start).total_seconds() / 60
            total_session_minutes += max(1, session_duration)

        avg_session_length = total_session_minutes / total_sessions if total_sessions > 0 else 0
        interactions_per_day = total_interactions / active_days if active_days > 0 else 0

        # Simple engagement score (0-100)
        # Factors: active days, frequency, session length
        # This is arbitrary but gives a relative metric
        score = min(
            100, (active_days * 2) + (interactions_per_day * 5) + (avg_session_length * 0.5)
        )

        return {
            "engagement_score": round(score, 1),
            "avg_session_length": round(avg_session_length, 1),
            "active_days": active_days,
            "interactions_per_active_day": round(interactions_per_day, 1),
        }

    def get_time_distribution(self, user_id: str) -> Dict[str, int]:
        """
        Get message distribution by hour of day

        Returns: {"00": 5, "01": 2, ..., "23": 10}
        """
        data = self.memory.load_memory(user_id)
        conversations = data.get("conversations", [])

        hours_counter = Counter()
        # Initialize all hours with 0
        for h in range(24):
            hours_counter[f"{h:02d}"] = 0

        for conv in conversations:
            timestamp_str = conv.get("timestamp")
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str)
                    hour_key = f"{dt.hour:02d}"
                    hours_counter[hour_key] += 1
                except (ValueError, TypeError):
                    pass

        return dict(sorted(hours_counter.items()))

    def export_report(self, user_id: str, format: str = "json") -> str:
        """
        Export analytics report

        Formats: json, csv, markdown
        """
        stats = self.get_conversation_stats(user_id)
        topics = self.get_topic_distribution(user_id)
        engagement = self.get_engagement_metrics(user_id)
        time_dist = self.get_time_distribution(user_id)

        report_data = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "statistics": stats,
            "topics": topics,
            "engagement": engagement,
            "time_distribution": time_dist,
        }

        if format.lower() == "json":
            return json.dumps(report_data, indent=2)

        elif format.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(["Category", "Metric", "Value"])

            # Stats
            for k, v in stats.items():
                writer.writerow(["Statistics", k, v])

            # Engagement
            for k, v in engagement.items():
                writer.writerow(["Engagement", k, v])

            # Topics
            for k, v in topics.items():
                writer.writerow(["Topic", k, v])

            return output.getvalue()

        elif format.lower() == "markdown":
            md = f"# Analytics Report for {user_id}\n\n"
            md += f"Generated at: {report_data['generated_at']}\n\n"

            md += "## General Statistics\n"
            for k, v in stats.items():
                md += f"- **{k.replace('_', ' ').title()}**: {v}\n"

            md += "\n## Engagement Metrics\n"
            for k, v in engagement.items():
                md += f"- **{k.replace('_', ' ').title()}**: {v}\n"

            md += "\n## Top Topics\n"
            for k, v in topics.items():
                md += f"- **{k}**: {v}\n"

            return md

        else:
            raise ValueError(f"Unsupported format: {format}")
