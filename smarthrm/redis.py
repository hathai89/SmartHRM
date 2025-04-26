import redis
from django.conf import settings

# Kết nối Redis
redis_instance = redis.StrictRedis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=getattr(settings, 'REDIS_DB', 1),
    decode_responses=True
)

def get_redis():
    """
    Trả về instance Redis
    """
    return redis_instance
