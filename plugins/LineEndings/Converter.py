class Converter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("to-unix", self.__to_unix_cb)
		self.__sigid3 = manager.connect("to-mac", self.__to_mac_cb)
		self.__sigid4 = manager.connect("to-windows", self.__to_windows_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __convert(self, character):
		self.__editor.busy(True)
		offset = self.__editor.cursor.get_offset()
		lines = self.__editor.get_text().splitlines()
		self.__editor.textbuffer.set_text(character.join(lines))
		iterator = self.__editor.textbuffer.get_iter_at_offset(offset)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.textview.scroll_to_iter(iterator, 0.3, use_align=True, xalign=1.0)
		self.__editor.busy(False)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return

	def __to_unix_cb(self, *args):
		self.__convert("\n")
		from i18n import msg1
		self.__editor.update_status_message(msg1, "yes")
		return False

	def __to_mac_cb(self, *args):
		self.__convert("\r")
		from i18n import msg2
		self.__editor.update_status_message(msg2, "yes")
		return False

	def __to_windows_cb(self, *args):
		self.__convert("\r\n")
		from i18n import msg3
		self.__editor.update_status_message(msg3, "yes")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False