import streamlit as st
import os
import google.generativeai as genai
from text_ext import extract_text_from_pdf
import base64
from dotenv import load_dotenv
from chat_mode import chat_response
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

text_model=genai.GenerativeModel("gemini-pro")
vision_model=genai.GenerativeModel("gemini-pro-vision") 
chat = text_model.start_chat(history=[])

def get_gemini_response(input, pdf_content):
    response = text_model.generate_content([input, pdf_content])
    return response.text

def get_gemini_vision_response(input, image, pdf_content):
    response = vision_model.generate_content([input, image, pdf_content])
    return response.text

##initialize our streamlit app
st.set_page_config(page_title="Gemini ChatPDF Application", layout="wide")
#st.subheader("Chat with PDF")
# Add some space at the top to center the subheader
#st.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>chatPDF</h2>", unsafe_allow_html=True)



with st.sidebar:
        st.title("Upload PDF:")
        research_field = st.text_input("Research Field: ",key="research_field", placeholder="Enter research fields with commas")
        uploaded_file = st.file_uploader("", type=["pdf"])
        option = st.selectbox('Select Mode', ('', 'Chat', 'Graph and Table', 'Code', 'Custom Prompting'))
        #print(option)
        #submit = st.button("Submit", type="primary")
        #submit1 = st.button("Resume Assesmet")
        #submit2 = st.button("Possible Improvements")
        #submit3 = st.button("Percentage Match")

if uploaded_file is None:
    st.stop()
else:   
    file_path = os.path.join("Uploaded", "paper.pdf")
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    


q_input=st.chat_input(key="input", placeholder="Ask your question")
#ask=st.button("Ask", type="primary")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
   
    else:
        raise FileNotFoundError("No file uploaded")


pdf_file_path = "Uploaded/paper.pdf"

if uploaded_file:
    pdf_text = extract_text_from_pdf(pdf_file_path)
    #print(pdf_text)
else:
    pdf_text = ""


initial_prompt = f"""
Imagine you are a seasoned researcher specializing in the field of {research_field}. 
You are presented with a research paper within your domain. Evaluate its working methodology 
and discuss its research impact through concise bullet points. Conclude by summarizing the 
research paper and propose three questions for the user based on the paper's context. Finnaly 
remeber the research paper context for the next questions.

Output will be as,
Research Paper Title \n
Research Summary \n
Methodology \n
Research Impact \n
Suggested Questions"""


if option=='':
    with st.spinner("Processing..."):
        response = get_gemini_response(initial_prompt, pdf_text)
        st.write(response)
    


question_prompt = f"""Envision yourself as a seasoned researcher with a wealth of knowledge in the {research_field} domain. 
        Upon being presented with a research paper within your specialized area, meticulously evaluate its methodology. 
        Provide detailed and contextual insights in response to my specific question or questions. Ensure your answers are 
        not only accurate but also comprehensive. In instances where the information is unavailable, please explicitly state, 
        'Sorry, I do not know the answer.' \n \n \n"""

intermediate_code_prompt = f"""Envision yourself as a seasoned researcher with a welth of knowledge in the {research_field} domain.
        Upon being presented with a research paper within your specialized area, meticulosly evaluate its methodology and detail working
        process. Provide detailed and contextual step by step informations for developing the complete project from scratch including models, 
        architectures, conversion process and related items mentioned in the document text"""

code_prompt = f"""As a proficient Python code generator specialized in {research_field}, 
        your expertise encompasses various aspects of research, including model construction,  developing task-specific 
        functions, exploring novel methods, and generating code for existing works. Additionally, you are exceled in 
        creating insightful visualizations, utilizing statistical data, such as bar graphs, pie charts, histograms, and
        scatter plots, to convey meaningful insights within the context of research data. Now, based on my question or
        specific inquiry regarding the given research paper data, please generate the relevant Python code to address my query. Finally
        explain the code in by each and every steps. \n \n \n"""

if q_input is None:
    st.stop()
else:
    if q_input and option=="Chat":
        with st.spinner("Processing..."):
            mod_prompt = question_prompt + pdf_text
            response = get_gemini_response(mod_prompt, q_input)
            chat_response(q_input, response)
            #st.write(response)
    
    elif q_input and option=="Code":

        with st.spinner("Processing..."):
            mod_prompt = intermediate_code_prompt + pdf_text
            response = get_gemini_response(mod_prompt, q_input)
            st.write(response)
            #mod_prompt = code_prompt + response
            #response = get_gemini_response(mod_prompt, q_input)
            #st.write(response)

    elif q_input and option=="Graph and Table":
        with st.spinner("Processing..."):
            #mod_prompt = code_prompt + pdf_text
            #response = get_gemini_response(mod_prompt, q_input)
            st.write("Graph and Table mode is not developed yet.")

    elif q_input and option == "Custom Prompting":
        mod_prompt = q_input
        response = get_gemini_response(mod_prompt, pdf_text)
        st.write(response)
    
    else:
        st.write(f"{option} Mode")



