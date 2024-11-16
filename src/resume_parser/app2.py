from flask import Flask, render_template, request, jsonify
import os
import re
import nltk
from werkzeug.utils import secure_filename
from docx import Document
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_keywords(text):
    
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word for word in words if word not in stopwords.words('english')]

    
    counter = Counter(words)
    keywords = counter.most_common(10)  # Top 10 keywords
    return keywords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text based on file type
        if filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            return jsonify({"error": "Unsupported file type"})

        keywords = extract_keywords(text)
        return jsonify({"keywords": keywords})

if __name__ == '__main__':
    app.run(debug=True)
