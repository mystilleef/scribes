class Extractor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marks", self.__marks_cb)
		
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

	def __send_string(self, marks):
		start = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		string = self.__editor.textbuffer.get_text(start, end)
		self.__manager.emit("extracted-text", string)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marks_cb(self, manager, marks):
		self.__send_string(marks)
		return False
