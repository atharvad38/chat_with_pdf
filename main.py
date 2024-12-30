
import streamlit as st
import pdfplumber
import pandas as pd
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None

class PDFProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
            self.chat_model = ChatAnthropic(
                anthropic_api_key=api_key,
                model="claude-3-sonnet-20240229",
                temperature=0.7
            )
        except Exception as e:
            st.error(f"Error initializing Anthropic client: {str(e)}")
            raise

    def validate_api_key(self) -> bool:
        try:
            self.chat_model.predict("test")
            return True
        except Exception as e:
            st.error(f"Invalid API key or API error: {str(e)}")
            return False

    def extract_pdf_content(self, pdf_file) -> Dict:
        try:
            content = {"text": "", "tables": [], "error": None}

            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content["text"] += text + "\n"

            if not content["text"].strip():
                raise ValueError("No readable text found in PDF")

            logger.info(f"Extracted text length: {len(content['text'])}")
            return content

        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return {"text": "", "tables": [], "error": str(e)}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def create_embeddings(self, text: str) -> Optional[FAISS]:
        try:
            if not text.strip():
                raise ValueError("Empty text provided")

            chunk_size = 500
            overlap = 50
            chunks = []

            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)

            logger.info(f"Created {len(chunks)} chunks")

            if not chunks:
                raise ValueError("No valid text chunks created")

            vector_store = FAISS.from_texts(
                chunks,
                self.embeddings
            )

            return vector_store

        except Exception as e:
            logger.error(f"Embedding creation error: {str(e)}")
            raise

def main():
    st.title("PDF Chat with Claude")

    api_key = 'YOUR Claude API-KEY'
    # if not api_key:
    #     st.warning("Please enter your Anthropic API key to continue.")
    #     return

    try:
        processor = PDFProcessor(api_key)

        if not processor.validate_api_key():
            st.error("Failed to validate Anthropic API key. Please check your key and try again.")
            return

        uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

        if uploaded_file:
            if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
                st.session_state.current_file = uploaded_file.name

                with st.spinner("Extracting text from PDF..."):
                    pdf_content = processor.extract_pdf_content(uploaded_file)

                    if pdf_content["error"]:
                        st.error(f"Error processing PDF: {pdf_content['error']}")
                        return

                    if not pdf_content["text"].strip():
                        st.error("No readable text found in the PDF.")
                        return

                    st.session_state.pdf_content = pdf_content

                with st.spinner("Creating vector store... This may take a moment."):
                    try:
                        vector_store = processor.create_embeddings(pdf_content["text"])
                        if vector_store:
                            st.session_state.vector_store = vector_store
                            st.success("PDF processed successfully!")
                        else:
                            st.error("Failed to create vector store - no vector store returned")
                    except RetryError:
                        st.error("Failed to create vector store after multiple attempts.")
                    except Exception as e:
                        st.error(f"Error creating vector store: {str(e)}")

            if st.session_state.vector_store:
                st.subheader("Ask questions about your PDF")
                query = st.text_input("Enter your question:")

                if query:
                    try:
                        results = st.session_state.vector_store.similarity_search(query, k=3)
                        context = "\n".join([result.page_content for result in results])

                        prompt = f"""Based on the following context, please answer the question.
                        Context: {context}
                        Question: {query}
                        Answer:"""

                        with st.spinner("Generating response..."):
                            response = processor.chat_model.predict(prompt)
                            st.write("Answer:", response)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
