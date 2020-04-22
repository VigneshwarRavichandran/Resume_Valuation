import redis

from models.tables import Candidates, Languages
from models.tables import engine, Base, session
from utilities.data_conversion import convert

redis_store = redis.Redis()
redis_keys = redis_store.keys()

for key in redis_keys:
	if "@" in str(key):
		candidate_details = redis_store.hgetall(key)
		candidate_details = convert(candidate_details)
		candidate = session.query(Candidates).filter_by(email_id=candidate_details['email_id']).first()
		if not candidate:
			candidate = Candidates(name=candidate_details['name'], email_id=candidate_details['email_id'], github_id=candidate_details['github_id'], phone_no=candidate_details['phone'])
			session.add(candidate)
			session.commit()

for key in redis_keys:
	if "@" not in str(key):
		email_ids = redis_store.zrevrange(key, 0, -1)
		for email_id in email_ids:
			email_id = convert(email_id)
			candidate = session.query(Candidates).filter_by(email_id=email_id).first()
			language = session.query(Languages).filter_by(candidate_id=candidate.id, name=convert(key)).first()
			if not language:
				language = Languages(name=convert(key), candidate_id=candidate.id)
				session.add(language)
				session.commit()
