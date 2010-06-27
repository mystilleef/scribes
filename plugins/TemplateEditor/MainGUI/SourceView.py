from gtksourceview2 import View, Buffer

class SourceView(View):

	def __init__(self, manager, editor):
		editor.response()
		View.__init__(self, Buffer())
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__add_view_to_scrolled_window()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("description-treeview-sensitivity", self.__sensitive_cb)
		self.__sigid3 = manager.connect("description-treeview-cursor-changed", self.__changed_cb)
		self.__sigid4 = manager.connect("selected-templates-dictionary-key", self.__key_cb)
		self.__sigid5 = manager.connect("templates-dictionary", self.__dictionary_cb)
		self.__sigid6 = self.connect("button-press-event", self.__button_press_event_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = self.get_buffer()
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self)
		del self
		self = None
		return False

	def __add_view_to_scrolled_window(self):
		self.__clear()
		scrolled_window = self.__manager.gui.get_widget("ScrolledWindow")
		scrolled_window.add(self)
		return False

	def __set_properties(self):
		self.set_property("editable", False)
		self.set_property("cursor-visible", False)
		self.set_property("can-focus", False)
		self.set_property("can-default", False)
		self.set_property("has-default", False)
		self.set_property("has-focus", False)
		self.set_property("is-focus", False)
		self.set_property("receives-default", False)
		return False

	def __update_properties(self):
		return False

	def __show_template(self, key):
		template = self.__dictionary[key][1]
		self.__buffer.set_text(template)
		self.set_property("sensitive", True)
		return False

	def __clear(self):
		self.set_property("sensitive", False)
		self.__buffer.set_text("")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __sensitive_cb(self, manager, sensitive):
		self.set_property("sensitive", sensitive) if sensitive else self.__clear()
		return False

	def __changed_cb(self, *args):
		self.__clear()
		return False

	def __key_cb(self, manager, key):
		self.__show_template(key)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False

	def __button_press_event_cb(self, *args):
		self.__manager.emit("show-edit-template-editor")
		return True
