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
	"""
	Calculate the resolution independent width and height of windows based on
	the host system's monitor resolution.

	@param window: Any window/dialog object.
	@type window: A gtk.Window object.

	@param width: An arbitrary ratio used to determine a resolution independent
		width.
	@type width: A Float/Integer object.

	@param height: An arbitrary ratio used to determine a resolution independent
		height.
	@type height: A Float/Integer object.

	@return: The width and height to set the window objects to.
	@rtype: A Tuple object containing the suggested width and height to set
		windows to.
	"""
	screen = window.get_screen()
	number = screen.get_number()
	rectangle = screen.get_monitor_geometry(number)
	width = int(rectangle.width/width)
	height = int(rectangle.height/height)
	return width, height

def create_button(stock_id, string):
	"""
	Create a button with a stock icon and a custom label

	@param stock_id: a GTK stock icon identifier
	@type stock_id: string
	@param string: text to be displayed on the button
	@type string: GTK Label

	@return: a stock icon and label
	@rtype: HBox object
	"""
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
	"""
	Create a scrollwindow object for the editor

	@return: A scroll window.
	@rtype:	A gtk.ScrolledWindow object.
	"""
	from gtk import ScrolledWindow, RESIZE_PARENT, POLICY_AUTOMATIC
	from gtk import SHADOW_IN
	scrollwin = ScrolledWindow()
	scrollwin.set_border_width(1)
	scrollwin.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
	scrollwin.set_shadow_type(SHADOW_IN)
	return scrollwin

def get_language(uri):
	"""
	Determine the source code language for a URI

	@param uri: A universal resource identifier pointing to, or representing, a
		file.
	@type uri: A String object.

	@return: An object representing a source code language.
	@rtype: A gtksourceview.SourceLanguage object.
	"""
	try:
		#print "uri", uri
		if uri is None: return None
		from gnomevfs import get_mime_type
		mimetype = get_mime_type(uri)
		#print "Mimetype", mimetype
		from gtksourceview import SourceLanguagesManager
		manager = SourceLanguagesManager()
		language = manager.get_language_from_mime_type(mimetype)
		#print "Language", language
	except RuntimeError:
		print "Caught runtime error when determining language"
		return None
	return language

def create_encoding_box(combobox):
	from internationalization import msg0157
	from gtk import Label, HBox
	label = Label(msg0157)
	label.set_use_underline(True)
	hbox = HBox(homogeneous=False, spacing=10)
	hbox.pack_start(label, False, False, 0)
	hbox.pack_start(combobox, True, True, 0)
	return hbox

def generate_encodings():
	"""
	Generate a tuple containing supported encodings.

	@return: A tuple containing supported encodings.
	@rtype: A tuple object.
	"""
	from internationalization import msg0208, msg0209, msg0210
	from internationalization import msg0211, msg0212, msg0213, msg0214, msg0215
	from internationalization import msg0216, msg0217, msg0218, msg0219, msg0220
	from internationalization import msg0221, msg0222, msg0223, msg0224, msg0225
	from internationalization import msg0226, msg0227, msg0228, msg0229, msg0230
	from internationalization import msg0231, msg0232, msg0233, msg0234, msg0235
	from internationalization import msg0236, msg0237, msg0238, msg0239, msg0240
	from internationalization import msg0241, msg0242, msg0243, msg0244, msg0245
	from internationalization import msg0246, msg0247, msg0248, msg0249, msg0250
	from internationalization import msg0251, msg0252, msg0253, msg0254, msg0255
	from internationalization import msg0256, msg0257, msg0258, msg0259, msg0260
	from internationalization import msg0261, msg0262, msg0263, msg0264, msg0265
	from internationalization import msg0266, msg0267, msg0268, msg0269, msg0270
	from internationalization import msg0271, msg0272, msg0273, msg0274, msg0275
	from internationalization import msg0276, msg0277, msg0278, msg0279, msg0280
	from internationalization import msg0281, msg0282, msg0283, msg0284, msg0285
	from internationalization import msg0286, msg0287, msg0288, msg0289, msg0290
	from internationalization import msg0291
	encodings = (
#		 Codec		Alias		Language
		("ISO-8859-1", "iso-8859-1", msg0262),
		("ISO-8859-2", "iso-8859-2", msg0263),
		("ISO-8859-3", "iso-8859-3", msg0264),
		("ISO-8859-4", "iso-8859-4", msg0265),
		("ISO-8859-5", "iso-8859-5", msg0266),
		("ISO-8859-6", "iso-8859-6", msg0267),
		("ISO-8859-7", "iso-8859-7", msg0268),
		("ISO-8859-8", "iso-8859-8", msg0269),
		("ISO-8859-9", "iso-8859-9", msg0270),
		("ISO-8859-10", "iso-8859-10", msg0271),
		("ISO-8859-13", "iso-8859-13", msg0272),
		("ISO-8859-14", "iso-8859-14", msg0273),
		("ISO-8859-15", "iso-8859-15", msg0274),
		("ISO-2022-JP", "iso2022jp", msg0255),
		("ISO-2022-jp-1", "iso2022jp-1", msg0256),
		("ISO-2022-JP-2", "iso2022jp-2", msg0257),
		("ISO-2022-JP-2004", "iso2022jp-2004", msg0258),
		("ISO-2022-JP-3", "iso2022jp-3", msg0259),
		("ISO-2022-JP-EXT", "iso2022jp-ext", msg0260),
		("ISO-2022-KR", "csiso2022kr", msg0261),
		("BIG5", "csbig5", msg0209),
		("BIG5HKSCS", "hkscs", msg0210),
		("SHIFT-JIS", "sjis", msg0285),
		("SHIFT-JIS-2004", "sjis2004", msg0286),
		("SHIFT-JISX0213", "sjisx0213", msg0287),
		("KOI8-R", "koi8_r", msg0276),
		("KOI8-U", "koi8_u", msg0277),
		("CP037", "IBM039", msg0211),
		("CP424", "IBM424", msg0212),
		("CP437", "437", msg0213),
		("CP500", "IBM500", msg0214),
		("CP737", "cp737", msg0215),
		("CP775", "IBM775", msg0216),
		("CP850", "IBM850", msg0217),
		("CP852", "IBM852", msg0218),
		("CP855", "IBM855", msg0219),
		("CP856", "cp856", msg0220),
		("CP857", "IBM857", msg0221),
		("CP860", "IBM860", msg0222),
		("CP861", "IBM861", msg0223),
		("CP862", "IBM862", msg0224),
		("CP863", "IBM863", msg0225),
		("CP864", "IBM864", msg0226),
		("CP865", "IBM865", msg0227),
		("CP866", "IBM866", msg0228),
		("CP869", "IBM869", msg0229),
		("CP874", "cp874", msg0230),
		("CP875", "cp875", msg0231),
		("CP932", "mskanji", msg0232),
		("CP949", "uhc", msg0233),
		("CP950", "ms950", msg0234),
		("CP1006", "cp1006", msg0235),
		("CP1026", "ibm1026", msg0236),
		("CP1140", "ibm1140", msg0237),
		("CP1250", "windows-1250", msg0238),
		("CP1251", "windows-1251", msg0239),
		("CP1252", "windows-1252", msg0240),
		("CP1253", "windows-1253", msg0241),
		("CP1254", "windows-1254", msg0242),
		("CP1255", "windows-1255", msg0243),
		("CP1256", "windows1256", msg0244),
		("CP1257", "windows-1257", msg0245),
		("CP1258", "windows-1258", msg0246),
		("EUC-JP", "ujis", msg0247),
		("EUC-JIS-2004", "eucjis2004", msg0248),
		("EUC-JISX0213", "eucjisx0213", msg0249),
		("EUC-KR", "ksc5601", msg0250),
		("GB2312",	"euccn", msg0251),
		("GBK", 	"ms936", msg0252),
		("GB18030", "gb18030-2000", msg0253),
		("HZ", "hzgb", msg0254),
		("JOHAB", "cp1361", msg0275),
		("MAC-CYRILLIC", "maccyrillic", msg0278),
		("MAC-GREEK", 	"macgreek", msg0279),
		("MAC-ICELAND", "maciceland", msg0280),
		("MAC-LATIN2", "maccentraleurope", msg0281),
		("MAC-ROMAN", "macroman", msg0282),
		("MAC-TURKISH", "macturkish", msg0283),
		("PTCP154", "cp154", msg0284),
		("UTF-16", "utf16", msg0288),
		("UTF-16-BE", "UTF-16BE", msg0289),
		("UTF-16-LE", "UTF-16LE", msg0290),
		("UTF-7", "U7", msg0291),
		("ASCII", "us-ascii", msg0208),
	)
	return encodings

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
	"""
	Check the permission flags of a URI.

	This function returns True if the URI has read/write permission flags or
	False if the URI has readonly permission.

	@param uri: An object representing, or pointing to, a document.
	@type uri: A gnomevfs.URI object.

	@return: True if you URI has read/write permissions, False otherwise
	@rtype: A Boolean object.
	"""
	value = True
	if uri.startswith("file:///"):
		from gnomevfs import get_local_path_from_uri
		local_path = get_local_path_from_uri(uri)
		from os import access, W_OK, path
		if path.exists(local_path):
			value = access(local_path, W_OK)
		else:
			from info import home_folder
			if local_path.startswith(home_folder) is False:
				value = False
	else:
		writable_scheme = ["ssh", "sftp", "smb", "dav", "davs", "ftp"]
		from gnomevfs import get_uri_scheme
		scheme = get_uri_scheme(uri)
		if not scheme in writable_scheme: value = False
	return value

def get_file_size(uri):
	"""
	Get the size of a file.

	@param uri: A URI pointing to a file.
	@type uri: A String object.

	@return: The size of a file.
	@rtype: An Integer object.
	"""
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
	"""
	Create a generic menu item.

	@param string: A string representing a label for the menu item.
	@type string: A String object.

	@param stock_id: An image for menu item.
	@type stock_id: A gtk.STOCK_ID object.

	@return: A menuitem with a label and stock ID.
	@rtype: A gtk.MenuItem object.
	"""
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
	"""
	Calculate the position to place the word completion window in the text
	editor's buffer.

	@param editor: Reference to the editor object.
	@type editor: An editor object

	@param width: The width of the text editor's completion window.
	@type width: An integer object.

	@param height: The height of the text editor's completion window.
	@type height: An integer object.
	"""
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
	"""
	Find a file in Scribes data folder.

	This function looks data files and images in Scribes data folder.

	#TODO: Use a more brute force approach.

	@param filename: The name of the file to find.
	@type filename: A String object.

	@return: The full path to the file.
	@rtype: A String object.
	"""
	from os import path
	from info import scribes_data_folder
	file_path = path.join(scribes_data_folder, filename)
	return file_path

def create_image(file_path):
	"""
	Create an image of a file.

	@param file_path: Path to the image file.
	@type file_path: A String object.
	"""
	image_file = find_file(file_path)
	from gtk import Image
	image = Image()
	image.set_from_file(image_file)
	return image

def __convert_to_string(value):
	"""
	Convert an integer to a hexidecimal string.

	@param value: An integer representing a unit of the gtk.gdk.Color
	@type value: An Integer object.

	@return: A hexidecimal string
	@rtype: A String object.
	"""
	if not value:
		return "0000"
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
	"""
	Convert a color to a string specification.

	@param color: A color.
	@type color: A gtk.gdk.Color object.

	@return: A hexidecimal representing the gtk.gdk.color
	@rtype: A String object.
	"""
	red = __convert_to_string(color.red)
	blue = __convert_to_string(color.blue)
	green = __convert_to_string(color.green)
	string = "#" + red + green + blue
	return string

def select_row(treeview, column=0):
	"""
	Select a row in a treeview if any.

	This function disables the treeview if it has no rows. Otherwise,
	it tries to figure out any row to select.

	@param treeview: Reference to a TreeView object.
	@type self: An gtk.TreeView object.
	"""
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
	"""
	Disconnect a signal from an object.

	@param signal_id: A numeric identifier for a signal.
	@type signal_id: A Integer object.

	@param instance: An object connected to a signal.
	@type instance: A GObject object.
	"""
	try:
		if signal_id and instance.handler_is_connected(signal_id): instance.disconnect(signal_id)
	except AttributeError:
		print "Disconnect Signal error: ", instance
	return

def init_gnome():
	"""
	Initialize the GNOME libraries.
	"""
	# Crashes the save dialog if uncommented.
	#import gnome.ui
	from info import version, name, scribes_data_path
	from gnome import PARAM_APP_DATADIR, program_init, ui
	properties = {
		PARAM_APP_DATADIR: scribes_data_path,
	}
	program = program_init(name, version, properties=properties)
	return

#try:
#	from psyco import bind
#	bind(generate_random_number)
#	bind(calculate_completion_window_position)
#	bind(disconnect_signal)
#except ImportError:
#	pass
