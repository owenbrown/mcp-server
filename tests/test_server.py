import pytest

from server import process_document

# Mark the test file as async
pytestmark = pytest.mark.asyncio

# Sample Veryfi API response
MOCK_RESPONSE = {
    "id": 123456,
    "total": 45.67,
    "date": "2025-03-31",
    "vendor": {"name": "Test Store"},
}


@pytest.fixture
def mock_file(tmp_path):
    """Create a temporary PDF file for testing."""
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes(b"%PDF-1.4 fake content")  # Minimal PDF content
    return str(file_path)


@pytest.asyncio
async def test_process_document_success(httpx_mock, mock_file):
    """Test process_document with a mocked successful API response."""
    # Mock the Veryfi API response
    httpx_mock.add_response(
        url="https://api.veryfi.com/api/v8/partner/documents",
        method="POST",
        json=MOCK_RESPONSE,
        status_code=200,
    )

    # Call the function with the mock file
    result = await process_document(mock_file)

    # Assertions
    assert result == MOCK_RESPONSE
    assert result["total"] == 45.67
    assert result["vendor"]["name"] == "Test Store"


@pytest.asyncio
async def test_process_document_file_not_found():
    """Test process_document with a non-existent file."""
    with pytest.raises(ValueError, match="File not found: nonexistent.pdf"):
        await process_document("nonexistent.pdf")
