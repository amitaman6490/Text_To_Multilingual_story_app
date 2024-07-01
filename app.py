import streamlit as st
from gtts import gTTS
import os
import base64 
from PyPDF2 import PdfReader
import openai

# Set up your API key
openai.api_key = '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'

def translate_text(text, dest_language):
    # Map the language code to the language name
    language_map = {
        'bn': 'Bengali',
        'gu': 'Gujarati',
        'hi': 'Hindi',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ur': 'Urdu',
        'fr': 'French',
        'es': 'Spanish',
        'ca': 'Catalan',
        'gl': 'Galician',
        'eu': 'Basque',
        'zh-CN': 'Chinese Simplified',
        'zh-TW': 'Chinese Traditional',
        # Add more languages here
    }
    language = language_map.get(dest_language)

    # Construct the prompt
    prompt = f"Translate the following English text to {language}: {text}"

    # Make the API request
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the translated text from the response
    translated_text = response['choices'][0]['message']['content']

    return translated_text


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")

def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title('Multilingual Storytelling with Accents')

    text = ""

    input_option = st.selectbox("Choose an input option", ["Enter text", "Upload a file"])

    if input_option == "Enter text":
        text = st.text_input("Enter your text here", "Hello, world!")
    else:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                text = extract_pdf_text(uploaded_file)
            elif uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode()
            else:
                st.write("Unsupported file type")

    # Create a dictionary mapping countries to their languages
    country_languages = {
        'India': {
            #'Assamese': 'as',
            'Bengali': 'bn',
            'Gujarati': 'gu',
            'Hindi': 'hi',
            'Kannada': 'kn',
            #'Kashmiri': 'ks',
            #'Konkani': 'kok',
            #'Maithili': 'mai',
            'Malayalam': 'ml',
            'Marathi': 'mr',
            #'Odia': 'or',
            #'Punjabi': 'pa',
            #'Sanskrit': 'sa',
            #'Sindhi': 'sd',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Urdu': 'ur',
        },
        'France': {
            'French': 'fr',
        },
        'Spain': {
            'Spanish': 'es',
            'Catalan': 'ca',
            'Galician': 'gl',
            'Basque': 'eu',
        },
        'China': {
            'Chinese Simplified': 'zh-CN',
            'Chinese Traditional': 'zh-TW',
        },
        # Add more countries and their languages here
    }

    # User selects a country
    country = st.selectbox("Select a country", list(country_languages.keys()))

    # User selects a language from the selected country
    language_name = st.selectbox("Select a language", list(country_languages[country].keys()))

    # Get the language code from the dictionary
    language_code = country_languages[country][language_name]

    if st.button('Translate and Convert to Speech'):
        translated_text = translate_text(text, language_code)
        text_to_speech(translated_text, language_code)
        st.write(f"Translated Text ({language_name}): {translated_text}")
        st.markdown(get_binary_file_downloader_html('output.mp3', 'Download Audio'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
