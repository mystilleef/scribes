class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__toggle_comment_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__create_trigger("toggle_comment", "alt - c")
		self.__manager = None
		return

	def __create_trigger(self, name, shortcut):
		# Trigger that (un)comments lines in several source code.
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __toggle_comment_cb(self, *args):
		try:
			self.__manager.toggle_comment()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.toggle_comment()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return
