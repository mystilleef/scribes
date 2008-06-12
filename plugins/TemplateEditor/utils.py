def is_valid_trigger(string):
	string = string.strip()
	if not string: return False
	chars = (" ", "\t", "(", "{", "<", "[", "=", ")", "}", ">", "]", "|")
	for char in string:
		if char in chars: return False
	return True

def is_duplicate_trigger(key):
	try:
		from Metadata import open_template_database
		database = open_template_database("r")
		value = database.has_key(key)
	finally:
		database.close()
	return value
