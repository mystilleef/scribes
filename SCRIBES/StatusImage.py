class Image(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid4 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid5 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid6 = editor.connect("save-error", self.__save_error_cb)
		self.__sigid7 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid8 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid9 = editor.connect("update-message", self.__update_message_cb)
		self.__sigid10 = editor.connect("set-message", self.__set_message_cb)
		self.__sigid11 = editor.connect("unset-message", self.__unset_message_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		from collections import deque
		self.__editor = editor
		self.__busy = False
		self.__queue = deque([])
		self.__image = editor.gui.get_widget("StatusImage")
		from gtk import stock_list_ids
		self.__id_dictionary = self.__map_scribes_ids()
		self.__stock_ids = stock_list_ids()
		self.__custom_ids = [name[4:] for name in self.__stock_ids]
		self.__scribe_ids = ("error", "pass", "fail", "scribes", "busy")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return 

	def __set_image(self, image_name):
		try:
			if image_name in self.__custom_ids: raise ValueError
			if image_name in self.__scribe_ids: raise TypeError
		except ValueError:
			image_name = "gtk-" + image_name
		except TypeError:
			image_name = self.__id_dictionary[image_name]
		finally:
			from gtk import ICON_SIZE_MENU
			self.__image.set_from_icon_name(image_name, ICON_SIZE_MENU)
			self.__image.show()
		return False

	def __set_default_image(self):
		try:
			if self.__queue: raise ValueError
			if not self.__editor.uri: raise TypeError
			self.__set_image("edit") if self.__editor.modified else self.__set_image("new")
		except ValueError:
			self.__set_image(self.__queue[-1])
		except TypeError:
			self.__image.hide()
		finally:
			self.__busy = False
		return False

	def __update_message_image(self, icon_name, time=5):
		self.__busy = True
		self.__set_image(icon_name)
		from gobject import timeout_add
		timeout_add(time*1000, self.__set_default_image, priority=9999)
		return False

	def __set_message_image(self, icon_name):
		self.__queue.append(icon_name)
		self.__set_image(icon_name)
		return False

	def __unset_message_image(self, icon_name):
		try:
			self.__queue.remove(icon_name)
		except ValueError:
			pass
		if self.__busy: return False
		from gobject import idle_add
		idle_add(self.__set_default_image, priority=9999)
		return False

	def __map_scribes_ids(self):
		dictionary = {"error": "gtk-dialog-error", "pass": "gtk-yes", "fail": "gtk-no",
		"scribes":"scribes", "busy": "gtk-execute"}
		return dictionary

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_file_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__set_message_image, "busy", priority=9999)
		return False

	def __loaded_file_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__update_message_image, "gtk-open", priority=9999)
		idle_add(self.__unset_message_image, "busy", priority=9999)
		return False

	def __saved_file_cb(self, *args):
		if self.__busy: return False
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__update_message_image, "gtk-save", 3, priority=9999)
		return False

	def __modified_file_cb(self, *args):
		if self.__busy: return False
		from gobject import idle_add
		self.__timer = idle_add(self.__set_default_image, priority=9999)
		return False

	def __save_error_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__update_message_image, "error", priority=9999)
		return False

	def __load_error_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__update_message_image, "error", priority=9999)
		idle_add(self.__unset_message_image, "busy", priority=9999)
		return False

	def __readonly_cb(self, *args):
		return False

	def __update_message_cb(self, editor, message, icon_name, time):
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__update_message_image, icon_name, time, priority=9999)
		return False

	def __set_message_cb(self, editor, message, icon_name):
		from gobject import idle_add
		idle_add(self.__set_message_image, icon_name, priority=9999)
		return False

	def __unset_message_cb(self, editor, message, icon_name):
		from gobject import idle_add
		idle_add(self.__unset_message_image, icon_name, priority=9999)
		return False
