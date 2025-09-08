"""
Examples of using the Ultrahuman MCP Server

This file demonstrates how to interact with the Ultrahuman MCP Server
using different MCP client libraries and approaches.
"""

import asyncio
import os
from datetime import datetime, timedelta

# Example 1: Direct tool usage (for testing)
async def example_direct_usage():
    """Example of testing tools directly"""
    print("=== Direct Tool Usage Example ===")
    
    from main import get_user_metrics, get_sleep_data, get_glucose_metrics
    
    # Test parameters
    email = "test@example.com"
    date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Testing with email: {email}, date: {date}")
    
    try:
        # This will fail without API key, but shows the structure
        result = await get_user_metrics(email, date)
        print("User metrics result:", result)
        
    except Exception as e:
        print(f"Expected error (no API key): {e}")


# Example 2: Using with MCP Client Session
async def example_mcp_client():
    """Example using MCP client session"""
    print("\n=== MCP Client Session Example ===")
    
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        
        # Server parameters
        server_params = StdioServerParameters(
            command="python3",
            args=["main.py"],
            env={"ULTRAHUMAN_AUTH_KEY": os.getenv("ULTRAHUMAN_AUTH_KEY", "test_key")}
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize connection
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print(f"Available tools: {[tool.name for tool in tools.tools]}")
                
                # Call a tool
                result = await session.call_tool(
                    "get_user_metrics",
                    {
                        "email": "test@example.com",
                        "date": "2024-01-15"
                    }
                )
                print("Tool result:", result)
                
    except ImportError:
        print("MCP client library not available. Install with: pip install mcp")
    except Exception as e:
        print(f"MCP client error: {e}")


# Example 3: HTTP client usage (when deployed)
async def example_http_client():
    """Example using HTTP requests to deployed server"""
    print("\n=== HTTP Client Example ===")
    
    import httpx
    
    # Replace with your actual deployed URL
    base_url = "https://your-project-name.railway.app/mcp"
    
    try:
        async with httpx.AsyncClient() as client:
            # Check server status
            response = await client.get(f"{base_url}/health")
            print(f"Server status: {response.status_code}")
            
            # List tools
            response = await client.post(
                f"{base_url}/tools/list",
                json={}
            )
            
            if response.status_code == 200:
                tools = response.json()
                print(f"Available tools: {tools}")
            
            # Call a tool
            tool_request = {
                "name": "get_user_metrics",
                "arguments": {
                    "email": "test@example.com",
                    "date": "2024-01-15"
                }
            }
            
            response = await client.post(
                f"{base_url}/tools/call",
                json=tool_request
            )
            
            result = response.json()
            print("Tool result:", result)
            
    except Exception as e:
        print(f"HTTP client error: {e}")


# Example 4: Data analysis workflow
async def example_health_analysis():
    """Example of a complete health data analysis workflow"""
    print("\n=== Health Analysis Workflow Example ===")
    
    # This example shows how you might use multiple tools together
    # to analyze a user's health data over time
    
    user_email = "user@example.com"
    base_date = datetime.now() - timedelta(days=7)
    
    # Collect data for the past week
    daily_data = []
    
    for i in range(7):
        date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"Analyzing data for {date}...")
        
        # In a real implementation, you would call the actual tools
        # Here we simulate the structure
        
        day_analysis = {
            "date": date,
            "sleep_quality": "Would get from get_sleep_data",
            "activity_level": "Would get from get_movement_data", 
            "glucose_stability": "Would get from get_glucose_metrics",
            "recovery_status": "Would get from get_heart_metrics"
        }
        
        daily_data.append(day_analysis)
    
    print("Week summary prepared:", len(daily_data), "days")
    
    # Analyze trends
    print("Trend analysis would be performed here...")
    print("- Sleep quality trend")
    print("- Activity consistency")
    print("- Glucose management")
    print("- Recovery patterns")


# Example 5: Real-time monitoring setup
async def example_monitoring_setup():
    """Example of setting up real-time health monitoring"""
    print("\n=== Monitoring Setup Example ===")
    
    # This shows how you might set up automated monitoring
    # of user health metrics
    
    users_to_monitor = [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com"
    ]
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Setting up monitoring for {len(users_to_monitor)} users")
    print(f"Monitoring date: {today}")
    
    for user in users_to_monitor:
        print(f"Monitoring setup for {user}:")
        print("  - Sleep quality alerts")
        print("  - Glucose spike notifications") 
        print("  - Activity goal tracking")
        print("  - Recovery status monitoring")
    
    print("Monitoring system ready!")


async def main():
    """Run all examples"""
    print("Ultrahuman MCP Server - Usage Examples")
    print("=" * 50)
    
    examples = [
        example_direct_usage,
        example_mcp_client,
        example_http_client,
        example_health_analysis,
        example_monitoring_setup
    ]
    
    for example in examples:
        try:
            await example()
        except Exception as e:
            print(f"Example failed: {e}")
        
        print("\n" + "-" * 50)
    
    print("\nAll examples completed!")
    print("\nTo run with real data:")
    print("1. Set ULTRAHUMAN_AUTH_KEY environment variable")
    print("2. Use real user emails with data sharing enabled")
    print("3. Deploy to Railway for production usage")


if __name__ == "__main__":
    asyncio.run(main())
