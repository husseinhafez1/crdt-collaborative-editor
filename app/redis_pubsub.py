import asyncio
import json
import threading
import redis


class RedisPubSub:
    def __init__(self, document, channel="crdt-ops", redis_url="redis://localhost:6379/0"):
        self.document = document
        self.channel = channel
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channel)
        self.loop = asyncio.get_event_loop()
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def publish(self, operation):
        self.redis.publish(self.channel, json.dumps(operation))

    def listen(self):
        for message in self.pubsub.listen():
            if message["type"] == "message":
                op = json.loads(message["data"])
                self.loop.call_soon_threadsafe(self.document.apply_operation, op)