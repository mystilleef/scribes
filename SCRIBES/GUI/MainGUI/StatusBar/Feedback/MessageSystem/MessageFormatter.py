from SCRIBES.SignalConnectionManager import SignalManager

class Formatter(SignalManager):
	"""
	This class generates a marked up string and an image id for the image that will be shown in
	the message bar.
	"""

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "format-feedback-message", self.__format_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from gtk import stock_list_ids
		self.__image_ids = [name[4:] for name in stock_list_ids()]
		self.__scribes_image_ids = ("error", "pass", "fail", "scribes", "busy", "run")
		self.__image_dictionary = self.__map_scribes_ids()
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __format(self, data):
		message, image_id, color, bold, italic, show_bar = data
		message = self.__markup((message, color, bold, italic))
		image_id = self.__get_gtk_image_id_from(image_id)
		self.__manager.emit("update-message-bar", (message, image_id, show_bar))
		return False

	def __markup(self, data):
		message, color, bold, italic = data
		if not message: return ""
		if color: message = "<span foreground='%s'>%s</span>" % (color, message)
		if bold: message =  "<b>%s</b>" % message
		if italic: message = "<i>%s</i>" % message
		return message

	def __get_gtk_image_id_from(self, image_id):
		if not image_id: return ""
		dictionary = self.__image_dictionary
		image = "gtk-%s" % image_id if image_id in self.__image_ids else dictionary[image_id]
		return image

	def __map_scribes_ids(self):
		dictionary = {"error": "gtk-dialog-error", "pass": "gtk-yes", "fail": "gtk-no",
		"scribes":"scribes", "busy": "gtk-execute", "run": "gtk-execute"}
		return dictionary

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __format_cb(self, manager, data):
#		self.__remove_timer()
#		from gobject import idle_add, PRIORITY_LOW
#		self.__timer = idle_add(self.__format, data, priority=PRIORITY_LOW)
		self.__format(data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
