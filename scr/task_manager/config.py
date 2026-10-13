"""Application configuration."""

from pathlib import Path

# Resolve data storage relative to the project root, not the shell's cwd.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "tasks.json"
