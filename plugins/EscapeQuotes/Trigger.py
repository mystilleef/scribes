class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__escape_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__unescape_cb)

	def __init_attributes(self, editor):
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("escape-quotes", "ctrl+shift+e")
		self.__trigger2 = self.__create_trigger("unescape-quotes", "ctrl+alt+e")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		self.__manager.destroy()
		triggers = (self.__trigger1, self.__trigger2 )
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		del self
		self = None
		return False

	def __escape_cb(self, *args):
		self.__manager.escape()
		return

	def __unescape_cb(self, *args):
		self.__manager.unescape()
		return False
