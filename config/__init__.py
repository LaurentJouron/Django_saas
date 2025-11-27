"""
Django project initialization.

Handles environment variable loading with priority:
1. .env (base configuration)
2. .env.{DJANGO_ENV} (environment-specific: development/production)
3. .env.local (local overrides, git-ignored)
"""

from pathlib import Path

from environ import Env

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = Env()

# Define environment files with priority order (first = lowest priority)
env_files = [
    BASE_DIR / ".env",  # Base configuration (committed to git)
    BASE_DIR
    / f".env.{env('DJANGO_ENV', default='development')}",  # Environment-specific
    BASE_DIR / ".env.local",  # Local overrides (git-ignored, highest priority)
]

# Load environment files in order
for env_file in env_files:
    if env_file.exists():
        env.read_env(env_file, overwrite=True)
