class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__editor.textview.connect("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("togglecase", "alt+u")
		self.__trigger2 = self.__create_trigger("titlecase", "alt+shift+u")
		self.__trigger3 = self.__create_trigger("swapcase", "alt+shift+l")
		return

	def __destroy(self):
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3,)
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		del self
		self = None
		return False

	def __create_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, trigger):
		if self.__manager is None: self.__manager = self.__create_manager()
		triggers = {"togglecase": self.__manager.toggle,
					"titlecase": self.__manager.title,
					"swapcase": self.__manager.swap}
		triggers[trigger.name]()
		return False

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False

	def destroy(self):
		self.__destroy()
		return
