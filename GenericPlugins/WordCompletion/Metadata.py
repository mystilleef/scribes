from SCRIBES.Utils import open_storage
STORAGE_FILE = "ToggleWordCompletion.dict"
KEY = "enable_word_completion"

def get_value():
	try:
		value = True
		storage = open_storage(STORAGE_FILE)
		value = storage[KEY]
	except KeyError:
		pass
	return value

def set_value(value):
	storage = open_storage(STORAGE_FILE)
	storage[KEY] = value
	return
