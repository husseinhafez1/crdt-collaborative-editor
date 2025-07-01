#!/usr/bin/env python3
"""
Simple test script to verify basic CRDT functionality.
Run this to test your implementation: python test_basic.py
"""

from app.crdt import RGACRDT

def test_basic_insert():
    """Test basic insert functionality."""
    print("Testing basic CRDT insert...")
    
    # Create a CRDT instance
    crdt = RGACRDT(site_id=1)
    
    # Test initial state
    print(f"Initial text: '{crdt.get_text()}'")
    
    # Insert some characters
    op1 = crdt.insert(0, "h")
    print(f"Insert 'h': {op1}")
    print(f"Text after insert: '{crdt.get_text()}'")
    
    op2 = crdt.insert(1, "e")
    print(f"Insert 'e': {op2}")
    print(f"Text after insert: '{crdt.get_text()}'")
    
    op3 = crdt.insert(2, "l")
    print(f"Insert 'l': {op3}")
    print(f"Text after insert: '{crdt.get_text()}'")
    
    # Check final state
    final_text = crdt.get_text()
    print(f"Final text: '{final_text}'")
    
    # Verify it worked
    if final_text == "hel":
        print("✅ Basic insert test PASSED!")
    else:
        print(f"❌ Basic insert test FAILED! Expected 'hel', got '{final_text}'")
    
    # Print character tree structure
    print("\nCharacter tree:")
    for char_id, char in crdt.characters.items():
        print(f"  {char_id}: char='{char.char}', parent={char.parent_id}, children={char.children}, deleted={char.is_deleted}")
    
    # Test delete functionality
    print("\n" + "="*50)
    print("Testing delete functionality...")
    
    # Delete character at position 1 (should delete 'e')
    op4 = crdt.delete(1)
    print(f"Delete at position 1: {op4}")
    print(f"Text after delete: '{crdt.get_text()}'")
    
    # Verify delete worked
    if crdt.get_text() == "hl":
        print("✅ Delete test PASSED!")
    else:
        print(f"❌ Delete test FAILED! Expected 'hl', got '{crdt.get_text()}'")
    
    # Print character tree after delete
    print("\nCharacter tree after delete:")
    for char_id, char in crdt.characters.items():
        print(f"  {char_id}: char='{char.char}', parent={char.parent_id}, children={char.children}, deleted={char.is_deleted}")

if __name__ == "__main__":
    test_basic_insert() 