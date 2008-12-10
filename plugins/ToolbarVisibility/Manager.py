class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.textview.connect("motion-notify-event", self.__motion_notify_event_cb)
		self.__sigid2 = editor.window.connect("leave-notify-event", self.__hide_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__monitor_mouse, priority=9999)
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__activate = False
		self.__show = None
		self.__uri = self.__get_database_uri(editor)
		return

	def __get_database_uri(self, editor):
		# Path to the font database.
		from os.path import join
		folder = join(editor.metadata_folder, "Preferences")
		file_path = join(folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		uri = get_uri(file_path)
		return uri

	def __monitor_mouse(self):
		self.__disable_mouse_monitor()
		from MinimalModeMetadata import get_value
		if get_value(): self.__enable_mouse_monitor()
		return False

	def __show_hide_full_view(self, widget):
		if self.__activate is False: return False
		x, y, type_ = widget.window.get_pointer()
		if y <= 21:
			if self.__show is True: return False
			self.__show_full_view()
		else:
			if self.__show is False: return False
			self.__hide_full_view()
		return False

	def __generic_cb(self, *args):
		self.__show_hide_full_view(self.__editor.textview)
		return

	def __hide_cb(self, window, event):
		if self.__activate is False: return False
		if not self.__show: return False
		window.window.get_pointer()
		self.__hide_full_view()
		return False

	def __motion_notify_event_cb(self, window, event):
		if self.__activate is False: return False
		self.__show_hide_full_view(window)
		return False

	def __show_full_view(self):
		self.__editor.refresh(False)
		self.__editor.toolbar.show()
		self.__editor.statusbar.show()
		self.__editor.refresh(False)
		self.__show = True
		return False

	def __hide_full_view(self):
		self.__editor.refresh()
		self.__editor.toolbar.hide()
		self.__editor.statusbar.hide()
		self.__editor.refresh()
		self.__show = False
		return False

	def __disable_mouse_monitor(self):
		self.__editor.textview.handler_block(self.__sigid1)
		self.__editor.window.handler_block(self.__sigid2)
		self.__activate = False
		return

	def __enable_mouse_monitor(self):
		self.__editor.textview.handler_unblock(self.__sigid1)
		self.__editor.window.handler_unblock(self.__sigid2)
		self.__activate = True
		return

	def toggle_minimal_interface(self):
		from MinimalModeMetadata import get_value, set_value
		minimal_mode = get_value()
		if minimal_mode:
			set_value(False)
			self.__disable_mouse_monitor()
		else:
			set_value(True)
			self.__enable_mouse_monitor()
		return

	def destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.window)
		del self
		self = None
		return

	def __changed_cb(self, *args):
		self.__monitor_mouse()
		return False

	def __precompile_methods(self):
		methods= (self.__show_hide_full_view, self.__show_full_view,
			self.__hide_full_view, self.__motion_notify_event_cb)
		self.__editor.optimize(methods)
		return False
