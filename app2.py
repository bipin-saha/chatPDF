import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import urllib
import warnings
from pathlib import Path as p
from pprint import pprint
from text_ext import extract_text_from_pdf
import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import streamlit as st

import warnings

# Filter out LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=Warning)
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
#print(GOOGLE_API_KEY)



chat_model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY, temperature=0.2,convert_system_message_to_human=True)

st.set_page_config(page_title="Gemini ChatPDF Langchain Application", layout="wide")
question = st.chat_input(key="input", placeholder="Ask your question")


pdf_file_path = "Uploaded\paper.pdf"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
context = extract_text_from_pdf(pdf_file_path)
#context = "No more today"
context = "\n\n"+context
#print(context)
texts = text_splitter.split_text(context)
#print(len(texts))

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

if question:
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})
    related_docs = vector_index.get_relevant_documents(question)

    prompt_template = """
        Answer the question with full detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, try to answer it from your knowledge but don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Response:
            """
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(chat_model, chain_type="stuff", prompt=prompt)
    response = chain({"input_documents":related_docs, "question": question}, return_only_outputs=True)
    
#question = "Describe the Multi-head attention layer in detail?"

    result = response
    st.write(result["output_text"])
