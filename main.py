from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import json
import httpx
import os


load_dotenv()

mcp = FastMCP("nepali_news")

USER_AGENT = "patrika"

NEWS_SITE = {
    "kathmandu-post":"https://kathmandupost.com/"
}

async def fetch_news(url:str):
    """This pulls and summarizes the latest news form the sepcified news site"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url,timeout=30.0)
            soup = BeautifulSoup(response.text,"html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text()for p in paragraphs])
            return text
        except httpx.TimeoutException as e:
            return "Time out"


@mcp.tool()
async def get_nepali_news(source:str)->str:
    """
    Fetch the latest news from a specific nepali news source.

    Args:
    source: Name of the news source( for example,"onlinekhabar" or "kathmandu-post")

    Returns:
    A brief summary of the nepali news
    """
    if source not in NEWS_SITE:
        raise ValueError(f"Source {source} is not supported")
    news_text = await fetch_news(NEWS_SITE[source])
    return news_text


if __name__ == "__main__":
    mcp.run(transport="stdio")
