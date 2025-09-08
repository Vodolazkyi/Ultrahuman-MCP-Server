"""
Test script for Ultrahuman MCP Server
"""
import asyncio
import os
from datetime import datetime, timedelta
from main import mcp

async def test_tools():
    """Test the MCP tools functionality"""
    print("Testing Ultrahuman MCP Server Tools...")
    print("=" * 50)
    
    # Test email and date
    test_email = "test@example.com"
    test_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Test Email: {test_email}")
    print(f"Test Date: {test_date}")
    print()
    
    # Test tools directly (will fail without real API key, but we can test structure)
    from main import get_user_metrics, get_sleep_data, get_movement_data, get_glucose_metrics, get_heart_metrics
    
    tools_to_test = [
        ("get_user_metrics", get_user_metrics),
        ("get_sleep_data", get_sleep_data), 
        ("get_movement_data", get_movement_data),
        ("get_glucose_metrics", get_glucose_metrics),
        ("get_heart_metrics", get_heart_metrics)
    ]
    
    for tool_name, tool_func in tools_to_test:
        print(f"1. Testing {tool_name}...")
        try:
            # This will fail without API key, but tests the tool structure
            result = await tool_func(test_email, test_date)
            
            if result.get("success"):
                print(f"✅ {tool_name} working")
            else:
                print(f"⚠️  {tool_name} returned error (expected without API key): {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"⚠️  {tool_name} failed (expected without API key): {e}")
        print()
    
    # Test resource
    print("2. Testing API Info Resource...")
    try:
        # Since it's a function resource, we need to call it
        info_func = mcp._resources["ultrahuman://api-info"]
        info = await info_func()
        print("✅ API Info resource working")
        print(f"Info length: {len(info)} characters")
    except Exception as e:
        print(f"❌ API Info resource failed: {e}")
    print()

    print("=" * 50)
    print("Test completed!")
    print()
    print("To test with real data:")
    print("1. Set ULTRAHUMAN_AUTH_KEY environment variable")
    print("2. Use a real user email that has shared data")
    print("3. Use a date that has available data")

if __name__ == "__main__":
    asyncio.run(test_tools())
