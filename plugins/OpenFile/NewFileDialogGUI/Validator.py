from gettext import gettext as _

class Validator(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validate", self.__validate_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __valid_name(self, name):
		if len(name) > 256: return False
		if "/" in name: return False
		return True
	
	def __exists(self, name):
		from gnomevfs import exists
		uri_folder = str(self.__editor.uri_object.parent) if self.__editor.uri else self.__editor.desktop_folder_uri
		from os.path import join
		uri = join(uri_folder, name)
		if exists(uri): return True
		return False

	def __validate(self, name):
		try:
			from Exceptions import NoNameError, InvalidNameError, FileExistError
			if not name: raise NoNameError
			if self.__valid_name(name) is False: raise InvalidNameError
			if self.__exists(name): raise FileExistError
			self.__manager.emit("validation-pass")
		except NoNameError:
			self.__manager.emit("validation-error", "")
		except InvalidNameError:
			self.__manager.emit("validation-error", _("Error: Invalid file name"))
		except FileExistError:
			self.__manager.emit("validation-error", _("Error: File already exists"))
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __validate_cb(self, manager, name):
		self.__validate(name)
		return False
