

```markdown
# Chat with PDF - Streamlit Application

## Overview

The **Chat with PDF** application is a powerful tool that allows users to upload PDFs, extract their content, and interact with them through an AI-based question-answering system. Powered by **Claude by Anthropic** and **HuggingFace Embeddings**, this app enables efficient extraction and interaction with data from PDF files.

### Key Features:
- **PDF Content Extraction**: Extracts text from PDF files using `pdfplumber`.
- **AI-Powered Interaction**: Ask questions related to the content of the PDF, and get answers using the **Claude AI model**.
- **Text Embeddings**: Converts extracted PDF text into embeddings stored in a **FAISS vector store** for fast and efficient querying.
- **Error Handling**: Built-in error handling to address API issues, PDF extraction failures, and embedding creation problems.
- **Retry Mechanism**: Uses the **Tenacity** library to automatically retry embedding creation in case of failure, with exponential backoff.

## Installation

To get started with the application, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/atharvad38/chat_with_pdf.git
cd chat_with_pdf
```

### 2. Install Required Packages
Make sure you have Python 3.x installed, and then install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Setup Anthropic API Key
You will need a valid **Anthropic API key** for the application to work. To get started:
1. Sign up at **Anthropic** and generate your API key.
2. Replace the `api_key` variable in the `app.py` file with your API key.

```python
api_key = 'your-anthropic-api-key-here'
```

### 4. Run the Application
Once everything is set up, you can start the Streamlit app by running:

```bash
streamlit run app.py
```

This will open the application in your default web browser.

## How to Use

1. **Upload a PDF**: Select and upload a PDF file using the file uploader in the app.
2. **PDF Processing**: The app will extract the text content from the PDF and create embeddings from the text.
3. **Ask Questions**: Once the embeddings are created, you can ask questions based on the document. The AI model will generate answers using the extracted content from the PDF.

## Code Explanation

### Key Components:

- **PDFProcessor Class**:
  - **`extract_pdf_content`**: This function extracts text from a PDF file using `pdfplumber`.
  - **`create_embeddings`**: This function converts the extracted text into embeddings and stores them in a **FAISS vector store** for efficient similarity search.
  - **`validate_api_key`**: Verifies that the provided Anthropic API key is valid.

- **Main Logic**:
  - Uses **Streamlit** to create a user interface.
  - **PDF Upload**: Users upload a PDF, and the app processes and creates embeddings for it.
  - **Question-Answering**: Once the PDF is processed, users can interact with the document by asking questions, and the AI provides answers based on the PDF content.

### Error Handling:
- Uses the **Tenacity** package for retries, particularly for the embedding creation process. If the creation fails, it retries up to 3 times with an exponential backoff.

## Requirements
- **Python 3.x**
- **Streamlit**
- **pdfplumber** (For extracting text from PDFs)
- **Pandas**
- **Langchain (Anthropic)**
- **HuggingFace Embeddings**
- **FAISS** (For efficient vector storage and search)
- **Tenacity** (For retry logic)
- **Logging** (For error and info logging)

![WhatsApp Image 2024-12-31 at 01 36 36_b895e6cd](https://github.com/user-attachments/assets/7d6441c3-662d-43e9-8033-4e15637585a6)


