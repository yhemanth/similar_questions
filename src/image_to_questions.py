from dotenv import load_dotenv
from openai import OpenAI
from pdf2image import convert_from_path
import base64
import os
import re
import sys

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
                {"role": "system", "content": 
                        """Extract the math questions. Use Markdown and LaTeX for formulas.
                        Mark the start of every question with a token '<start>' and end of every question with '<end>'.
                        Extract all questions. Do not skip any, even if they look incomplete, unclear.
                        If something resembles a question, include it.
                        Some of the questions have multiple choices numbered (a), (b), (c) and so on.
                        Include those as well, wherever they are visible.
                        Your output must have the same number of <start>…<end> blocks as the number of questions visible in the input."""
                 },
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract the math questions. Use Markdown and LaTeX for formulas."},
                    {"type": "image_url", "image_url": 
                        {"url": f"data:image/png;base64,{img_b64}"}}
                ]}
            ]
        )
    return response.choices[0].message.content

def convert_scanned_text_to_questions(scanned_text, output_file):
    pattern = r'<start>(.*?)<end>'
    matches = re.findall(pattern, scanned_text, flags=re.DOTALL)
    with open(output_file, 'w') as of:
        print(f'Found {len(matches)} post scan.')
        for match in matches:
            question = ' '.join(match.splitlines())
            of.writelines(question)
            of.write('\n')

if __name__ == '__main__':

    if (len(sys.argv) < 3):
        print(f"Usage: python {os.path.basename(__file__)}  <inputfile> <outputfile>")
        sys.exit(1)

    client = initialize_openai_client()
    print("Initialized OpenAI client.")
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    scanned_text = scan_questions_page(client, input_file)
    print(f'Retrieved scanned_text from image file {input_file}')
    convert_scanned_text_to_questions(scanned_text, output_file)
    print(f'Stored questions to file {output_file}')