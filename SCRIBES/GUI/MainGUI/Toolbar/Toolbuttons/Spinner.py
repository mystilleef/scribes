from gtk import ToolItem

class Spinner(ToolItem):

	def __init__(self, editor):
		ToolItem.__init__(self)
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("busy", self.__busy_cb)
		self.__sigid3 = editor.connect("spin-throbber", self.__spin_throbber_cb)
		self.__sigid4 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid5 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid6 = editor.connect("load-error", self.__load_error_cb)
		self.__set_properties()
		self.show_all()
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk.gdk import PixbufAnimation
		from os.path import join
		self.__animation = PixbufAnimation(join(editor.data_folder, "throbber-active.gif"))
		throbber_png_path = join(editor.data_folder, "throbber-inactive.png")
		from gtk import image_new_from_file
		self.__image = image_new_from_file(throbber_png_path)
		self.__pixbuf = self.__image.get_pixbuf()
		self.__call_count = 0
		self.__is_spinning = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		self.destroy()
		del self
		self = None
		return

	def __set_properties(self):
		from ..Utils import never_focus
		never_focus(self)
		self.add(self.__image)
		return

	def __start(self):
		self.__call_count += 1
		if self.__is_spinning: return
		self.__is_spinning = True
		self.__image.set_from_animation(self.__animation)
		return

	def __stop(self):
		if self.__is_spinning is False: return
		self.__call_count -= 1
		if self.__call_count: return
		self.__is_spinning = False
		self.__call_count = 0
		self.__image.clear()
		self.__image.set_from_pixbuf(self.__pixbuf)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, editor, busy):
		self.__start() if busy else self.__stop()
		return False

	def __spin_throbber_cb(self, editor, spin):
		self.__start() if spin else self.__stop()
		return False

	def __checking_file_cb(self, *args):
		self.__start()
		return False

	def __loaded_file_cb(self, *args):
		self.__stop()
		return False

	def __load_error_cb(self, *args):
		self.__stop()
		return False
