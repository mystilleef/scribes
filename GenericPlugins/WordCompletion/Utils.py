def is_delimeter(text):
	if text.isalnum() or (text in ("_", "-")): return False
	return True
