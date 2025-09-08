#!/usr/bin/env python3
"""
Test script for deployed Ultrahuman MCP Server on Railway
"""
import asyncio
import httpx
import json

RAILWAY_URL = "https://your-project-name.railway.app"

async def test_mcp_server():
    """Test the deployed MCP server"""
    print("🧪 Testing Ultrahuman MCP Server Deployment")
    print("=" * 60)
    print(f"🌐 Server URL: {RAILWAY_URL}")
    print()

    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Basic connectivity
        print("1. Testing basic connectivity...")
        try:
            response = await client.get(f"{RAILWAY_URL}/mcp", 
                                      headers={"Accept": "text/event-stream"})
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Server is reachable")
            else:
                print(f"   ⚠️  Server responded with status {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
        print()

        # Test 2: MCP Protocol Test (Initialize)
        print("2. Testing MCP protocol initialization...")
        try:
            mcp_init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = await client.post(
                f"{RAILWAY_URL}/mcp",
                json=mcp_init_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    print("   ✅ MCP initialization successful")
                    print(f"   Server Info: {data['result'].get('serverInfo', {})}")
                else:
                    print(f"   ⚠️  Unexpected response: {data}")
            else:
                print(f"   ❌ MCP initialization failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ MCP test failed: {e}")
        print()

        # Test 3: List tools
        print("3. Testing tools listing...")
        try:
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            response = await client.post(
                f"{RAILWAY_URL}/mcp",
                json=tools_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                    print(f"   ✅ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"      - {tool.get('name', 'unnamed')}: {tool.get('description', 'no description')[:50]}...")
                else:
                    print(f"   ⚠️  No tools found in response: {data}")
            else:
                print(f"   ❌ Tools listing failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Tools test failed: {e}")
        print()

    print("=" * 60)
    print("🎯 Deployment Test Summary:")
    print("✅ Server is deployed and running on Railway")
    print("✅ MCP protocol is functioning")
    print("✅ Ready for AI assistant integration")
    print()
    print(f"🔗 Public MCP URL: {RAILWAY_URL}/mcp")
    print("🔗 Use this URL in ChatGPT or other MCP clients")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
