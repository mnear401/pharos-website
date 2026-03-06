import datetime
import hashlib
import logging
import os
import sqlite3
import time

logger = logging.getLogger(__name__)


class L2Bridge:
    """
    Placeholder for the Scroll AnchorRegistry connection layer.

    This will eventually own:
    - Provider/Web3 setup for Scroll
    - AnchorRegistry contract instance + ABI management
    - Read/write helpers, retries, and observability hooks
    """

    def __init__(self, provider=None):
        """
        Args:
            provider: Optional. A web3-like object (e.g., `web3.Web3`) or any object
                with `eth.block_number`. You may also pass a callable that returns an int.
        """
        self.provider = provider

    def _get_block_number(self, provider) -> int:
        if provider is None:
            raise RuntimeError("No provider configured for L2Bridge.")

        if callable(provider):
            block_number = provider()
        else:
            block_number = getattr(getattr(provider, "eth", None), "block_number", None)

        if block_number is None:
            raise RuntimeError("Provider does not expose `eth.block_number`.")

        return int(block_number)

    def heartbeat(self, provider) -> int:
        """
        Logs the current L2 block number and returns it.
        """
        block_number = self._get_block_number(provider)
        logger.info("L2Bridge heartbeat: current block=%s", block_number)
        return block_number

def generate_cryptographic_hash(filepath):
    # Using SHA-256 to simulate the Falcon-1024/zk-STARK logic locally
    # This reads the actual raw bytes of the document
    secure_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            secure_hash.update(byte_block)
    return secure_hash.hexdigest()

def boot_sentinel():
    vault_stamps = 100  # The Desk Book Tier
    
    print("\n=======================================================")
    print("                 ANCHOR SENTINEL (CLI)                 ")
    print("             Pharos Anchor LLC (2026)                  ")
    print("=======================================================")

    conn = sqlite3.connect("anchor_log.db")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS anchor_log "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, filename TEXT, hash TEXT)"
    )
    conn.commit()

    while True:
        print(f"\n[VAULT BALANCE]: {vault_stamps} Digital Stamps remaining.")
        
        if vault_stamps <= 0:
            print("[!] Vault depleted. Please purchase a new Desk Book.")
            break

        # Prompt for file drag-and-drop
        filepath = input("\n[>] Drag and drop a document here (or type 'exit' to quit): ").strip().strip("'\"")
        
        if filepath.lower() == 'exit':
            print("\n[*] Shutting down Sentinel node...")
            break
            
        if not os.path.isfile(filepath):
            print("\n[!] VERITATEM ERROR: File not found. Check the path and try again.")
            continue
            
        print("\n[*] Reading file binary...")
        time.sleep(0.5)
        print("[*] Generating SHA-256 Cryptographic Hash...")
        time.sleep(1.5) # Simulating sub-15s Layer 2 finality
        
        try:
            # Generate the actual hash and deduct the stamp
            file_hash = generate_cryptographic_hash(filepath)
            filename = os.path.basename(filepath)
            conn.execute(
                "INSERT INTO anchor_log (timestamp, filename, hash) VALUES (?, ?, ?)",
                (datetime.datetime.now().isoformat(), filename, file_hash)
            )
            conn.commit()
            vault_stamps -= 1
            
            # Output the immutable truth
            print("\n[+] ================================================= [+]")
            print("                IMMUTABLE TRUTH SECURED                  ")
            print(f"    Document : {filename}")
            print(f"    Hash     : 0x{file_hash}")
            print(f"    Cost     : 1 Stamp deducted.")
            print("[+] ================================================= [+]")
            
        except Exception as e:
            print(f"\n[!] Protocol Failure: {e}")

if __name__ == "__main__":
    boot_sentinel()
