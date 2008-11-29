class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__create_trigger()
		return

	def __create_trigger(self):
		# Trigger to close current window and open new one.
		trigger = self.__editor.create_trigger("close_reopen", "ctrl+shift+n")
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, *args):
		self.__editor.response()
		self.__editor.new()
		self.__editor.response()
		self.__editor.close()
		self.__editor.response()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return
