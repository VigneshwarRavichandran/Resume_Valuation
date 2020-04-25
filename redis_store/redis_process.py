import redis

from utilities.data_conversion import convert

redis_store = redis.Redis()
redis_pipe = redis_store.pipeline()


def generate_language_score(repository):
	programming_languages = {}
	for repo in repository:
		programming_language = repo['repo_language'].lower()
		try:
			if programming_languages[programming_language] < 100:
				programming_languages[programming_language] += 10
		except:
			programming_languages[programming_language] = 10
	return programming_languages

def loading_data(data):
	redis_store.hset(data["email_id"], 'email_id', data["email_id"])
	redis_store.hset(data["email_id"], 'name', data["name"].upper())
	if data["phone_number"]:
		redis_store.hset(data["email_id"], 'phone', data["phone_number"])
	else:
		redis_store.hset(data["email_id"], 'phone', 'null')
	if data["github_username"]:
		redis_store.hset(data["email_id"], 'github_id', data["github_username"])
	else:
		redis_store.hset(data["email_id"], 'github_id', 'null')

	language_scores = []
	if "repository" in data:
		scores = generate_language_score(data["repository"])
		for language in scores:
			score = int(scores[language])
			language_scores.append({"language" : language, "score" : score})
			programming_language_score = data["programming_language_scores_dict"].get(language, 0)
			total_score = score + programming_language_score
			redis_store.zadd(language.lower(), {data["email_id"]: total_score})
		for programming_language in data["programming_language_scores_dict"]:
			if programming_language not in scores:
				redis_store.zadd(language.lower(), {data["email_id"]: data["programming_language_scores_dict"][programming_language]})
		return language_scores
	return None

def retrieve_data(data):
	email_ids = redis_store.zrevrange(
		data, 0, -1)
	return convert(email_ids)