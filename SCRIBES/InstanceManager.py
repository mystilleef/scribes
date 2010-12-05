class Manager(object):

	def __init__(self):
		from DBusService import DBusService
		DBusService(self)
		self.__init_attributes()
		from SaveProcessInitializer.Manager import Manager
		Manager()
		from TerminalSignalHandler import Handler
		Handler(self)
		from signal import signal, SIGINT, SIGQUIT, SIG_DFL
		signal(SIGINT, SIG_DFL)
		signal(SIGQUIT, SIG_DFL)
		from sys import setcheckinterval
		setcheckinterval(-1)
		from gobject import timeout_add
		timeout_add(60000, self.__init_psyco, priority=9999)
		self.__init_i18n()

	def __init_attributes(self):
		from collections import deque
		self.__editor_instances = deque([])
		from gtk import WindowGroup
		self.__wingroup = WindowGroup()
		self.__busy = False
		self.__interval = 0
		self.__shortcut_list = []
#		self.__count = 0
		return

########################################################################
#
#						Public APIs
#
########################################################################

	def register_editor(self, instance):
		self.__wingroup.add_window(instance.window)
		self.__editor_instances.append(instance)
		return False

	def unregister_editor(self, instance):
		try:
			self.__editor_instances.remove(instance)
			self.__wingroup.remove_window(instance.window)
		except (ValueError, TypeError):
			print "===================================================="
			print "Module: InstanceManager.py"
			print "Class: Manager"
			print "Method: unregister_editor"
			print "Exception Type: ValueError"
			print "Error: Instance not found", instance
			print "===================================================="
		finally:
			if instance and instance.window: instance.window.destroy()
			if instance: del instance
			# Quit when there are no editor instances.
			if not self.__editor_instances: self.__quit()
		return

	def save_processor_is_ready(self):
		from Utils import get_save_processor
		processor = get_save_processor()
		return processor.is_ready() if processor else False

	def get_save_processor(self):
		from Utils import get_save_processor
		return get_save_processor()

	def open_files(self, uris=None, encoding="utf-8"):
		try:
			if not uris: raise ValueError
			has_uri = lambda x: x in self.get_uris()
			has_not_uri = lambda x: not (x in self.get_uris())
			open_file = lambda x: self.__open_file(x, encoding)
			# Focus respective window if file is already open.
			[self.focus_file(str(uri)) for uri in uris if has_uri(str(uri))]
			# Open new file if it's not already open.
			[open_file(str(uri)) for uri in uris if has_not_uri(str(uri))]
		except ValueError:
			self.__new_editor()
		return False

	def close_files(self, uris):
		if not uris: return False
		[self.__close_file(str(uri)) for uri in uris]
		return False

	def close_all_windows(self):
		# This is the best place I can think of to capture last session files.
		last_session_uris = self.get_uris()
		from LastSessionMetadata import set_value
		set_value(last_session_uris)
		from copy import copy
		[instance.close() for instance in copy(self.__editor_instances)]
		return False

	def get_last_session_uris(self):
		from LastSessionMetadata import get_value
		return get_value()

	def focus_file(self, uri):
		if uri is None: uri = ""
		found_instance = [editor for editor in self.__editor_instances if editor.uri == str(uri)]
		if not found_instance: return False
		editor = found_instance[0]
		self.__focus(editor)
		return False

	def focus_by_id(self, id_):
		instance = [instance for instance in self.__editor_instances if instance.id_ == id_]
		editor = instance[0]
		self.__focus(editor)
		return False

	def get_uris(self):
		if not self.__editor_instances: return []
		return [str(editor.uri) for editor in self.__editor_instances if editor.uri]

	def get_text(self):
		if not self.__editor_instances: return []
		return [editor.text for editor in self.__editor_instances]

	def get_editor_instances(self):
		return self.__editor_instances

	def add_shortcut(self, shortcut):
		return self.__shortcut_list.append(shortcut)

	def remove_shortcut(self, shortcut):
		return self.__shortcut_list.remove(shortcut)

	def get_shortcuts(self):
		return self.__shortcut_list

	def response(self):
		if self.__busy: return False
		self.__busy = True
		from Utils import response
		response()
		self.__busy = False
		return False

	def set_vm_interval(self, response=True):
		#FIXME: This function is deprecated!
		return False

	def __open_file(self, uri, encoding="utf-8"):
		if not uri: return False
		uri = str(uri)
		instances = self.__editor_instances
		empty_windows = [x for x in instances if not x.contains_document]
		empty_windows[0].load_file(str(uri), encoding) if empty_windows else self.__new_editor(uri, encoding)
		return False

	def __close_file(self, uri):
		from copy import copy
		[editor.close() for editor in copy(self.__editor_instances) if editor.uri == str(uri)]
		return False

	def __new_editor(self, uri=None, encoding="utf-8"):
		if uri is None: uri = ""
		from Editor import Editor
		Editor(self, str(uri), encoding)
		return False

	def __focus(self, editor):
		editor.refresh(True)
		if editor.window.get_data("minimized"): editor.window.deiconify()
		editor.window.present()
		editor.refresh(True)
#		editor.textview.grab_focus()
		return False

	def __init_garbage_collector(self):
		from gc import collect
		collect()
		return True

	def __init_psyco(self):
		try:
			from psyco import background
			background()
		except ImportError:
			pass
		return False

	def __init_i18n(self):
		from Globals import data_path
		from os import path
		locale_folder = path.join(data_path, "locale")
		# Initialize glade first.
		try:
			from locale import setlocale, LC_ALL, Error, bindtextdomain
			bindtextdomain("scribes", locale_folder)
			setlocale(LC_ALL, "")
		except Error:
			pass
		from gtk import glade
		glade.bindtextdomain("scribes", locale_folder)
		glade.textdomain("scribes")
		from gettext import textdomain, bindtextdomain
		from gettext import install, bind_textdomain_codeset
		bindtextdomain("scribes", locale_folder)
		bind_textdomain_codeset("scribes", "UTF-8")
		textdomain("scribes")
		install("scribes", locale_folder, unicode=1)
		return

	def __remove_swap_area(self):
		from glob import glob
		from Globals import metadata_folder, tmp_folder
		from os.path import join
		files = glob(join(tmp_folder, ".Scribes*scribes"))
		from shutil import rmtree
		[rmtree(file_, True) for file_ in files]
		files = glob(join(metadata_folder, "__db*"))
		[rmtree(file_, True) for file_ in files]
		return

	def __quit(self):
		self.__remove_swap_area()
		raise SystemExit

	def force_quit(self):
		from os import _exit
		_exit(0)
		return
