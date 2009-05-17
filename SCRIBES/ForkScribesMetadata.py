from Utils import open_database
basepath = "/Preferences/ForkScribes.gdb"

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["fork"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(fork):
	try:
		database = open_database(basepath, "w")
		database["fork"] = fork
	finally:
		database.close()
	return
