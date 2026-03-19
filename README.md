# AWS What's New MCP Server

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

An MCP server that fetches the latest AWS What's New announcements and service health status.

## Tools

### `fetch_aws_news`

Fetches recent AWS announcements via the official RSS feed.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count`   | int  | 10      | Number of posts to fetch (1–50) |

Returns a list of objects with `id`, `title`, `link`, `published`, `categories`, and `description`.

### `fetch_aws_status`

Fetches current AWS service disruptions from the [AWS Health Dashboard](https://health.aws.amazon.com).

No parameters. Returns active events only — an empty list means all services are operating normally.

Each event includes `region`, `service`, `summary`, `status`, `started`, `latest_update`, and `impacted_services`.

## Setup

```bash
# Install dependencies
pip install fastmcp httpx

# Or using uv
uv pip install fastmcp httpx
```

## Usage

### Run directly

```bash
python server.py
```

### MCP client configuration

Add to your MCP client config (e.g. `~/.kiro/settings.json` or Claude Desktop):

```json
{
  "mcpServers": {
    "aws-whats-new": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/aws-whats-new-mcp"
    }
  }
}
```

Or with `uv`:

```json
{
  "mcpServers": {
    "aws-whats-new": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/path/to/aws-whats-new-mcp"
    }
  }
}
```

## License

Apache 2.0 © 2026 Paulo Pereira
