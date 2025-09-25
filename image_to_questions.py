from dotenv import load_dotenv
from openai import OpenAI
from pdf2image import convert_from_path
import base64
import os
import re

def initialize_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    return client

def scan_questions_page(client, questions_page_image):
    with open(questions_page_image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
        response = client.chat.completions.create (
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a math OCR assistant that converts scanned questions into Markdown with LaTeX."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract the math questions. Use Markdown and LaTeX for formulas."},
                    {"type": "image_url", "image_url": 
                        {"url": f"data:image/png;base64,{img_b64}"}}
                ]}
            ]
        )
    return response.choices[0].message.content

def convert_scanned_text_to_questions(scanned_text, output_file):
    pattern = r'(?m)^\d.*(?:\n^(?!\d).*|\n)*(?=\n\d|\Z)'
    matches = re.findall(pattern, scanned_text)
    with open(output_file, 'w') as of:
        for match in matches:
            question = ' '.join(match.splitlines())
            of.writelines(question)
            of.write('\n')

if __name__ == '__main__':
    client = initialize_openai_client()
    print("Initialized OpenAI client.")
    input_file = 'images/jee_mains_page_3.jpg'
    output_file = 'output/jee_mains_page_3.md'
    scanned_text = scan_questions_page(client, input_file)
    print(f'Retrieved scanned_text from image file {input_file}')
    convert_scanned_text_to_questions(scanned_text, output_file)
    print(f'Stored questios to file {output_file}')