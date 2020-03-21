import redis

from utilities import convert


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
	redis_store.hset(data["email_id"], 'phone', data["phone_number"])
	redis_store.hset(data["email_id"], 'email_id', data["name"])
	language_scores = generate_language_score(data["repository"])
	for language in language_scores:
		redis_store.zadd(language.lower(), {data["email_id"]: int(language_scores[language])})
	return language_scores

def retrieve_data(data):
	email_ids = redis_store.zrevrange(
		data, 0, 1)
	return convert(email_ids)