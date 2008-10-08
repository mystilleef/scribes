from gettext import gettext as _

class Label(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validate", self.__validate_cb)
		self.__sigid3 = manager.connect("validation-error", self.__error_cb)
		self.__sigid4 = manager.connect("create", self.__create_cb)
		self.__sigid5 = manager.connect("validation-pass", self.__pass_cb)
		self.__sigid6 = manager.connect("creation-error", self.__error_cb)
		self.__sigid7 = manager.connect("creation-pass", self.__pass_cb)
		self.__sigid8 = manager.connect("hide-newfile-dialog-window", self.__hide_cb)
		self.__set_label()
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.new_gui.get_widget("FeedbackLabel")
		return  
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		del self
		self = None
		return False

	def __set_label(self, message=None, bold=False, italic=False, color=None):
		try:
			if not message: raise ValueError
			if color: message = "<span foreground='%s'>" % color + message + "</span>"
			if bold: message =  "<b>" + message + "</b>"
			if italic: message = "<i>" + message + "</i>"
			self.__label.set_label(message)
		except ValueError:
			self.__label.set_label("")
		return False
	
	def __info_message(self, message):
		self.__set_label(message, False, True, "turquoise")
		return False
	
	def __error_message(self, message):
		self.__set_label(message, True, False, "red")
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __pass_cb(self, *args):
		self.__set_label()
		return False
	
	def __error_cb(self, manager, message):
		self.__error_message(message)
		return False
	
	def __validate_cb(self, *args):
		self.__info_message(_("Validating please wait..."))
		return False
	
	def __create_cb(self, *args):
		self.__info_message(_("Creating file please wait..."))
		return False
	
	def __hide_cb(self, *args):
		self.__set_label()
		return False
