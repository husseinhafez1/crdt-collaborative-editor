import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import functools
from app.metrics import crdt_operations_total, active_sessions, crdt_conflicts_resolved

@dataclass
class Character:
    char: str
    site_id: int
    logical_timestamp: int
    parent_id: Optional[str] = None
    is_deleted: bool = False
    children: List[str] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.id is None:
            self.id = f"{self.site_id}:{self.logical_timestamp}:{uuid.uuid4().hex[:8]}"


class RGACRDT:
    def __init__(self, site_id: int):
        self.site_id = site_id
        self.logical_timestamp = 0
        self.characters: Dict[str, Character] = {}
        self.root_id = "root"
        root_char = Character("", -1, -1)
        root_char.parent_id = None
        self.characters[self.root_id] = root_char
    
    def insert(self, position: int, char: str) -> dict:
        self.logical_timestamp += 1
        char_id = self._generate_character_id(char)
        parent_id = self._find_insertion_position(position)
        new_char = Character(char, self.site_id, self.logical_timestamp, parent_id, id=char_id)
        self.characters[char_id] = new_char
        self._add_character(new_char)
        crdt_operations_total.labels(operation_type="insert").inc()
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
        crdt_operations_total.labels(operation_type="delete").inc()
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
                parent_id=operation["parent_id"],
                id=char_id
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
            siblings = self.characters[char.parent_id].children
            if char.id not in siblings:
                siblings.append(char.id)
                siblings.sort(key=functools.cmp_to_key(compare_character_ids))
    
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

    def _traverse(self, parent_id):
        chars = []
        children = self.characters[parent_id].children
        print(f"Traversing children of {parent_id}: {children}")
        children_sorted = sorted(children, key=functools.cmp_to_key(compare_character_ids))
        for cid in children_sorted:
            if cid not in self.characters:
                print(f"Character {cid} not found in characters")
            char = self.characters[cid]
            if not char.is_deleted:
                chars.append(char.char)
            chars.extend(self._traverse(cid))
        return chars

    def get_text(self):
        return "".join(self._traverse(self.root_id))
    
    def _add_character(self, char: Character):
        if char.parent_id and char.parent_id in self.characters:
            siblings = self.characters[char.parent_id].children
            if char.id not in siblings:
                siblings.append(char.id)
                siblings.sort(key=functools.cmp_to_key(compare_character_ids))


def compare_character_ids(id1: str, id2: str) -> int:
    site1, ts1, rand1 = id1.split(":")
    site2, ts2, rand2 = id2.split(":")
    if int(ts1) < int(ts2):
        return -1
    elif int(ts1) > int(ts2):
        return 1
    if int(site1) < int(site2):
        return -1
    elif int(site1) > int(site2):
        return 1
    if rand1 < rand2:
        return -1
    elif rand1 > rand2:
        return 1
    return 0

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