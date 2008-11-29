from gettext import gettext as _

class Processor(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("extracted-text", self.__extract_cb)
		self.__sigid3 = manager.connect("case", self.__case_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__case_type = None
		return 

	def __send_string(self, string):
		if self.__case_type == "toggle": self.__case_type = "lower" if string.isupper() else "upper"
		umessage = _("Converted '%s' to upper case") % string
		lmessage = _("Converted '%s' to lower case") % string
		tmessage = _("Converted '%s' to title case") % string
		smessage = _("Converted '%s' to swap case") % string
		dictionary = {
			"upper": (string.upper, umessage),
			"lower": (string.lower, lmessage),
			"title": (string.title, tmessage),
			"swap": (string.swapcase, smessage),
		}
		self.__manager.emit("processed-text", dictionary[self.__case_type][0]())
		message = dictionary[self.__case_type][1]
		self.__editor.update_message(message, "pass")
		self.__case_type = None
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __extract_cb(self, manager, string):
		self.__send_string(string)
		return False

	def __case_cb(self, manager, case):
		self.__case_type = case
		return False
