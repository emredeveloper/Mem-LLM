"""
Tool Workspace Manager (v2.1.3+)
=================================

Manages file artifacts created by tools.
Provides cleanup and organization for tool-generated files.

Author: Cihat Emre Karatas
Version: 2.1.3
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class ToolWorkspace:
    """
    Manages workspace for tool-generated files.

    Features:
    - Isolated workspace directory
    - Automatic cleanup
    - File organization by date/user
    - Safe file operations
    """

    def __init__(self, base_dir: Optional[str] = None, auto_cleanup: bool = False):
        """
        Initialize tool workspace.

        Args:
            base_dir: Base directory for workspace (default: ./tool_workspace)
            auto_cleanup: Auto-delete files after session (default: False)
        """
        self.base_dir = Path(base_dir) if base_dir else Path("tool_workspace")
        self.auto_cleanup = auto_cleanup
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create workspace directory
        self.base_dir.mkdir(exist_ok=True)

        # Session directory
        self.session_dir = self.base_dir / self.current_session
        if not auto_cleanup:
            self.session_dir.mkdir(exist_ok=True)

        logger.info(f"Tool workspace initialized: {self.base_dir.absolute()}")

    def _validate_user_id(self, user_id: str) -> str:
        """Validate user_id to avoid path traversal."""
        if not user_id or not user_id.strip():
            raise ValueError("user_id cannot be empty")

        candidate = Path(user_id.strip())

        if candidate.is_absolute() or candidate.drive:
            raise ValueError("user_id must be a relative identifier")

        if len(candidate.parts) != 1 or candidate.parts[0] in (".", ".."):
            raise ValueError("user_id must not contain path separators")

        return candidate.parts[0]

    def _validate_relative_path(self, path_value: str, field_name: str = "path") -> Path:
        """Validate a relative path fragment to keep operations inside workspace."""
        if not path_value or not path_value.strip():
            raise ValueError(f"{field_name} cannot be empty")

        candidate = Path(path_value.strip())

        if candidate.is_absolute() or candidate.drive:
            raise ValueError(f"{field_name} must be a relative path")

        if any(part in (".", "..") for part in candidate.parts):
            raise ValueError(f"{field_name} must not contain '.' or '..'")

        return candidate

    def _ensure_within(self, base_dir: Path, candidate_path: Path) -> Path:
        """Resolve and verify candidate path stays inside base_dir."""
        resolved_base = base_dir.resolve()
        resolved_candidate = candidate_path.resolve()

        try:
            resolved_candidate.relative_to(resolved_base)
        except ValueError as exc:
            raise ValueError("Path escapes workspace boundaries") from exc

        return resolved_candidate

    def _get_target_dir(self, user_id: Optional[str] = None) -> Path:
        """Get base directory for current operation."""
        if user_id and not self.auto_cleanup:
            safe_user_id = self._validate_user_id(user_id)
            user_dir = self.session_dir / safe_user_id
            user_dir.mkdir(exist_ok=True)
            return user_dir

        if self.auto_cleanup:
            return self.base_dir

        return self.session_dir

    def get_file_path(self, filename: str, user_id: Optional[str] = None) -> Path:
        """
        Get full path for a tool-generated file.

        Args:
            filename: Name of the file
            user_id: Optional user ID for organization

        Returns:
            Full path in workspace
        """
        target_dir = self._get_target_dir(user_id)
        safe_relative = self._validate_relative_path(filename, field_name="filename")
        candidate = target_dir / safe_relative
        return self._ensure_within(target_dir, candidate)

    def list_files(self, user_id: Optional[str] = None, pattern: str = "*") -> List[Path]:
        """
        List files in workspace.

        Args:
            user_id: Filter by user ID
            pattern: File pattern (e.g., "*.txt")

        Returns:
            List of file paths
        """
        if pattern and ".." in pattern:
            raise ValueError("Pattern must not contain '..'")

        search_dir = self._get_target_dir(user_id)

        if not search_dir.exists():
            return []

        return list(search_dir.glob(pattern or "*"))

    def cleanup(self, user_id: Optional[str] = None, older_than_days: Optional[int] = None):
        """
        Clean up workspace files.

        Args:
            user_id: Clean only this user's files (None = all)
            older_than_days: Remove files older than N days (None = all)
        """
        if user_id:
            # Clean specific user directory
            safe_user_id = self._validate_user_id(user_id)
            user_dir = self.session_dir / safe_user_id
            user_dir = self._ensure_within(self.session_dir, user_dir)
            if user_dir.exists():
                shutil.rmtree(user_dir)
                logger.info(f"Workspace cleaned for user: {safe_user_id}")
        elif older_than_days:
            # Clean old session directories
            cutoff = datetime.now().timestamp() - (older_than_days * 86400)
            for session_dir in self.base_dir.iterdir():
                if session_dir.is_dir() and session_dir.stat().st_mtime < cutoff:
                    shutil.rmtree(session_dir)
                    logger.info(f"Removed old session: {session_dir.name}")
        else:
            # Clean everything in workspace
            for item in self.base_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            logger.info("Workspace cleaned")

    def get_stats(self) -> dict:
        """
        Get workspace statistics.

        Returns:
            Dict with file counts and sizes
        """
        total_files = 0
        total_size = 0

        for file_path in self.base_dir.rglob("*"):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size

        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "workspace_dir": str(self.base_dir.absolute()),
            "current_session": self.current_session,
        }

    def __del__(self):
        """Cleanup on deletion if auto_cleanup is enabled"""
        if self.auto_cleanup and self.base_dir.exists():
            try:
                for item in self.base_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                logger.info("Auto-cleanup completed")
            except Exception as e:
                logger.error(f"Auto-cleanup error: {e}")


# Global workspace instance
_default_workspace: Optional[ToolWorkspace] = None


def get_workspace(base_dir: Optional[str] = None, auto_cleanup: bool = False) -> ToolWorkspace:
    """
    Get or create the default tool workspace.

    Args:
        base_dir: Base directory (only used on first call)
        auto_cleanup: Auto-delete files (only used on first call)

    Returns:
        ToolWorkspace instance
    """
    global _default_workspace
    if _default_workspace is None:
        _default_workspace = ToolWorkspace(base_dir, auto_cleanup)
    return _default_workspace


def set_workspace(workspace: ToolWorkspace):
    """Set the global workspace instance"""
    global _default_workspace
    _default_workspace = workspace
