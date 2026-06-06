import redis
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_cache(key):
    data = r.get(key)
    return json.loads(data) if data else None

def set_cache(key, value):
    r.set(key, json.dumps(value), ex=3600)