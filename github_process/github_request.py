import requests
import json
import os

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

def github_analysis(username):
	url = "https://api.github.com/users/"+username+"/repos"
	req = requests.get(url, headers={"Authorization": "token {}".format(AUTH_TOKEN)})
	req_body = req.json()
	repository = []

	for repo in req_body:
		repo_name = repo['name']
		repo_language = repo['language']
		if all([repo_language, repo_name]):
			repository.append({
				"repo_name" : repo_name,
				"repo_language" : repo_language,
		 	})

	return repository