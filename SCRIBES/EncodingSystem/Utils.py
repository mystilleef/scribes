def format_encoding(encoding):
	utf8_encodings = ("utf-8", "utf8", "UTF8", "UTF-8", "Utf-8", None)
	if encoding in utf8_encodings: return "utf-8"
	return encoding.strip().lower()
