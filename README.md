# MCP Server for Veryfi Document Processing

## Overview

A Model Context Protocol (MCP) server implementation that integrates with Veryfi for data extraction from documents


## Setup

### With Claude Desktop

Modify claude_desktop_config.json to include this

```
{
    "mcpServers": {
        "veryfi": {
            "command": "uv",
            "args": [
                "--directory",
                "path/to/mcp-server",
                "run",
                "src/server.py"
            ],
            "env": {
                "VERYFI_CLIENT_ID": "...",
                "VERYFI_API_TOKEN": "..."
            }
        }
    }
}
```

In Claude, you can simply prompt with `process document and parameters`

## Development Setup

### Local Development

1. Clone the repository
2. Create a `.env` file with the following variables:

   ```bash
   VERYFI_CLIENT_ID=your_client_id
   VERYFI_API_TOKEN=your_api_token
   ```

3. Install dependencies:

   ```bash
   pip install uv
   uv sync
   ```

4. Run the server locally:

   ```bash
   uv run mcp dev src/server.py
   ```

### Testing

Run the test suite with:

```bash
uv run pytest
```

