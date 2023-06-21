import pytest
from langchain.docstore.document import Document
from backend.src.pdf_loader import PdfToTextLoader


@pytest.fixture
def sample_pdf_path(tmp_path):
    # Create a sample PDF file
    pdf_path = tmp_path / "sample.pdf"
    with open(pdf_path, "w") as file:
        file.write("Sample PDF content")
    return str(pdf_path)


def test_pdf_to_text_loader_init(sample_pdf_path):
    loader = PdfToTextLoader(sample_pdf_path)
    assert loader.pdf_path == sample_pdf_path
    assert loader.file_name == "sample.pdf"


def test_PdfToTextLoader_init_invalid_pdf_path():
    with pytest.raises(TypeError):
        PdfToTextLoader(12345)


def test_pdf_to_text_loader_load_single_pdf(sample_pdf_path):
    loader = PdfToTextLoader(sample_pdf_path)
    result = loader.load_single_pdf()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == "Sample PDF content"


def test_pdf_to_text_loader_text_to_docs():
    loader = PdfToTextLoader("")
    text = "Sample text"
    result = loader.text_to_docs(text)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Document)
    assert result[0].page_content == text


def test_pdf_to_text_loader_text_to_docs_multiple_pages():
    loader = PdfToTextLoader("")
    text = ["Page 1", "Page 2"]
    result = loader.text_to_docs(text)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], Document)
    assert result[0].page_content == "Page 1"
    assert isinstance(result[1], Document)
    assert result[1].page_content == "Page 2"
    assert result[1].metadata["page"] == 2
