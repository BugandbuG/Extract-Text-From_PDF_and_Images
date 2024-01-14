import pytesseract
from PIL import Image
import PyPDF2
from PyPDF2 import PdfReader
from PIL import Image
from flask import Flask, request, render_template
import os

def extract_text_from_pdf(pdf_path):
    # Convert PDF to image
    image = convert_pdf_to_image(pdf_path)

    # Extract text from image
    text = extract_text_from_image(image)

    return text

def convert_pdf_to_image(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)

        # Get the first page of the PDF
        page = pdf.pages[0]

        # Convert the page to an image
        image = page.to_image()

        # Return the image
        return image

def extract_text_from_image(image):
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)

    return text

# Example usage
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])  
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' not in request.files:
            return render_template('home.html', msg='No file selected')

        file = request.files['file']

        # Save the uploaded file
        if file.filename == '':
            return render_template('home.html', msg='No file selected')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Get the path of the saved file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        try: 
            # Extract text from PDF
            text = extract_text_from_pdf(file_path)
        except: 
            # Extract text from image
            text = extract_text_from_image(file_path)
        # Extract text from the uploaded file
        # text = extract_text_from_pdf(file_path)

        return render_template('home.html', text = text)
    return render_template('home.html')
if __name__ == '__main__':
    # app.config['UPLOAD_FOLDER'] = '/path/to/save/uploaded/files'

    # Create the upload folder if it doesn't exist
    
    
     
    app.run(debug=True)

