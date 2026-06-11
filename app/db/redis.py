import os
from functools import cache

from redis import Redis


@cache
def get_client():
    return Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=6379,
        decode_responses=True
    )
