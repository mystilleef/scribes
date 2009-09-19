class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__new_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("new-window", "<ctrl>n")
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		del self
		self = None
		return False

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __new(self):
		self.__editor.response()
		self.__editor.new()
		self.__editor.response()
		return False

	def __new_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__new, priority=9999)
		return
