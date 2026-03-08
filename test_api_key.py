#!/usr/bin/env python3
"""Test script to validate PocketSmith API key."""

import asyncio
import sys
import aiohttp


async def test_api_key(api_key: str):
    """Test the PocketSmith API key."""
    base_url = "https://api.pocketsmith.com/v2"
    
    print(f"Testing PocketSmith API key...")
    print(f"API URL: {base_url}/me")
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    print()
    
    # Test with Bearer token
    print("Test 1: Using Bearer authentication")
    headers = {"X-Developer-Key": api_key}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{base_url}/me",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                print(f"Status Code: {response.status}")
                print(f"Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ SUCCESS! User: {data.get('login', 'unknown')}")
                    print(f"Response data: {data}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ FAILED with status {response.status}")
                    print(f"Response: {text}")
                    
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    
    # Test with X-Developer-Key (alternative format some APIs use)
    print("Test 2: Using X-Developer-Key authentication")
    headers = {"X-Developer-Key": api_key}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{base_url}/me",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                print(f"Status Code: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ SUCCESS! User: {data.get('login', 'unknown')}")
                    print(f"Response data: {data}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ FAILED with status {response.status}")
                    print(f"Response: {text}")
                    
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_api_key.py YOUR_API_KEY")
        print("\nExample:")
        print("  python test_api_key.py abc123def456...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    result = asyncio.run(test_api_key(api_key))
    
    if result:
        print("\n✅ Your API key is valid and working!")
        print("The integration should work with this key.")
    else:
        print("\n❌ API key validation failed.")
        print("Please check:")
        print("1. API key is copied correctly (no extra spaces)")
        print("2. API key is still active in PocketSmith")
        print("3. You have internet connectivity")
        sys.exit(1)
