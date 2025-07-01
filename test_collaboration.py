#!/usr/bin/env python3
"""
Test script to verify CRDT collaboration between multiple clients.
Run this to test your apply_operation implementation: python test_collaboration.py
"""

from app.crdt import RGACRDT

def test_collaboration():
    """Test collaboration between two clients."""
    print("Testing CRDT collaboration between two clients...")
    
    # Create two CRDT instances (simulating two clients)
    crdt1 = RGACRDT(site_id=1)
    crdt2 = RGACRDT(site_id=2)
    
    print(f"Initial state - Client 1: '{crdt1.get_text()}', Client 2: '{crdt2.get_text()}'")
    
    # Client 1 inserts "hello"
    print("\nClient 1 inserting 'hello'...")
    op1 = crdt1.insert(0, "h")
    op2 = crdt1.insert(1, "e")
    op3 = crdt1.insert(2, "l")
    op4 = crdt1.insert(3, "l")
    op5 = crdt1.insert(4, "o")
    
    print(f"Client 1 text after inserts: '{crdt1.get_text()}'")
    
    # Apply operations to client 2
    print("\nApplying operations to Client 2...")
    crdt2.apply_operation(op1)
    crdt2.apply_operation(op2)
    crdt2.apply_operation(op3)
    crdt2.apply_operation(op4)
    crdt2.apply_operation(op5)
    
    print(f"Client 2 text after applying operations: '{crdt2.get_text()}'")
    
    # Verify both clients have the same text
    if crdt1.get_text() == crdt2.get_text() == "hello":
        print("✅ Collaboration test PASSED! Both clients have 'hello'")
    else:
        print(f"❌ Collaboration test FAILED!")
        print(f"  Client 1: '{crdt1.get_text()}'")
        print(f"  Client 2: '{crdt2.get_text()}'")
    
    # Test delete collaboration
    print("\n" + "="*50)
    print("Testing delete collaboration...")
    
    # Client 2 deletes character at position 1 (should delete 'e')
    op6 = crdt2.delete(1)
    print(f"Client 2 deletes character at position 1: {op6}")
    print(f"Client 2 text after delete: '{crdt2.get_text()}'")
    
    # Apply delete operation to client 1
    crdt1.apply_operation(op6)
    print(f"Client 1 text after applying delete: '{crdt1.get_text()}'")
    
    # Verify both clients have the same text after delete
    if crdt1.get_text() == crdt2.get_text() == "hllo":
        print("✅ Delete collaboration test PASSED! Both clients have 'hllo'")
    else:
        print(f"❌ Delete collaboration test FAILED!")
        print(f"  Client 1: '{crdt1.get_text()}'")
        print(f"  Client 2: '{crdt2.get_text()}'")
    
    # Print character trees for both clients
    print("\n" + "="*50)
    print("Character tree comparison:")
    print("Client 1:")
    for char_id, char in crdt1.characters.items():
        print(f"  {char_id}: char='{char.char}', site_id={char.site_id}, timestamp={char.logical_timestamp}, deleted={char.is_deleted}")
    
    print("\nClient 2:")
    for char_id, char in crdt2.characters.items():
        print(f"  {char_id}: char='{char.char}', site_id={char.site_id}, timestamp={char.logical_timestamp}, deleted={char.is_deleted}")

if __name__ == "__main__":
    test_collaboration() 