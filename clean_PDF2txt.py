import PyPDF2
import re

def clean_extracted_text(text):
    """Clean and preprocess extracted text."""
    # Remove chapter titles and sections
    text = re.sub(r'^(Introduction|Chapter \d+:|What is|Examples:|Chapter \d+)', '', text, flags=re.MULTILINE)
    text = re.sub(r'ctitious', 'fictitious', text)
    text = re.sub(r'ISBN[- ]13: \d{13}', '', text)
    text = re.sub(r'ISBN[- ]10: \d{10}', '', text)
    text = re.sub(r'Library of Congress Control Number : \d+', '', text)
    text = re.sub(r'(\.|\?|\!)(\S)', r'\1 \2', text)  # Ensure space after punctuation
    text = re.sub(r'All rights reserved|Copyright \d{4}', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # Remove all newlines and replace newlines only after periods
    text = text.replace('\n', ' ')
    text = re.sub(r'(\.)(\s)', r'\1\n', text)

    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + ' '  # Append text of each page
    return text

def main():
    pdf_path = 'The Rise and Potential of Large Language ModelBased Agents A Survey.pdf'  # Path to your PDF file
    extracted_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_extracted_text(extracted_text)

    # Output the cleaned text to a file
    with open('./cleaned_text_output.txt', 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

if __name__ == '__main__':
    main()