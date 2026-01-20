from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Union, BinaryIO, Optional
from fastapi import HTTPException, status

def extract_text_from_pdf(file_input: Union[str, BinaryIO], password: Optional[str] = None) -> list[dict]:
    """
    Reads a PDF file (path or binary stream) and extracts text.
    Handles password protection.
    Returns a list of CHUNKS (not just pages).
    """
    try:
        reader = PdfReader(file_input)

        # ---------------------------------------------------------
        # MODIFICATION: Password Logic
        # ---------------------------------------------------------
        if reader.is_encrypted:
            if password:
                # Attempt to decrypt
                result = reader.decrypt(password)
                if result == 0:  # 0 means decryption failed
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect password for encrypted PDF"
                    )
            else:
                # Encrypted but no password provided
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, # 422 triggers the UI to ask for password
                    detail="PDF is password protected. Please provide a password."
                )

        pages = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages.append({
                "page": idx + 1,
                "text": text
            })

        # Pass the extracted pages to the chunking function
        return chunk_text(pages)

    except HTTPException:
        raise  # Re-raise known HTTP errors so the API catches them
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read PDF: {str(e)}"
        )

def chunk_text(pages: list[dict], chunk_size=500, overlap=50) -> list[dict]:
    """
    Splits page text into smaller overlapping chunks.
    This function remains unchanged but is critical for the pipeline.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []
    for page in pages:
        # Split the text of this specific page
        page_chunks = text_splitter.split_text(page["text"])
        
        # Add metadata (page number) to each chunk
        for chunk_text in page_chunks:
            chunks.append({
                "text": chunk_text,
                "page": page["page"]
            })
            
    return chunks