"""
Ultrahuman MCP Server

This server provides access to Ultrahuman Partnership API data through MCP tools.
"""
import os
import asyncio
from datetime import datetime, date
from typing import Optional, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Ultrahuman")

# Environment variables for configuration
ULTRAHUMAN_AUTH_KEY = os.getenv("ULTRAHUMAN_AUTH_KEY")
ULTRAHUMAN_BASE_URL = os.getenv("ULTRAHUMAN_BASE_URL", "https://partner.ultrahuman.com/api/v1")
DEFAULT_EMAIL = os.getenv("ULTRAHUMAN_DEFAULT_EMAIL")


class UltrahumanClient:
    """Client for interacting with Ultrahuman Partnership API"""
    
    def __init__(self, auth_key: str, base_url: str = "https://partner.ultrahuman.com/api/v1"):
        self.auth_key = auth_key
        self.base_url = base_url
        self.headers = {
            "Authorization": auth_key,
            "Content-Type": "application/json"
        }
    
    async def get_metrics(self, email: str, date_str: str) -> Dict[str, Any]:
        """Get metrics for a specific user and date"""
        url = f"{self.base_url}/metrics"
        params = {
            "email": email,
            "date": date_str
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()


@mcp.tool
async def get_default_user_metrics(date: str) -> Dict[str, Any]:
    """
    Get comprehensive health metrics for the default user (from environment) on a specific date.
    
    Args:
        date: Date in YYYY-MM-DD format (e.g., "2024-01-15")
    
    Returns:
        Dictionary containing user's health metrics including all available data
    """
    if not DEFAULT_EMAIL:
        return {
            "success": False,
            "error": "ULTRAHUMAN_DEFAULT_EMAIL environment variable not set",
            "date": date
        }
    
    return await get_user_metrics(DEFAULT_EMAIL, date)


@mcp.tool
async def get_user_metrics(email: str, date: str) -> Dict[str, Any]:
    """
    Get comprehensive health metrics for a specific user and date from Ultrahuman.
    
    Args:
        email: User's email address (e.g., user@example.com)
        date: Date in YYYY-MM-DD format (e.g., "2024-01-15")
    
    Returns:
        Dictionary containing user's health metrics including:
        - Sleep Data
        - Movement Data  
        - Heart Rate
        - HRV (Heart Rate Variability)
        - Temperature
        - Steps
        - Glucose
        - Metabolic Score
        - Glucose Variability (%)
        - Average Glucose (mg/dL)
        - HbA1c
        - Time in Target (%)
        - Recovery Index
        - Movement Index
        - VO2 Max
    """
    if not ULTRAHUMAN_AUTH_KEY:
        raise ValueError("ULTRAHUMAN_AUTH_KEY environment variable is required")
    
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")
    
    client = UltrahumanClient(ULTRAHUMAN_AUTH_KEY, ULTRAHUMAN_BASE_URL)
    
    try:
        metrics = await client.get_metrics(email, date)
        return {
            "success": True,
            "email": email,
            "date": date,
            "metrics": metrics
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "email": email,
            "date": date
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "email": email,
            "date": date
        }


@mcp.tool
async def get_sleep_data(email: str, date: str) -> Dict[str, Any]:
    """
    Get sleep-specific data for a user on a specific date.
    
    Args:
        email: User's email address
        date: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing sleep metrics
    """
    metrics = await get_user_metrics(email, date)
    
    if not metrics.get("success"):
        return metrics
    
    sleep_data = metrics.get("metrics", {}).get("sleep_data", {})
    return {
        "success": True,
        "email": email,
        "date": date,
        "sleep_data": sleep_data
    }


@mcp.tool
async def get_movement_data(email: str, date: str) -> Dict[str, Any]:
    """
    Get movement and activity data for a user on a specific date.
    
    Args:
        email: User's email address
        date: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing movement metrics including steps, movement index, etc.
    """
    metrics = await get_user_metrics(email, date)
    
    if not metrics.get("success"):
        return metrics
    
    movement_data = {
        "steps": metrics.get("metrics", {}).get("steps"),
        "movement_index": metrics.get("metrics", {}).get("movement_index"),
        "movement_data": metrics.get("metrics", {}).get("movement_data", {})
    }
    
    return {
        "success": True,
        "email": email,
        "date": date,
        "movement_data": movement_data
    }


@mcp.tool
async def get_glucose_metrics(email: str, date: str) -> Dict[str, Any]:
    """
    Get glucose-related metrics for a user on a specific date.
    
    Args:
        email: User's email address
        date: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing glucose metrics including glucose levels, variability, HbA1c, etc.
    """
    metrics = await get_user_metrics(email, date)
    
    if not metrics.get("success"):
        return metrics
    
    glucose_data = {
        "glucose": metrics.get("metrics", {}).get("glucose"),
        "glucose_variability": metrics.get("metrics", {}).get("glucose_variability"),
        "average_glucose": metrics.get("metrics", {}).get("average_glucose"),
        "hba1c": metrics.get("metrics", {}).get("hba1c"),
        "time_in_target": metrics.get("metrics", {}).get("time_in_target"),
        "metabolic_score": metrics.get("metrics", {}).get("metabolic_score")
    }
    
    return {
        "success": True,
        "email": email,
        "date": date,
        "glucose_data": glucose_data
    }


@mcp.tool
async def get_heart_metrics(email: str, date: str) -> Dict[str, Any]:
    """
    Get heart-related metrics for a user on a specific date.
    
    Args:
        email: User's email address
        date: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing heart rate, HRV, and recovery metrics
    """
    metrics = await get_user_metrics(email, date)
    
    if not metrics.get("success"):
        return metrics
    
    heart_data = {
        "heart_rate": metrics.get("metrics", {}).get("heart_rate"),
        "hrv": metrics.get("metrics", {}).get("hrv"),
        "recovery_index": metrics.get("metrics", {}).get("recovery_index"),
        "vo2_max": metrics.get("metrics", {}).get("vo2_max")
    }
    
    return {
        "success": True,
        "email": email,
        "date": date,
        "heart_data": heart_data
    }


@mcp.resource("ultrahuman://api-info")
async def get_api_info() -> str:
    """Get information about the Ultrahuman Partnership API"""
    return """
    Ultrahuman Partnership API Information
    
    The Partnership API gives you full access to the data generated by Ultrahuman devices.
    
    Available Metrics:
    1. Sleep Data - Sleep patterns, quality, duration
    2. Movement Data - Activity levels, movement patterns
    3. Heart Rate - Continuous heart rate monitoring
    4. HRV - Heart Rate Variability measurements
    5. Temperature - Body temperature readings
    6. Steps - Daily step count
    7. Glucose - Blood glucose levels (from CGM)
    8. Metabolic Score - Overall metabolic health score
    9. Glucose Variability (%) - Blood sugar stability
    10. Average Glucose (mg/dL) - Daily glucose average
    11. HbA1c - Long-term glucose control indicator
    12. Time in Target (%) - Time spent in target glucose range
    13. Recovery Index - Recovery status metrics
    14. Movement Index - Movement quality assessment
    15. VO2 Max - Cardiovascular fitness measure
    
    API Environments:
    - Live: https://partner.ultrahuman.com/api/v1/metrics
    - Test: https://www.staging.ultrahuman.com/api/v1/metrics
    
    Authentication:
    - Authorization key required in header
    - Data sharing code needed for user consent
    """


if __name__ == "__main__":
    # Run the server with HTTP transport for web deployment
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
