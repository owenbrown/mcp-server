# MCP Server for Veryfi Document Processing

## Overview

A Model Context Protocol (MCP) server implementation that integrates with Veryfi for data extraction from documents


## Setup

### Get your Veryfi username, client_id, and api key
Log into [https://app.veryfi.com](https://app.veryfi.com), then navigate to [https://app.veryfi.com/api/settings/keys/]("https://app.veryfi.com/api/settings/keys/)



### With Claude Desktop

Modify claude_desktop_config.json to include this:

Do not set environment variables here. It will cause confusion if the enviroment
variables used by the MCP server differ from those used by your other code.

Instead, setting them in your execution environmont or using a .env file.

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
            "env": {}
        }
    }
}
```


## Development Setup

### Local Development

1. Clone the repository
2. Create a `.env` file with the following variables:

   ```bash
   VERYFI_CLIENT_ID="veryfi-client-id-goes-here_client_id"
   VERYFI_USERNAME="veryfi-username-goes-here"
   VERYFI_API_KEY="veryfi-api-key-goes-here"
   ```

Alternatively, you can set your environment variables
in your execution environment. For example, on a Mac,
append this to your ~/.zprofile
```bash
export VERYFI_CLIENT_ID="veryfi-client-id-goes-here_client_id"
export VERYFI_USERNAME="veryfi-username-goes-here"
export VERYFI_API_KEY="veryfi-api-key-goes-here"
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

