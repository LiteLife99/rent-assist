import os

if os.getenv("USE_FASTSTREAM_DEPENDS") == "true":
    from faststream import Depends
else:
    from fastapi import Depends

__all__ = ["Depends"]
