class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.__create_trigger()
		return

	def __create_trigger(self):
		trigger = self.__editor.create_trigger("show-quick-open-window", "<ctrl><alt>o")
		self.__editor.add_trigger(trigger)
		return trigger

	def __activate_cb(self, *args):
		try :
			self.__quickopen_window.show_dialog()
		except AttributeError :
			from Window import QuickOpenWindow
			self.__quickopen_window = QuickOpenWindow(self.__editor)
			self.__quickopen_window.show_dialog()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return
