DBUS_SERVICE = "org.sourceforge.ScribesPythonErrorChecker"
DBUS_PATH = "/org/sourceforge/ScribesPythonErrorChecker"

def file_has_changed(file_path, modification_time):
	from SCRIBES.Utils import get_modification_time
	modtime = get_modification_time(file_path)
	return modtime != modification_time

def validate_session(file_path, stale_session, editor_id, session_id, modification_time):
	from Exceptions import StaleSessionError, FileChangedError
	if editor_id in stale_session and session_id in stale_session: raise StaleSessionError
	if file_has_changed(file_path, modification_time): raise FileChangedError
	return

def update_python_environment_with(module_path):
	from os.path import dirname
	module_folder = dirname(module_path)
	from sys import path
	if not (module_folder in path): path.insert(0, module_folder)
	from os import environ, pathsep, putenv
	python_path = pathsep.join(path)
	environ["PYTHONPATH"] = python_path
	putenv("PYTHONPATH", python_path)
	return

def reformat_error(message):
	message = message.strip(" \t\n\r").split()
	strings = [string for string in message if string.strip(" \t\n\r")]
	message = " ".join(strings)
	return message
