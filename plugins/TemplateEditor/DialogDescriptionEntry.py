class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("dialog-hide-window", self.__hide_cb)
		self.__sigid3 = manager.connect("description-selected", self.__description_selected_cb)
		self.__sigid4 = manager.connect("show-edit-dialog", self.__show_edit_dialog_cb)
		self.__sigid5 = manager.connect("valid-trigger", self.__validate_trigger_cb)
		self.__sigid6 = manager.connect("process-1", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.dglade.get_widget("DescriptionEntry")
		self.__description = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_edit_dialog_cb(self, *args):
		self.__entry.set_text(self.__description)
		return False

	def __hide_cb(self, *args):
		self.__entry.set_text("")
		return False

	def __description_selected_cb(self, manager, description):
		self.__description = description
		return False

	def __validate_trigger_cb(self, manager, sensitive):
		self.__entry.set_property("sensitive", sensitive)
		return False

	def __process_cb(self, manager, name):
		description = self.__entry.get_text()
		self.__manager.emit("process-2", (name, description))
		return False

