import asyncio
import base64
import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from validate_credentials import check_veryfi_credentials

load_dotenv()

# Get Veryfi credentials from environment
VERYFI_CLIENT_ID = os.getenv("VERYFI_CLIENT_ID")
VERYFI_USERNAME = os.getenv("VERYFI_USERNAME")
VERYFI_API_KEY = os.getenv("VERYFI_API_KEY")
VERYFI_API_URL = "https://api.veryfi.com/api/v8/partner/documents"


server = FastMCP(name="veryfi-mcp")


@server.tool(
    name="process_document",
    description="Upload a document to Veryfi and extract data from receipts, invoices, etc.",
)
async def process_document(file_path: str, document_type: str = "receipt") -> dict:
    """Upload a document to Veryfi and extract data.

    Args:
        file_path: Path to the document file to process
        document_type: Type of document (default: "receipt")

    Returns:
        dict: Extracted data from Veryfi API
    """
    # Check credentials before processing
    error_message = check_veryfi_credentials()
    if error_message:
        raise ValueError(error_message)

    logging.info(f"Processing document: {file_path}")

    # Read and encode file
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "rb") as file:
        content_bytes = file.read()

    file_data = base64.b64encode(content_bytes).decode("utf-8")

    # Prepare payload
    payload = {
        "categories": [],
        "tags": [],
        "compute": True,
        "document_type": document_type,
        "file_data": file_data,
    }

    # Prepare headers with correct authentication format
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "CLIENT-ID": VERYFI_CLIENT_ID,
        "AUTHORIZATION": f"apikey {VERYFI_USERNAME}:{VERYFI_API_KEY}",
    }

    # Make request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            VERYFI_API_URL,
            json=payload,
            headers=headers,
            timeout=120.0,
        )
        response.raise_for_status()
        result = response.json()
        logging.info(f"Successfully processed document: {path.name}")
        return result


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
