from SCRIBES.Utils import open_storage
STORAGE_FILE = "ForkScribes.dict"
KEY = "fork_scribes"

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
