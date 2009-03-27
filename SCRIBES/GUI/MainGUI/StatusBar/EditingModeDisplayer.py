from gettext import gettext as _
INS = _("<b>INS</b>")
OVR = _("<b>OVR</b>")

class Displayer(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.textview.connect("toggle-overwrite", self.__overwrite_cb)
		self.__update_mode()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__label = editor.gui.get_widget("StatusInsertionType")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.textview)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update_mode(self):
		textview = self.__editor.textview
		set_label = self.__label.set_label
		self.__editor.response()
		set_label(OVR) if textview.get_overwrite() else set_label(INS)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __overwrite_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update_mode, priority=9999)
		return False
