import os
import re
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PdfToTextLoader:
    """
        Class for loading pdfs and saving them as texts
    """

    def __init__(self, pdf_path: str) -> None:
        """
            Args:
                pdf_path (str): path to pdf file
        """

        if not isinstance(pdf_path, str):
            raise TypeError(f"Type {type(pdf_path)} is not suported for `pdf_path`.")
        self.pdf_path = pdf_path
        self.file_name = os.path.basename(self.pdf_path)

    def load_single_pdf(self) -> list:
        """
            Loads pdf file and saves it as list of strings

            Returns:
                list: list of texts from pdf
        """

        pdf = PyPDFLoader(self.pdf_path)
        output = []
        for page in pdf.load_and_split():
            text = page.page_content
            # Merge hyphenated words
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            # Fix newlines in the middle of sentences
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            output.append(text)
        return output

    def text_to_docs(self, text: str) -> list:
        """
            Converts a string or list of strings to a list of Documents with metadata.

            Args:
                text (str|list): string or list of strings from pdf

            Returns:
                list: list of chunked Document
        """

        if isinstance(text, str):
            # Take a single string as one page
            text = [text]
        page_docs = [Document(page_content=page) for page in text]

        # Add page numbers as metadata
        for i, doc in enumerate(page_docs):
            doc.metadata["page"] = i + 1

        # Split pages into chunks
        doc_chunks = []

        for doc in page_docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                chunk_overlap=0,
            )
            chunks = text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk, metadata={"file": self.pdf_path, "page": doc.metadata["page"], "chunk": i}
                )

                # Add sources a metadata
                doc.metadata["source"] = f"File:{self.file_name} Page:{doc.metadata['page']} Part:{doc.metadata['chunk']}."
                doc_chunks.append(doc)
        return doc_chunks
