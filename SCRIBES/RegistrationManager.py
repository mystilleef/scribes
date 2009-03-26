class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("register-object", self.__register_cb)
		self.__sigid2 = editor.connect("unregister-object", self.__unregister_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from collections import deque
		self.__objects = deque()
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.imanager.unregister_editor(self.__editor)
		self.__editor.window.destroy()
		del self.__editor
		del self
		self = None
		return False

	def __register(self, _object):
		self.__objects.append(_object)
		return False

	def __unregister(self, _object):
		self.__objects.remove(_object)
		if not self.__objects: self.__destroy()
		return False
	
	def __register_cb(self, editor, _object):
		self.__register(_object)
		return False
	
	def __unregister_cb(self, editor, _object):
		self.__unregister(_object)
		return False
