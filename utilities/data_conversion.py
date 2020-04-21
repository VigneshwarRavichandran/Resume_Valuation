from datetime import datetime
from datetime import timedelta  

def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    if isinstance(data, list):
        return list(map(convert, data))

    return data

def convert_timestamp(datetime_str):
	start_datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
	end_datetime_obj = start_datetime_obj + timedelta(minutes=120)
	start_datetime = start_datetime_obj.strftime("%Y-%m-%dT%H:%M:%S")
	end_datetime = end_datetime_obj.strftime("%Y-%m-%dT%H:%M:%S")
	return start_datetime, end_datetime 