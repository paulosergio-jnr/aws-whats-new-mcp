# AWS What's New MCP Server

An MCP server that fetches the latest AWS What's New announcements via the official RSS feed.

## Tool

### `fetch_aws_news`

Fetches recent AWS announcements.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count`   | int  | 10      | Number of posts to fetch (1–50) |

Returns a list of objects with `title`, `link`, `published`, and `description`.

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

MIT
