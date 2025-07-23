import streamlit as st
import googletrans
import asyncio
import pdfplumber

# Initialize translation engine
translator = googletrans.Translator()

st.title("🌍 Multilingual Translator App")

# File upload option for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

text_input = ""

if uploaded_file is not None:
    try:
        with st.spinner("Extracting text from PDF..."):
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_input += text + "\n"

        if not text_input.strip():
            st.warning("No text found! Try uploading a text-based PDF.")
        else:
            st.text_area("Extracted Text from PDF:", text_input, height=200)

    except Exception as e:
        st.error(f"Error processing PDF: {e}")

# Manual text input
text_input = st.text_area("Or enter text to translate:", text_input)

# Language selection
languages = googletrans.LANGUAGES
lang_options = list(languages.values())
selected_lang = st.selectbox("Select target language:", lang_options)

# Get language code
lang_code = [code for code, name in languages.items() if name == selected_lang][0]

if st.button("Translate"):
    if text_input:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            translated_text = loop.run_until_complete(translator.translate(text_input, dest=lang_code))
            translated_text = translated_text.text  # Extract translated text
            st.success(f"Translated: {translated_text}")
        except Exception as e:
            st.error(f"Translation error: {e}")
    else:
        st.error("Please enter some text to translate or upload a PDF file.")
