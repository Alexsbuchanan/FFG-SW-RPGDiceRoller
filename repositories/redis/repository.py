import asyncio

from __init__ import REDIS_URI, REDIS_USERNAME, REDIS_PASSWORD

from redis import asyncio as aioredis




async def main():
    redis = await aioredis.from_url(REDIS_URI)
    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    print(value)


if __name__ == "__main__":
    asyncio.run(main())