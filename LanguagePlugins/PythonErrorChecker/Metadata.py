from SCRIBES.Utils import open_storage
STORAGE_FILE = "PythonErrorCheckType.dict"
KEY = "more_error_checks"

def get_value():
	try:
		value = True
		storage = open_storage(STORAGE_FILE)
		value = storage[KEY]
	except:
		pass
	return value

def set_value(value):
	storage = open_storage(STORAGE_FILE)
	storage[KEY] = value
	return
