"""
Merkle Tree - Cryptographic tree structure for tamper-evident log anchoring.

Provides daily Merkle root generation and inclusion proof verification
for anchoring event logs on-chain.
"""

import hashlib
from typing import List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class MerkleProof:
    """Merkle inclusion proof for an event."""
    leaf_hash: str
    siblings: List[str]
    root: str
    path: List[bool]  # True = right, False = left
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'leaf_hash': self.leaf_hash,
            'siblings': self.siblings,
            'root': self.root,
            'path': self.path
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class MerkleTree:
    """
    Merkle tree implementation for event log anchoring.
    
    Features:
    - Binary tree construction from leaf hashes
    - Root hash generation
    - Inclusion proof generation
    - Proof verification
    """
    
    def __init__(self, leaf_hashes: List[str]):
        """
        Initialize Merkle tree from leaf hashes.
        
        Args:
            leaf_hashes: List of SHA-256 hashes (event hashes)
        """
        if not leaf_hashes:
            raise ValueError("Cannot create Merkle tree from empty list")
        
        self.leaves = leaf_hashes.copy()
        self.tree = self._build_tree(leaf_hashes)
        self.root = self.tree[0][0] if self.tree else None
    
    @staticmethod
    def hash_pair(left: str, right: str) -> str:
        """
        Hash a pair of nodes.
        
        Args:
            left: Left node hash
            right: Right node hash
            
        Returns:
            SHA-256 hash of concatenated nodes
        """
        combined = left + right
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def _build_tree(self, hashes: List[str]) -> List[List[str]]:
        """
        Build the Merkle tree from leaf hashes.
        
        Args:
            hashes: List of leaf hashes
            
        Returns:
            List of tree levels (bottom to top)
        """
        if not hashes:
            return []
        
        tree = [hashes.copy()]
        
        while len(tree[-1]) > 1:
            current_level = tree[-1]
            next_level = []
            
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # If odd number of nodes, duplicate the last one
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = self.hash_pair(left, right)
                next_level.append(parent)
            
            tree.append(next_level)
        
        return tree
    
    def get_root(self) -> str:
        """
        Get the Merkle root hash.
        
        Returns:
            Root hash (hex string)
        """
        return self.root
    
    def get_proof(self, leaf_hash: str) -> Optional[MerkleProof]:
        """
        Generate inclusion proof for a leaf.
        
        Args:
            leaf_hash: Hash of the leaf to prove
            
        Returns:
            MerkleProof if leaf exists, None otherwise
        """
        try:
            # Find leaf index
            leaf_index = self.leaves.index(leaf_hash)
        except ValueError:
            return None
        
        siblings = []
        path = []
        current_index = leaf_index
        
        # Traverse tree from bottom to top
        for level in self.tree[:-1]:  # Exclude root level
            # Determine sibling
            if current_index % 2 == 0:
                # Current node is left child
                sibling_index = current_index + 1
                path.append(True)  # Sibling is on the right
            else:
                # Current node is right child
                sibling_index = current_index - 1
                path.append(False)  # Sibling is on the left
            
            # Get sibling hash (duplicate if it doesn't exist)
            if sibling_index < len(level):
                siblings.append(level[sibling_index])
            else:
                siblings.append(level[current_index])
            
            # Move to parent index
            current_index = current_index // 2
        
        return MerkleProof(
            leaf_hash=leaf_hash,
            siblings=siblings,
            root=self.root,
            path=path
        )
    
    @staticmethod
    def verify_proof(proof: MerkleProof) -> bool:
        """
        Verify a Merkle inclusion proof.
        
        Args:
            proof: MerkleProof to verify
            
        Returns:
            True if proof is valid, False otherwise
        """
        current_hash = proof.leaf_hash
        
        for sibling, is_right in zip(proof.siblings, proof.path):
            if is_right:
                # Sibling is on the right
                current_hash = MerkleTree.hash_pair(current_hash, sibling)
            else:
                # Sibling is on the left
                current_hash = MerkleTree.hash_pair(sibling, current_hash)
        
        return current_hash == proof.root
    
    def get_tree_info(self) -> dict:
        """
        Get information about the tree structure.
        
        Returns:
            Dictionary with tree statistics
        """
        return {
            'leaf_count': len(self.leaves),
            'tree_height': len(self.tree),
            'root': self.root,
            'levels': [len(level) for level in self.tree]
        }


class DailyMerkleAnchor:
    """
    Daily Merkle tree anchoring service.
    
    Generates daily Merkle roots from event logs and prepares
    them for on-chain anchoring.
    """
    
    def __init__(self):
        """Initialize the anchoring service."""
        self.anchored_roots = {}  # date -> root mapping
    
    def generate_daily_root(self, date: str, event_hashes: List[str]) -> str:
        """
        Generate Merkle root for a day's events.
        
        Args:
            date: Date string (YYYY-MM-DD)
            event_hashes: List of event hashes for the day
            
        Returns:
            Merkle root hash
        """
        if not event_hashes:
            # Empty day - use zero hash
            root = hashlib.sha256(b'empty').hexdigest()
        else:
            tree = MerkleTree(event_hashes)
            root = tree.get_root()
        
        self.anchored_roots[date] = root
        return root
    
    def get_root_for_date(self, date: str) -> Optional[str]:
        """
        Get the anchored root for a specific date.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            Root hash if anchored, None otherwise
        """
        return self.anchored_roots.get(date)
    
    def prepare_anchor_transaction(self, date: str, root: str) -> dict:
        """
        Prepare data for on-chain anchoring transaction.
        
        Args:
            date: Date string
            root: Merkle root hash
            
        Returns:
            Transaction data dictionary
        """
        return {
            'date': date,
            'merkle_root': root,
            'timestamp': None,  # Will be set when anchored
            'tx_hash': None,  # Will be set after anchoring
            'chain': 'ethereum-sepolia',  # Or 'solana-devnet'
            'status': 'pending'
        }


# Example usage
if __name__ == "__main__":
    # Simulate daily event hashes
    event_hashes = [
        hashlib.sha256(f"event_{i}".encode()).hexdigest()
        for i in range(10)
    ]
    
    print(f"Building Merkle tree from {len(event_hashes)} events...")
    
    # Build tree
    tree = MerkleTree(event_hashes)
    print(f"Merkle root: {tree.get_root()}")
    print(f"Tree info: {json.dumps(tree.get_tree_info(), indent=2)}")
    
    # Generate proof for first event
    proof = tree.get_proof(event_hashes[0])
    if proof:
        print(f"\nGenerated proof for event 0:")
        print(proof.to_json())
        
        # Verify proof
        is_valid = MerkleTree.verify_proof(proof)
        print(f"\nProof valid: {is_valid}")
    
    # Daily anchoring
    anchor = DailyMerkleAnchor()
    root = anchor.generate_daily_root("2025-12-12", event_hashes)
    print(f"\nDaily root for 2025-12-12: {root}")
    
    anchor_tx = anchor.prepare_anchor_transaction("2025-12-12", root)
    print(f"Anchor transaction data:")
    print(json.dumps(anchor_tx, indent=2))
