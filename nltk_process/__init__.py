
import re
import nltk
import requests
import json

from nltk.corpus import stopwords
from nltk.corpus import names
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
from nltk import Tree
from fuzzywuzzy import fuzz

stop = stopwords.words('english')

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    phone_numbers = [re.sub(r'\D', '', number) for number in phone_numbers]
    valid_phone_numbers = []
    for number in phone_numbers:
        if len(number) == 10:
            valid_phone_numbers.append(number)
    if len(valid_phone_numbers) != 0:
        return valid_phone_numbers[0]
    return None

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)[0]

def extract_github_url(sentences):
    base_url = "https://github.com/"
    names = []
    urls = []
    for tagged_sentence in sentences:
        for chunk in tagged_sentence:
            try:
                if "github.com" in chunk[0]:
                    urls.append(chunk[0])
                if chunk[1] == "NNP":
                    names.append(chunk[0])
            except:
                pass
    name_dict = None
    has_found = False
    is_valid = False
    for url in urls:
        url_segments = url.split('/')
        username = url_segments[-1]
        req = requests.get(base_url+username)
        if req.status_code == requests.codes.ok:
            return username

    for name in names:
        if has_found:
            username = name
            req = requests.get(base_url+username)
            if req.status_code == requests.codes.ok:
                return username
        else:
            if "github" in name.lower():
                has_found = True

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(sentences, email):
    names = []
    email_name = email.split('@')
    email_name = email_name[0]
    for tagged_sentence in sentences:
        for chunk in tagged_sentence:
            try:
                if chunk[1] == "NNP":
                    names.append(chunk[0])
            except:
                pass
    name_dict = None
    for name in names:
        ratio = fuzz.ratio(email_name.lower(),name.lower())
        if name_dict:
            largest_ratio = name_dict[1]
            if ratio > largest_ratio:
                name_dict = [name, ratio]
        else:
            name_dict = [name, ratio]
    return name_dict[0]

def extract_languages(sentences):
    programming_language_scores = {}
    languages = []

    with open('./nltk_process/programming_languages.json') as pl_json_file:
        programming_languages_data = json.load(pl_json_file)

    with open('./nltk_process/languages.json') as l_json_file:
        languages_data = json.load(l_json_file)

    for tagged_sentence in sentences:
        for chunk in tagged_sentence:
            if chunk[0].lower() in programming_languages_data:
                try:
                    if programming_language_scores[chunk[0].lower()] < 100:
                        programming_language_scores[chunk[0].lower()] += 10
                except:
                    programming_language_scores[chunk[0].lower()] = 10
            if chunk[0].lower() in languages_data:
                languages.append(chunk[0].lower())

    return list(set(languages)), programming_language_scores

def get_analysis(filename):
    with open(filename, 'r') as file:
        document = file.read()
    
    sentences = ie_preprocess(document)
    number = extract_phone_numbers(document)
    email = extract_email_addresses(document)
    name = extract_names(sentences, email)
    github_username = extract_github_url(sentences)
    languages, programming_language_scores = extract_languages(sentences)

    return({
        "name" : name,
        "email_id" : email,
        "phone_number" : number,
        "programming_language_scores" : programming_language_scores,
        "languages" : languages,
        "github_username" : github_username
    })  