import asyncio
import logging
import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

VERYFI_CLIENT_ID = os.getenv("VERYFI_CLIENT_ID")
VERYFI_API_TOKEN = os.getenv("VERYFI_API_TOKEN")
VERYFI_API_URL = "https://api.veryfi.com/api/v8/partner/"
server = FastMCP(name="veryfi-mcp")
AUTH_HEADERS = {
    "client-id": VERYFI_CLIENT_ID,
    "authorization": VERYFI_API_TOKEN,
}


@server.tool(
    name="process_document",
    description="Upload a document to Veryfi and extract data.",
)
async def process_document(**parameters) -> dict:
    """Upload a document to Veryfi and extract data."""
    logging.info(f"Processing with parameters: {parameters['parameters']}")
    document_type = parameters["parameters"].pop("document_type", "documents")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{VERYFI_API_URL}/{document_type}",
            headers=AUTH_HEADERS,
            json=parameters["parameters"],
            timeout=120,
        )
        response.raise_for_status()
        return response.json()


# @server.resource("data://documents", mime_type="application/json")
# async def get_documents(document_type: str) -> dict:
#     logging.info("Getting documents")
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"{VERYFI_API_URL}/{document_type}",
#             headers=AUTH_HEADERS,
#             timeout=60,
#         )
#         response.raise_for_status()
#         result = response.json()
#         logging.info(f"Got response: {result}")
#         return result


# @server.resource("data://documents/{id}")
# async def get_document(id: int, document_type: str) -> str:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"{VERYFI_API_URL}/{document_type}/{id}",
#             headers=AUTH_HEADERS,
#             timeout=15,
#         )
#         response.raise_for_status()
#         result = response.json()
#         logging.info(f"Got response: {result}")
#         return result


if __name__ == "__main__":
    logging.info("MCP server starting...")
    try:
        asyncio.run(server.run())
    except Exception:
        logging.exception("Server failed")
