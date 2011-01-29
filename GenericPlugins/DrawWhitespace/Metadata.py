from SCRIBES.Utils import open_storage
STORAGE_FILE = "ToggleDrawWhiteSpaces.dict"
KEY = "toggle_white_spaces"

def get_value():
	try:
		value = False
		storage = open_storage(STORAGE_FILE)
		value = storage[KEY]
	except KeyError:
		pass
	return value

def set_value(value):
	storage = open_storage(STORAGE_FILE)
	storage[KEY] = value
	return
