import os


# Ensure required database environment variables exist before any app imports
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_DB", "postgres")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("LOGGING_CONFIG", os.path.join(os.path.dirname(os.path.dirname(__file__)), "uvicorn_logging_conf_string.ini"))
