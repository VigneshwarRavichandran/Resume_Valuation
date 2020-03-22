import os 
import sys
import shutil
import json

from flask import request, Flask, jsonify, render_template
from PIL import Image 
import pytesseract  
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from tesseract import *
from nltk_process import get_analysis
from github_process import github_analysis
from redis_store import loading_data
from redis_store import retrieve_data
from calendar_api import create_event
from utilities import convert_timestamp

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
		analysis['language_scores'] = loading_data(analysis)
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

@app.route('/test', methods=['POST', 'GET'])
def test():
	if request.method == 'GET':
		analysis = {'name': 'VIGNESHWAR', 'email_id': 'vigneshwarravichandran@gmail.com', 'phone_number': '9962190989', 'github_username': 'VigneshwarRavichandran', 'repository': [{'repo_name': '100DaysOfCode', 'repo_language': 'Python'}, {'repo_name': 'Chat_bot', 'repo_language': 'Python'}, {'repo_name': 'DataStructures', 'repo_language': 'Python'}, {'repo_name': 'dept-website', 'repo_language': 'HTML'}, {'repo_name': 'Django-Basics', 'repo_language': 'Python'}, {'repo_name': 'Django-Test', 'repo_language': 'Python'}, {'repo_name': 'Feedback_System', 'repo_language': 'Python'}, {'repo_name': 'Feedback_System_REST', 'repo_language': 'Python'}, {'repo_name': 'Flask-test', 'repo_language': 'Python'}, {'repo_name': 'Gmail_api', 'repo_language': 'Python'}, {'repo_name': 'griddb_nosql', 'repo_language': 'C++'}, {'repo_name': 'hugo-lodi-theme', 'repo_language': 'HTML'}, {'repo_name': 'JSON_Merger', 'repo_language': 'Python'}, {'repo_name': 'JWT_flask', 'repo_language': 'Python'}, {'repo_name': 'Leave-Management-Bot', 'repo_language': 'Python'}, {'repo_name': 'logics', 'repo_language': 'Python'}, {'repo_name': 'login_system', 'repo_language': 'Python'}, {'repo_name': 'login_system-django-', 'repo_language': 'Python'}, {'repo_name': 'MadStreetDen_task', 'repo_language': 'Python'}, {'repo_name': 'Movie_recommendation', 'repo_language': 'Python'}, {'repo_name': 'My-blog', 'repo_language': 'HTML'}, {'repo_name': 'My_website', 'repo_language': 'CSS'}, {'repo_name': 'pdf_converter', 'repo_language': 'Python'}, {'repo_name': 'python', 'repo_language': 'Python'}, {'repo_name': 'Question_paper_generator', 'repo_language': 'Python'}, {'repo_name': 'restaurant_bot', 'repo_language': 'Python'}, {'repo_name': 'Resume_Valuation', 'repo_language': 'Python'}, {'repo_name': 'send_recieve_msg', 'repo_language': 'Python'}], 'language_scores': [{'language': 'Python', 'score': 23}, {'language': 'HTML', 'score': 3}, {'language': 'C++', 'score': 1}, {'language': 'CSS', 'score': 1}]}
		return render_template('analysis.html', analysis=analysis)


if __name__ == '__main__':
	app.run()