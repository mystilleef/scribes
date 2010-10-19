class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("fileinfo", self.__fileinfo_cb)
		self.__label.set_text("")

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.glade.get_widget("TypeLabel")
		return

	def __set_label(self, fileinfo):
		try:
			from gio import content_type_get_description as get_desc
			self.__label.set_text(get_desc(self.__editor.mimetype))
		except:
			self.__label.set_text("plain text document")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__label.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __fileinfo_cb(self, manager, fileinfo):
		from gobject import idle_add
		idle_add(self.__set_label, fileinfo)
		return False
