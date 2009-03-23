class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("update-image", self.__update_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__id_dictionary = self.__map_scribes_ids()
		from gtk import stock_list_ids
		self.__stock_ids = stock_list_ids()
		self.__custom_ids = [name[4:] for name in self.__stock_ids]
		self.__scribe_ids = ("error", "pass", "fail", "scribes", "busy")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __map_scribes_ids(self):
		dictionary = {"error": "gtk-dialog-error", "pass": "gtk-yes", "fail": "gtk-no",
		"scribes":"scribes", "busy": "gtk-execute"}
		return dictionary

	def __update(self, image_id):
		try:
			if image_id in self.__custom_ids: raise ValueError
			if image_id in self.__scribe_ids: raise TypeError
		except ValueError:
			image_id = "gtk-" + image_id
		except TypeError:
			image_id = self.__id_dictionary[image_id]
		finally:
			self.__manager.emit("set-image", image_id)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, image_id):
		from gobject import idle_add
		idle_add(self.__update, image_id, priority=9999)
		return False
