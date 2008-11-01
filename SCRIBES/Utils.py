# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This modules contains a library of generic auxiliary functions that can be used
accross the project. The functions are designed with reuse and modularity in
mind.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def calculate_resolution_independence(window, width, height):
	# Need to deprecate this function.
	screen = window.get_screen()
	number = screen.get_number()
	rectangle = screen.get_monitor_geometry(number)
	width = int(rectangle.width/width)
	height = int(rectangle.height/height)
	return width, height

def create_button(stock_id, string):
	from gtk import HBox, Image, Label, ICON_SIZE_BUTTON, Alignment
	alignment = Alignment()
	alignment.set_property("xalign", 0.5)
	alignment.set_property("yalign", 0.5)
	hbox = HBox(False, 3)
	if stock_id:
		image = Image()
		image.set_from_stock(stock_id, ICON_SIZE_BUTTON)
		hbox.pack_start(image, False, False, 0)
	label = Label(string)
	label.set_property("use-underline", True)
	hbox.pack_start(label, False, False, 0)
	alignment.add(hbox)
	return alignment

def process_color(color):
	red = int(color[0])
	green = int(color[1])
	blue = int(color[2])
	pixel = long(color[3])
	from gtk.gdk import Color
	color = Color(red, green, blue, pixel)
	return color

def create_scrollwin():
	from gtk import ScrolledWindow, RESIZE_PARENT, POLICY_AUTOMATIC
	from gtk import SHADOW_IN
	scrollwin = ScrolledWindow()
	scrollwin.set_border_width(1)
	scrollwin.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
	scrollwin.set_shadow_type(SHADOW_IN)
	return scrollwin

def __get_language_for_mime_type(mime):
	from gtksourceview2 import language_manager_get_default
	lang_manager = language_manager_get_default()
	lang_ids = lang_manager.get_language_ids()
	for i in lang_ids:
		lang = lang_manager.get_language(i)
		for m in lang.get_mime_types():
			if m == mime: return lang
	return None

def get_language(uri):
	try:
		if uri is None: return None
		from gnomevfs import get_mime_type
		mimetype = get_mime_type(uri.strip())
		language = __get_language_for_mime_type(mimetype)
	except RuntimeError:
		print "Caught runtime error when determining mimetype or language"
		return None
	return language

def create_encoding_box(combobox):
	from i18n import msg0157
	from gtk import Label, HBox
	label = Label(msg0157)
	label.set_use_underline(True)
	hbox = HBox(homogeneous=False, spacing=10)
	hbox.pack_start(label, False, False, 0)
	hbox.pack_start(combobox, True, True, 0)
	return hbox

def generate_random_number(sequence):
	from random import random
	while True:
		exit = True
		number = random()
		if sequence:
			for item in sequence:
				if number == item:
					exit = False
					break
		if exit: break
	return number

def check_uri_permission(uri):
	value = True
	if uri.startswith("file:///"):
		from gnomevfs import get_local_path_from_uri
		local_path = get_local_path_from_uri(uri)
		from os import access, W_OK, path
		if path.exists(local_path):
			value = access(local_path, W_OK)
		else:
			from Globals import home_folder
			if local_path.startswith(home_folder) is False:
				value = False
	else:
		writable_scheme = ["ssh", "sftp", "smb", "dav", "davs", "ftp"]
		from gnomevfs import get_uri_scheme
		scheme = get_uri_scheme(uri)
		if not scheme in writable_scheme: value = False
	return value

def get_file_size(uri):
	size = 0
	from gnomevfs import get_file_info, FILE_INFO_GET_MIME_TYPE
	from gnomevfs import FILE_INFO_FORCE_SLOW_MIME_TYPE
	from gnomevfs import FILE_INFO_FOLLOW_LINKS, FILE_INFO_DEFAULT
	FILE_INFO_ACCESS_RIGHTS = 1 << 4
	try:
		fileinfo = get_file_info(uri, FILE_INFO_DEFAULT |
							FILE_INFO_GET_MIME_TYPE |
							FILE_INFO_FORCE_SLOW_MIME_TYPE |
							FILE_INFO_FOLLOW_LINKS |
							FILE_INFO_ACCESS_RIGHTS)
		if fileinfo:
			try:
				size = fileinfo.size
			except:
				pass
	except:
		pass
	return size

def create_menuitem(string, stock_id=None):
	from gtk import MenuItem, Image, HBox, Label
	hbox = HBox(spacing=7)
	hbox.set_property("border-width", 2)
	if stock_id:
		image = Image()
		image.set_property("stock", stock_id)
		hbox.pack_start(image, False, False, 0)
	label = Label(string)
	label.set_property("use-underline", True)
	hbox.pack_start(label, False, False, 0)
	menuitem = MenuItem()
	menuitem.add(hbox)
	return menuitem

def calculate_completion_window_position(editor, width, height):
	# The flag is true when the position of the word completion window needs to
	# adjusted accross the y-axis.
	editor.y_coordinate_flag = False

	# Get the cursor's coordinate and size.
	cursor_x, cursor_y = get_cursor_window_coordinates(editor)
	cursor_height = get_cursor_size(editor)[1]

	# Get the text editor's textview coordinate and size.
	window = editor.text_view.get_window(TEXT_WINDOW_TEXT)
	rectangle = editor.text_view.get_visible_rect()
	window_x, window_y = window.get_origin()
	window_width, window_height = rectangle.width, rectangle.height

	# Determine where to position the completion window.
	position_x = window_x + cursor_x
	position_y = window_y + cursor_y + cursor_height

	# If the completion window extends past the text editor's buffer,
	# reposition the completion window inside the text editor's buffer area.
	if (position_x + width) > (window_x + window_width):
		position_x = (window_x + window_width) - width
	if (position_y + height) > (window_y + window_height):
		position_y = (window_y + cursor_y) - height
		editor.y_coordinate_flag = True
	return position_x, position_y

def find_file(filename):
	from os import path
	from Globals import data_folder
	file_path = path.join(data_folder, filename)
	return file_path

def create_image(file_path):
	image_file = find_file(file_path)
	from gtk import Image
	image = Image()
	image.set_from_file(image_file)
	return image

def __convert_to_string(value):
	if not value: return "0000"
	string = str(hex(value)).lstrip("0x")
	if len(string) < 4:
		if len(string) == 3:
			string = "0" + string
		elif len(string) == 2:
			string = "00" + string
		else:
			string = "000" + string
	return string

def convert_color_to_spec(color):
	red = __convert_to_string(color.red)
	blue = __convert_to_string(color.blue)
	green = __convert_to_string(color.green)
	string = "#" + red + green + blue
	return string

def select_row(treeview, column=0):
	selection = treeview.get_selection()
	model = treeview.get_model()
	path, iterator = selection.get_selected()
	if iterator:
		path = model.get_path(iterator)
		treeview.set_cursor(path, treeview.get_column(column))
		treeview.grab_focus()
	else:
		first_iterator = model.get_iter_first()
		if first_iterator:
			path = model.get_path(first_iterator)
			treeview.set_cursor(path, treeview.get_column(column))
			treeview.grab_focus()
		else:
			treeview.set_property("sensitive", False)
	return

def disconnect_signal(signal_id, instance):
	try:
		if signal_id and instance.handler_is_connected(signal_id): instance.disconnect(signal_id)
	except AttributeError:
		print "Disconnect Signal error: ", instance
	return

def __is_beside_bracket(iterator, characters):
	if iterator.get_char() in characters: return True
	iterator.backward_char()
	if iterator.get_char() in characters: return True
	return False

def __is_open_bracket(iterator, characters):
	return self.__is_beside_bracket(iterator, characters)

def __is_close_bracket(iterator, characters):
	return self.__is_beside_bracket(iterator, characters)

def __reposition_iterator(iterator, open_chars, close_chars):
	if self.__is_open_bracket(iterator.copy(), open_chars):
		if iterator.get_char() in open_chars: return iterator
		iterator.backward_char()
	else:
		if not (iterator.get_char() in close_chars): return iterator
		iterator.forward_char()
	return iterator

def __get_open_characters():
	return ("{", "(", "[", "<")

def __get_close_characters():
	return ("}", ")", "]", ">")

def __get_open_character(iterator):
	iterator.backward_char()
	return iterator.get_char()

def __get_close_character(iterator):
	return iterator.get_char()

def __get_pair_character(character):
	if character == "{":
		pair_character = "}"
	elif character == "}":
		pair_character = "{"
	elif character == "(":
		pair_character = ")"
	elif character == ")":
		pair_character = "("
	elif character == "[":
		pair_character = "]"
	elif character == "]":
		pair_character = "["
	elif character == "<":
		pair_character = ">"
	elif character == ">":
		pair_character = "<"
	return pair_character

def __is_open_character(iterator):
	characters = __get_open_characters()
	if iterator.get_char() in characters: return True
	success = iterator.backward_char()
	if not success: return False
	if iterator.get_char() in characters: return True
	return False

def __is_close_character(iterator):
	characters = __get_close_characters()
	iterator.backward_char()
	if iterator.get_char() in characters: return True
	iterator.forward_char()
	if iterator.get_char() in characters: return True
	return False

def __reposition_open_iterator(iterator):
	characters = __get_open_characters()
	if not (iterator.get_char() in characters): return iterator
	iterator.forward_char()
	return iterator

def __reposition_close_iterator(iterator):
	characters = __get_close_characters()
	iterator.backward_char()
	if iterator.get_char() in characters: return iterator
	iterator.forward_char()
	return iterator

def __search_for_open_character(iterator):
	iterator = __reposition_close_iterator(iterator.copy())
	character = __get_close_character(iterator.copy())
	search_character = __get_pair_character(character)
	count = 0
	while True:
		success = iterator.backward_char()
		if not success: raise ValueError
		char = iterator.get_char()
		if char == character: count += 1
		if char == search_character and not count: break
		if char == search_character and count: count -= 1
	return iterator

def __search_for_close_character(iterator):
	iterator = __reposition_open_iterator(iterator.copy())
	character = __get_open_character(iterator.copy())
	search_character = __get_pair_character(character)
	count = 0
	while True:
		char = iterator.get_char()
		if char == character: count += 1
		if char == search_character and not count: break
		if char == search_character and count: count -= 1
		success = iterator.forward_char()
		if not success: raise ValueError
	return iterator

def find_matching_bracket(iterator):
	try:
		if __is_open_character(iterator.copy()):
			iterator = __search_for_close_character(iterator.copy())
		elif __is_close_character(iterator.copy()):
			iterator = __search_for_open_character(iterator.copy())
		else:
			iterator = None
	except ValueError:
		return None
	return iterator

def init_gnome():
	# Crashes the save dialog if uncommented.
	from Globals import version, name, data_path
	from gnome import PARAM_APP_DATADIR, program_init, ui
	properties = {
		PARAM_APP_DATADIR: data_path,
	}
	program = program_init(name, version, properties=properties)
	from gnome.ui import authentication_manager_init
	authentication_manager_init()
	return

def backward_to_line_begin(iterator):
	if iterator.starts_line(): return iterator
	while True:
		iterator.backward_char()
		if iterator.starts_line(): break
	return iterator

def forward_to_line_end(iterator):
	if iterator.ends_line(): return iterator
	iterator.forward_to_line_end()
	return iterator

def open_database(basepath, flag="c"):
	if not basepath.endswith(".gdb"): raise Exception
	from Globals import metadata_folder
	from os.path import exists, join, split
	database_path = join(metadata_folder, basepath.strip("/"))
	folder, file_ = split(database_path)
	if not (folder or file_): raise Exception
	if not exists(folder):
		from os import makedirs
		makedirs(folder)
	from shelve import open as open_
	from anydbm import error
	try:
		database = open_(database_path, flag=flag, writeback=False)
	except error:
		database = open_(database_path, flag="n", writeback=False)
	return database

def response():
	from gtk import events_pending, main_iteration
	while events_pending(): main_iteration(False)
	return

def create_uri(uri, exclusive=True):
	from gnomevfs import create, OPEN_WRITE  
	create(uri, OPEN_WRITE, exclusive)
	return

def uri_is_folder(uri):
	if not uri: return False
	from gnomevfs import get_file_info
	info = get_file_info(uri)
	if info.type == 2: return True
	return False

def set_vm_interval(response=True):
	from sys import setcheckinterval, maxint
	interval = -1 if response else maxint
	setcheckinterval(interval)
	return False

try:
	from psyco import bind
	bind(response)
except ImportError:
	pass
