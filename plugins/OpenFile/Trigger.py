class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__open_dialog_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__remote_dialog_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__newfile_dialog_cb)
		editor.get_toolbutton("OpenToolButton").props.sensitive = True

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("show_open_dialog", "ctrl+o")
		self.__trigger2 = self.__create_trigger("show_remote_dialog", "ctrl+l")
		self.__trigger3 = self.__create_trigger("show_newfile_dialog", "ctrl+shift+o")
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		del self
		self = None
		return 

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __open_dialog_cb(self, *args):
		self.__get_manager().show_open_dialog()
		return False
	
	def __remote_dialog_cb(self, *args):
		self.__get_manager().show_remote_dialog()
		return False
	
	def __newfile_dialog_cb(self, *args):
		self.__get_manager().show_newfile_dialog()
		return False

	def destroy(self):
		self.__destroy()
		return
