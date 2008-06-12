class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid3 = manager.connect("show-add-dialog", self.__show_add_dialog_cb)
		self.__sigid4 = manager.connect("dialog-hide-window", self.__hide_cb)
		self.__sigid5 = manager.connect("trigger-selected", self.__trigger_selected_cb)
		self.__sigid6 = manager.connect_after("show-edit-dialog", self.__show_edit_dialog_cb)
		self.__sigid7 = manager.connect("template-selected", self.__template_selected_cb)
		self.__sigid8 = manager.connect("process", self.__process_cb)
		self.__entry.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.dglade.get_widget("NameEntry")
		self.__trigger = ""
		self.__language = ""
		self.__is_edit_dialog = False
		return

	def __background_color(self, color="Normal"):
		return False

	def __validate_trigger(self):
		text = self.__entry.get_text()
		from utils import is_valid_trigger, is_duplicate_trigger
		valid = is_valid_trigger(text)
		self.__manager.emit("valid-trigger", valid)
		if self.__is_edit_dialog: return False
		key = self.__language.strip() + "|" + text.strip()
		duplicate = is_duplicate_trigger(key)
		if duplicate: self.__manager.emit("valid-trigger", False)
		return False

	def __send_trigger_info(self):
		text = self.__entry.get_text()
		self.__manager.emit("process-1", text)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__entry)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__validate_trigger()
		return False

	def __show_add_dialog_cb(self, *args):
		self.__entry.grab_focus()
		return False

	def __show_edit_dialog_cb(self, *args):
		self.__is_edit_dialog = True
		self.__entry.set_text(trigger)
		self.__entry.grab_focus()
		return

	def __hide_cb(self, *args):
		self.__entry.set_text("")
		self.__is_edit_dialog = False
		return False

	def __trigger_selected_cb(self, manager, trigger):
		self.__trigger = trigger
		return False

	def __template_selected_cb(self, manager, data):
		self.__language = data[0]
		return False

	def __process_cb(self, *args):
		self.__send_trigger_info()
		return False

