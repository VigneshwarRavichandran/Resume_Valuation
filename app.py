import os 
import sys
import shutil
import json

from flask import request, Flask, jsonify, render_template
from PIL import Image 
import pytesseract  
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from tesseract.tesseract_processing import *
from nltk_process.nltk_analysis import get_analysis
from github_process.github_request import github_analysis
from redis_store.redis_process import loading_data
from redis_store.redis_process import retrieve_data
from calendar_api.events_creation import create_event
from utilities.data_conversion import convert_timestamp

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
		if os.path.exists("./out_files"):
			shutil.rmtree('./out_files')
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
		if analysis['github_username']:
			analysis['repository'] = github_analysis(analysis['github_username'])
		shutil.rmtree('./out_files')
		analysis['github_language_scores'] = loading_data(analysis)
		print(analysis)
		return render_template('analysis.html', analysis=analysis)

	return render_template('upload.html')

@app.route('/retrieve', methods=['POST', 'GET'])
def retrieve():
	if request.method == 'POST':
		language = request.form['language']
		description = request.form['description']
		date_time = request.form['date_time']
		candidates = retrieve_data(language.lower())
		start_timestamp, end_timestamp = convert_timestamp(date_time)
		create_event(candidates, start_timestamp, end_timestamp, description)
		return "Invites send"

	return render_template('retrieve.html')


if __name__ == '__main__':
	app.run()