from redis import Redis
client = Redis(host="redis", port=6379, decode_responses=True)
