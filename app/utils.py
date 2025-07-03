"""
Utility functions for the CRDT collaborative editor.

This module contains helper functions used across the application
for validation, serialization, and common operations.
"""

import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import time


def generate_client_id() -> str:
    """
    Generate a unique client ID.
    
    Returns:
        Unique client identifier string
    """
    return f"client_{uuid.uuid4().hex[:8]}"


def validate_operation(operation: Dict[str, Any]) -> bool:
    required_fields = {"type", "site_id", "logical_timestamp"}
    if not isinstance(operation, dict):
        return False
    if not required_fields.issubset(operation.keys()):
        return False
    if operation["type"] not in ("insert", "delete"):
        return False
    if operation["type"] == "insert":
        if not all(k in operation for k in ("char_id", "char", "parent_id")):
            return False
    if operation["type"] == "delete":
        if "char_id" not in operation:
            return False
    return True


def serialize_operation(operation: Dict[str, Any]) -> str:
    return json.dumps(operation)


def deserialize_operation(data: str) -> Optional[Dict[str, Any]]:
    """
    Deserialize an operation from JSON string.
    
    Args:
        data: JSON string to deserialize
        
    Returns:
        Operation dictionary or None if invalid
    """
    # TODO: Implement this function
    # 1. Parse JSON string
    # 2. Handle parsing errors
    # 3. Return operation dict or None
    try:
        return json.loads(data)
    except Exception as e:
        logging.error(f"Failed to deserialize operation: {e}")
        return None


def create_operation(operation_type: str, **kwargs) -> Dict[str, Any]:
    op = {
        "type": operation_type,
        "site_id": kwargs.get("site_id", 0),
        "logical_timestamp": kwargs.get("logical_timestamp", get_timestamp()),
    }
    op.update(kwargs)
    return op


def get_timestamp() -> int:
    return int(time.time() * 1000)


def log_operation(operation: Dict[str, Any], client_id: str):
    """
    Log an operation for debugging.
    
    Args:
        operation: Operation to log
        client_id: ID of the client performing the operation
    """
    # TODO: Implement this function
    # 1. Format log message
    # 2. Include timestamp and client info
    # 3. Write to log
    ts = get_timestamp()
    logging.info(f"[{ts}] Client {client_id}: {operation}")


def calculate_position_offset(text: str, position: int) -> int:
    position = max(0, position)
    position = min(position, len(text))
    return position