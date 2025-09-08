# Ultrahuman MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.12+-green.svg)](https://github.com/jlowin/fastmcp)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)

A Model Context Protocol (MCP) server that provides access to Ultrahuman API data. This server allows AI assistants and applications to interact with Ultrahuman health and fitness data through standardized MCP tools.

## Features

- **Complete Health Metrics Access**: Sleep, movement, heart rate, HRV, glucose, and more
- **Specialized Tools**: Dedicated tools for different data types (sleep, movement, glucose, heart metrics)
- **Error Handling**: Robust error handling with detailed error messages
- **Date Validation**: Automatic validation of date formats
- **Environment Configuration**: Flexible configuration through environment variables

## Available Tools

### Core Tools

- `get_default_user_metrics(date)` - Get all health metrics for default user (from env) on a specific date
- `get_user_metrics(email, date)` - Get all health metrics for a user on a specific date
- `get_sleep_data(email, date)` - Get sleep-specific metrics
- `get_movement_data(email, date)` - Get movement and activity data
- `get_glucose_metrics(email, date)` - Get glucose-related metrics
- `get_heart_metrics(email, date)` - Get heart rate, HRV, and recovery data

### Resources

- `ultrahuman://api-info` - Information about the Ultrahuman Partnership API

## Available Metrics

The server provides access to the following health metrics:

1. **Sleep Data** - Sleep patterns, quality, duration
2. **Movement Data** - Activity levels, movement patterns  
3. **Heart Rate** - Continuous heart rate monitoring
4. **HRV** - Heart Rate Variability measurements
5. **Temperature** - Body temperature readings
6. **Steps** - Daily step count
7. **Glucose** - Blood glucose levels (from CGM)
8. **Metabolic Score** - Overall metabolic health score
9. **Glucose Variability (%)** - Blood sugar stability
10. **Average Glucose (mg/dL)** - Daily glucose average
11. **HbA1c** - Long-term glucose control indicator
12. **Time in Target (%)** - Time spent in target glucose range
13. **Recovery Index** - Recovery status metrics
14. **Movement Index** - Movement quality assessment
15. **VO2 Max** - Cardiovascular fitness measure

## Setup

### Prerequisites

1. **Ultrahuman API Access**:
   - Authorization key (40-character alpha-numeric string)
   - Data sharing code from users
   - User email with granted access
   - **📋 See detailed setup instructions**: [API_SETUP.md](./API_SETUP.md)
   - Contact support@ultrahuman.com for API access
   - API documentation: https://blog.ultrahuman.com/blog/accessing-the-ultrahuman-partnership-api/

2. **Python 3.11+**

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Vodolazkyi/Ultrahuman-Server.git
cd Ultrahuman-Server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp env.example .env
# Edit .env with your Ultrahuman API credentials
```

4. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000/mcp` by default.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ULTRAHUMAN_AUTH_KEY` | Your 40-character authorization key | Required |
| `ULTRAHUMAN_BASE_URL` | API base URL | `https://partner.ultrahuman.com/api/v1` |
| `ULTRAHUMAN_DEFAULT_EMAIL` | Default user email for testing | Optional |
| `PORT` | Server port | `8000` |

## Usage Examples

### Using with MCP Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
        env={"ULTRAHUMAN_AUTH_KEY": "your_key_here"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Get user metrics
            result = await session.call_tool(
                "get_user_metrics",
                {
                    "email": "user@example.com",
                    "date": "2024-01-15"
                }
            )
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Tool Examples

#### Get Complete Metrics
```python
# Get all metrics for a user
result = await session.call_tool("get_user_metrics", {
    "email": "user@example.com",
    "date": "2024-01-15"
})
```

#### Get Sleep Data Only
```python
# Get sleep-specific data
result = await session.call_tool("get_sleep_data", {
    "email": "user@example.com", 
    "date": "2024-01-15"
})
```

#### Get Glucose Metrics
```python
# Get glucose-related metrics
result = await session.call_tool("get_glucose_metrics", {
    "email": "user@example.com",
    "date": "2024-01-15"
})
```

## API Response Format

All tools return a consistent response format:

```json
{
    "success": true,
    "email": "user@example.com",
    "date": "2024-01-15",
    "metrics": {
        // ... actual metrics data
    }
}
```

On error:
```json
{
    "success": false,
    "email": "user@example.com", 
    "date": "2024-01-15",
    "error": "Error description"
}
```

## Deployment

### Railway Deployment

This server is configured for deployment on Railway:

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `ULTRAHUMAN_AUTH_KEY`
   - `ULTRAHUMAN_BASE_URL` (optional)
3. Deploy automatically from main branch

### Docker Deployment

```bash
# Build the image
docker build -t ultrahuman-mcp .

# Run the container
docker run -p 8000:8000 \
  -e ULTRAHUMAN_AUTH_KEY=your_key_here \
  ultrahuman-mcp
```

## API Environments

- **Production**: `https://partner.ultrahuman.com/api/v1/metrics`
- **Staging**: `https://www.staging.ultrahuman.com/api/v1/metrics`

## Error Handling

The server includes comprehensive error handling:

- **Authentication Errors**: Invalid or missing authorization key
- **Validation Errors**: Invalid email format or date format
- **API Errors**: HTTP errors from Ultrahuman API
- **Network Errors**: Connection timeouts or network issues

## Security

- API keys are managed through environment variables
- All API requests use HTTPS
- No sensitive data is logged or cached

## Contributing

We welcome contributions! Please feel free to:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues related to:
- **MCP Server**: Open an issue in this repository
- **Ultrahuman API**: Contact Ultrahuman support
- **FastMCP**: Check the [FastMCP documentation](https://github.com/jlowin/fastmcp)

## Repository Setup

For maximum visibility and SEO optimization, see [GITHUB_SETUP.md](./GITHUB_SETUP.md) for detailed instructions on:
- Configuring GitHub About section with proper tags
- SEO optimization for search engines
- Adding to MCP showcases and awesome lists

## Links

- [Ultrahuman API Documentation](https://blog.ultrahuman.com/blog/accessing-the-ultrahuman-partnership-api/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Awesome MCP](https://github.com/modelcontextprotocol/awesome-mcp) - Add your project here!
