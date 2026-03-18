import json
import re
from datetime import datetime, timezone
from html import unescape
from xml.etree import ElementTree

import httpx
from fastmcp import FastMCP

mcp = FastMCP(name="AWS What's New")

AWS_WHATS_NEW_RSS = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
AWS_HEALTH_EVENTS = "https://health.aws.amazon.com/public/currentevents"

STATUS_MAP = {"0": "resolved", "1": "informational", "2": "degraded", "3": "disruption"}


def _strip_html(text: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", text)).strip()


def _parse_categories(raw: str) -> list[str]:
    """Extract clean service/category names from the RSS category field."""
    if not raw:
        return []
    # e.g. "general:products/amazon-connect,marketing:marchitecture/serverless"
    return [seg.split("/", 1)[1] for seg in raw.split(",") if "/" in seg]


@mcp.tool
async def fetch_aws_news(count: int = 10) -> list[dict]:
    """Fetch the latest AWS What's New announcements.

    Each result includes a unique `id` field that remains stable across calls.
    Use it to avoid processing announcements you have already seen.

    Args:
        count: Number of announcements to return (default 10, max 50).
    """
    count = max(1, min(count, 50))

    async with httpx.AsyncClient() as client:
        resp = await client.get(AWS_WHATS_NEW_RSS, timeout=30)
        resp.raise_for_status()

    root = ElementTree.fromstring(resp.text)
    items = root.findall(".//item")[:count]

    return [
        {
            "id": item.findtext("guid", ""),
            "title": item.findtext("title", ""),
            "link": item.findtext("link", ""),
            "published": item.findtext("pubDate", ""),
            "categories": _parse_categories(item.findtext("category", "")),
            "description": _strip_html(item.findtext("description", "")),
        }
        for item in items
    ]


@mcp.tool
async def fetch_aws_status() -> list[dict]:
    """Fetch current AWS service disruptions from the AWS Health Dashboard.

    Returns active events only. An empty list means all services are operating normally.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(AWS_HEALTH_EVENTS, timeout=30)
        resp.raise_for_status()

    events = json.loads(resp.content.decode("utf-16"))

    return [
        {
            "region": event["region_name"],
            "service": event["service_name"],
            "summary": event["summary"],
            "status": STATUS_MAP.get(event["status"], event["status"]),
            "started": datetime.fromtimestamp(
                int(event["date"]), tz=timezone.utc
            ).isoformat(),
            "latest_update": event["event_log"][-1]["message"] if event.get("event_log") else "",
            "impacted_services": [
                {
                    "name": s["service_name"],
                    "current": STATUS_MAP.get(s["current"], s["current"]),
                    "max": STATUS_MAP.get(s["max"], s["max"]),
                }
                for s in event.get("impacted_services", {}).values()
            ],
        }
        for event in events
    ]


if __name__ == "__main__":
    mcp.run()
