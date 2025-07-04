from .crdt import RGACRDT
from .utils import log_operation, validate_operation
from .redis_pubsub import RedisPubSub


class Document:
    def __init__(self):
        self.crdt = RGACRDT(site_id=0)
        self.clients = set()
    
    def apply_operation(self, operation: dict) -> dict:
        self.crdt.apply_operation(operation)
    
    def get_state(self) -> dict:
        return {"text": self.crdt.get_text()}
    
    def reset(self):
        self.crdt = RGACRDT(site_id=0)
    
    def add_client(self, client_id: str):
        self.clients.add(client_id)
    
    def remove_client(self, client_id: str):
        self.clients.discard(client_id)
    
    def _broadcast_operation(self, operation: dict, exclude_client: str = None):
        redis_pubsub.publish(operation)
        for client in self.clients:
            if client != exclude_client:
                log_operation(operation, client)
    
    def _validate_operation(self, operation: dict) -> bool:
        return validate_operation(operation)