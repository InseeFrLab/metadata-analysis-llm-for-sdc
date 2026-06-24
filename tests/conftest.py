"""Make the repo root importable so `from core import ...` works under pytest."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
