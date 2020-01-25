import os 
import sys
import shutil

from flask import request, Flask, jsonify, render_template
from PIL import Image 
import pytesseract  
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from tesseract import *
from nltk_process import get_analysis
from github_process import github_analysis

upload_file = './upload_files'
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		PDF_file = secure_filename(file.filename)
		file.save(os.path.join('./upload_files/', PDF_file))
		file_path = './upload_files/' + PDF_file
		pages = convert_from_path(PDF_file, 500) 
		image_counter = 1
		os.mkdir("./out_files")
		
		for page in pages: 
			filename = "./out_files/page_"+str(image_counter)+".jpg"
			page.save(filename, 'JPEG')  
			image_counter = image_counter + 1

		filelimit = image_counter-1
		outfile = "./out_files/out_text.txt"
		fout = open(outfile, "a") 
		
		for itr in range(1, filelimit + 1): 
			filename = "./out_files/page_"+str(itr)+".jpg"
			text = str(((pytesseract.image_to_string(Image.open(filename)))))
			text = text.replace('-\n', '')
			fout.write(text)
		
		fout.close()
		analysis = get_analysis(outfile)
		analysis['repository'] = github_analysis(analysis['github_username'])
		shutil.rmtree('./out_files')
		return analysis

	return render_template('upload.html')


if __name__ == '__main__':
	app.run()