class Initializer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		self.__sigid1 = manager.connect("restart", self.__restart_cb)
		self.__start()

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __start(self):
		from gobject import spawn_async
		from SCRIBES.Globals import python_path
		python = self.__get_python_executable()
		folder = self.__get_save_process_folder()
		module = self.__get_save_process_executable(folder)
		spawn_async([python, module, python_path], working_directory=folder)
		return False

	def __get_python_executable(self):
		from sys import prefix
		return prefix + "/bin" + "/python"

	def __get_save_process_folder(self):
		from os.path import join, split
		SCRIBES_folder = split(split(globals()["__file__"])[0])[0]
		return join(SCRIBES_folder, "SaveSystem/ExternalProcess")

	def __get_save_process_executable(self, folder):
		from os.path import join
		return join(folder, "ScribesSaveProcess.py")

	def __restart_cb(self, *args):
		self.__start()
		return False
