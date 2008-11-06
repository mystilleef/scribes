class Trigger(object):
	"""
	This class creates objects, triggers,  that allows users to perform
	python specific navigation and selection operations in Python source
	code.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__prv_trigger.connect("activate", self.__prv_block_cb)
		self.__sigid2 = self.__nxt_trigger.connect("activate", self.__nxt_block_cb)
		self.__sigid3 = self.__select_trigger.connect("activate", self.__select_block_cb)
		self.__sigid4 = self.__end_trigger.connect("activate", self.__end_block_cb)
		self.__sigid5 = self.__select_function_trigger.connect("activate", self.__select_function_cb)
		self.__sigid6 = self.__select_class_trigger.connect("activate", self.__select_class_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__prv_trigger = self.__create_trigger("move_to_previous_block", "alt+bracketleft")
		self.__nxt_trigger = self.__create_trigger("move_to_next_block", "alt+bracketright")
		self.__select_trigger = self.__create_trigger("select_python_block", "alt+h")
		self.__end_trigger = self.__create_trigger("move_to_block_end", "alt+e")
		self.__select_function_trigger = self.__create_trigger("select_function", "alt+f")
		self.__select_class_trigger = self.__create_trigger("select_class", "alt+a")
		self.__manager = None
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __prv_block_cb(self, *args):
		self.__get_manager().previous_block()
		return

	def __nxt_block_cb(self, *args):
		self.__get_manager().next_block()
		return

	def __select_function_cb(self, *args):
		self.__get_manager().select_function()
		return

	def __select_class_cb(self, *args):
		self.__get_manager().select_class()
		return

	def __select_block_cb(self, *args):
		self.__get_manager().select_block()
		return

	def __end_block_cb(self, *args):
		self.__get_manager().end_of_block()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__prv_trigger)
		self.__editor.remove_trigger(self.__nxt_trigger)
		self.__editor.remove_trigger(self.__select_trigger)
		self.__editor.remove_trigger(self.__end_trigger)
		self.__editor.remove_trigger(self.__select_function_trigger)
		self.__editor.remove_trigger(self.__select_class_trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__prv_trigger)
		self.__editor.disconnect_signal(self.__sigid2, self.__nxt_trigger)
		self.__editor.disconnect_signal(self.__sigid3, self.__select_trigger)
		self.__editor.disconnect_signal(self.__sigid4, self.__end_trigger)
		self.__editor.disconnect_signal(self.__sigid5, self.__select_function_trigger)
		self.__editor.disconnect_signal(self.__sigid6, self.__select_class_trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return
