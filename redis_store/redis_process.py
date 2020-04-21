import redis

from utilities.data_conversion import convert


redis_store = redis.Redis(host='localhost')
redis_pipe = redis_store.pipeline()


def generate_language_score(repository):
	programming_languages = {}
	for repo in repository:
		programming_language = repo['repo_language']
		try:
			programming_languages[programming_language] += 1
		except:
			programming_languages[programming_language] = 1
	return programming_languages

def loading_data(data):
	redis_store.hset(data["email_id"], 'email_id', data["email_id"])
	redis_store.hset(data["email_id"], 'email_id', data["name"])
	if data["phone_number"]:
		redis_store.hset(data["email_id"], 'phone', data["phone_number"])
	else:
		redis_store.hset(data["email_id"], 'phone', 'null')
	language_scores = []
	if "repository" in data:
		scores = generate_language_score(data["repository"])
		for language in scores:
			score = int(scores[language])
			language_scores.append({"language" : language, "score" : score})
			redis_store.zadd(language.lower(), {data["email_id"]: score})
		return language_scores
	return None

def retrieve_data(data):
	email_ids = redis_store.zrevrange(
		data, 0, 1)
	return convert(email_ids)