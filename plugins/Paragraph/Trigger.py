class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__view.connect("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__manager = None 
		self.__trigger1 = self.__create_trigger("next_paragraph", "alt+Right")
		self.__trigger2 = self.__create_trigger("previous_paragraph", "alt+Left")
		self.__trigger3 = self.__create_trigger("reflow_paragraph", "alt+q")
		return

	def __destroy(self):
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		self.__editor.disconnect_signal(self.__sigid4, self.__view)
		self.__editor.remove_triggers(triggers)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return

	def __get_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, trigger):
		if not self.__manager: self.__manager = self.__get_manager()
		function = {
			self.__trigger1: self.__manager.next_paragraph,
			self.__trigger2: self.__manager.previous_paragraph,
			self.__trigger3: self.__manager.reflow_paragraph,
		}
		function[trigger]()
		return False

	def destroy(self):
		self.__destroy()
		return

	def __popup_cb(self, *args):
	#	from PopupMenuItem import PopupMenuItem
	#	self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False
