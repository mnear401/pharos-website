import logging
from sentinel import L2Bridge  # Ensure this matches your file name

# 1. Setup Logging to see the 'Heartbeat'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. Create a 'Mock Provider' (Simulating the Blockchain)
class MockWeb3:
    def eth_block_number(self):
        return 12345678  # Simulating a live block height

def main():
    print("\n[ANCHOR SENTINEL: PULSE TEST INITIATED]")
    
    # 3. Initialize the Bridge
    mock_provider = MockWeb3()
    bridge = L2Bridge()
    
    # 4. Execute the Heartbeat
    # We pass the mock provider's method to your heartbeat function
    pulse = bridge.heartbeat(mock_provider.eth_block_number)
    
    if isinstance(pulse, int) and pulse > 0:
        print(f"SUCCESS: Sentinel Heartbeat Verified at Block {pulse}")
    else:
        print("FAILURE: Heartbeat flatlined.")

if __name__ == "__main__":
    main()