"""
CRDT (Conflict-Free Replicated Data Type) Implementation
This module implements a Replicated Growable Array (RGA) for text sequences.

Key concepts to understand:
1. Each character needs a unique identifier (site_id + logical_timestamp + random_suffix)
2. Characters are stored in a tree structure where each character points to its parent
3. Insert operations place characters between existing ones
4. Delete operations mark characters as deleted (tombstone approach)
5. All operations must be commutative and associative

TODO: Implement the following classes and methods:

1. Character class:
   - __init__(self, char: str, site_id: int, logical_timestamp: int, parent_id: str = None)
   - Properties: char, site_id, logical_timestamp, parent_id, is_deleted, children

2. RGACRDT class:
   - __init__(self, site_id: int)
   - insert(self, position: int, char: str) -> dict
   - delete(self, position: int) -> dict
   - apply_operation(self, operation: dict)
   - get_text(self) -> str
   - _find_insertion_position(self, position: int) -> str
   - _generate_character_id(self, char: str) -> str
   - _add_character(self, char: Character)
   - _remove_character(self, char_id: str)

3. Helper functions:
   - compare_character_ids(id1: str, id2: str) -> int
   - generate_unique_id(site_id: int, logical_timestamp: int) -> str
"""

import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Character:
    """
    Represents a single character in the CRDT with its metadata.
    
    Attributes:
        char: The actual character
        site_id: Unique identifier for the site/client
        logical_timestamp: Logical timestamp for ordering
        parent_id: ID of the parent character in the tree
        is_deleted: Whether this character is marked as deleted
        children: List of child character IDs
    """
    char: str
    site_id: int
    logical_timestamp: int
    parent_id: Optional[str] = None
    is_deleted: bool = False
    children: List[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    @property
    def id(self) -> str:
        """Generate unique character ID."""
        return f"{self.site_id}:{self.logical_timestamp}:{uuid.uuid4().hex[:8]}"


class RGACRDT:
    """
    Replicated Growable Array CRDT implementation for text sequences.
    
    This CRDT ensures that concurrent edits from multiple clients
    converge to the same final state without conflicts.
    """
    
    def __init__(self, site_id: int):
        """
        Initialize the RGA CRDT.
        
        Args:
            site_id: Unique identifier for this site/client
        """
        self.site_id = site_id
        self.logical_timestamp = 0
        self.characters: Dict[str, Character] = {}
        self.root_id = "root"
        
        # Initialize with root character
        root_char = Character("", -1, -1)
        root_char.parent_id = None
        self.characters[self.root_id] = root_char
    
    def insert(self, position: int, char: str) -> dict:
        self.logical_timestamp += 1
        char_id = self._generate_character_id(char)
        parent_id = self._find_insertion_position(position)
        new_char = Character(char, self.site_id, self.logical_timestamp, parent_id)
        self.characters[char_id] = new_char
        self._add_character(new_char)
        return {
            "type": "insert",
            "char_id": char_id,
            "char": char,
            "parent_id": parent_id,
            "site_id": self.site_id,
            "logical_timestamp": self.logical_timestamp
        }
    
    def delete(self, position: int) -> dict:
        self.logical_timestamp += 1
        char_id = self._find_character_at_position(position)
        self.characters[char_id].is_deleted = True
        return {
            "type": "delete",
            "char_id": char_id,
            "site_id": self.site_id,
            "logical_timestamp": self.logical_timestamp
        }
    
    def apply_operation(self, operation: dict):
        if operation["type"] == "insert":
            char_id = operation["char_id"]
            new_char = Character(
                char=operation["char"],
                site_id=operation["site_id"],
                logical_timestamp=operation["logical_timestamp"],
                parent_id=operation["parent_id"]
            )
            self.characters[char_id] = new_char
            self._add_character(new_char)
        elif operation["type"] == "delete":
            char_id = operation["char_id"]
            if char_id in self.characters:
                self.characters[char_id].is_deleted = True
    
    def get_text(self) -> str:
        text = ""
        for char_id, char in self.characters.items():
            if char_id != self.root_id and not char.is_deleted:
                text += char.char
        return text
    
    def _find_insertion_position(self, position: int) -> str:
        return self.root_id
    
    def _generate_character_id(self, char: str) -> str:
        return f"{self.site_id}:{self.logical_timestamp}:{uuid.uuid4().hex[:8]}"
    
    def _add_character(self, char: Character):
        if char.parent_id and char.parent_id in self.characters:
            self.characters[char.parent_id].children.append(char.id)
    
    def _find_character_at_position(self, position: int) -> str:
        count = 0
        for char_id, char in self.characters.items():
            if char_id != self.root_id and not char.is_deleted:
                if count == position:
                    return char_id
                count += 1
        raise ValueError(f"No character found at position {position}")
    
    def _remove_character(self, char_id: str):
        if char_id in self.characters:
            self.characters[char_id].is_deleted = True


def compare_character_ids(id1: str, id2: str) -> int:
    """
    Compare two character IDs for ordering.
    
    Args:
        id1: First character ID
        id2: Second character ID
        
    Returns:
        -1 if id1 < id2, 0 if equal, 1 if id1 > id2
    """
    # TODO: Implement this method
    # 1. Parse site_id and logical_timestamp from IDs
    # 2. Compare site_id first, then logical_timestamp
    # 3. Use random suffix as tiebreaker
    pass


def generate_unique_id(site_id: int, logical_timestamp: int) -> str:
    """
    Generate a unique character ID.
    
    Args:
        site_id: Site identifier
        logical_timestamp: Logical timestamp
        
    Returns:
        Unique character ID string
    """
    # TODO: Implement this method
    # 1. Combine site_id, logical_timestamp, and random suffix
    # 2. Return formatted string
    pass 