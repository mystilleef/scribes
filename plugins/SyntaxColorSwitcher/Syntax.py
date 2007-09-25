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
Provide syntax highlighting for gtksourceview.Buffer objects.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def convert_string_to_boolean(string):
	"""
	Convert a string representing True or False into their boolean equivalents.

	@param string: A string representing True or False
	@type string: A String object.

	@return: True or False
	@rtype: A Boolean object.
	"""
	if string == "True":
		value = True
	else:
		value = False
	return value

def get_style(style_elements):
	"""
	Get a style to be used for syntax highlighting.

	@param style_elements: Attributes of a stye to be used for syntax highlighting.
	@type style_elements: A Tuple object.

	@return: A style to be used for syntax highlighting.
	@rtype: A gtk.Style object.
	"""
	from gtksourceview import SourceTagStyle
	style = SourceTagStyle()
	from gtk.gdk import color_parse
	style.foreground = color_parse(style_elements[0].get_string())
	if style_elements[1].get_string() != "None":
		style.background = color_parse(style_elements[1].get_string())
	style.bold = convert_string_to_boolean(style_elements[2].get_string())
	style.italic = convert_string_to_boolean(style_elements[3].get_string())
	style.underline = convert_string_to_boolean(style_elements[4].get_string())
	return style

def set_language_style(language, entries, syntax_key):
	"""
	Use syntax highlight color found in GConf.

	This function modifies the default language style set by gtksourceview.
	Language style represent the style of highlighted keywords in source code
	file. This function uses the style attributes found in the GConf database
	instead.

	@param language: An object representing the language for a source code.
	@type language: A gtksourceview.SourceLanguage object.

	@param entries: Entries found for a particular language in the GConf database.
	@type entries: A gconf.Entry object.

	@param syntax_key: A GConf key.
	@param syntax_key: A String object.

	@return: An object representing the language for a source code file.
	@rtype: A gtksourceview.SourceLanguage object.
	"""
	try:
		# Syntax color keys in GConf
		key_list = [item.key.replace(syntax_key + "/", "") for item in entries]
		# Syntax color attributes for keys in GConf
		value_list = [item.value.get_list() for item in entries]
		count = 0
		for key in key_list:
			style = get_style(value_list[count])
			language.set_tag_style(key, style)
			count += 1
	except:
		return None
	return language

def activate_syntax_highlight(textbuffer, language=None):
	"""
	Highlight keywords in source code for various programming languages.

	This function can be called via a timeout_add function to it returns False
	to prevent the function from being called repeatedly.

	@param textbuffer: A buffer object.
	@type textbuffer: A gtksourceview.SourceBuffer object.

	@param language: An object representing the language for a source code.
	@type language: A gtksourceview.SourceLanguage object.

	@return: False to terminate the timeout_add function that calls this one.
	@rtype: A Boolean object.
	"""
	textbuffer.set_highlight(True)
	try:
		if language:
			syntax_key = "/apps/scribes/SyntaxHighlight/" + language.get_id()
			from gconf import client_get_default
			client = client_get_default()
			if client.dir_exists(syntax_key):
				entries = client.all_entries(syntax_key)
				if entries:
					language = set_language_style(language, entries, syntax_key)
			textbuffer.set_language(language)
	except:
		pass
	return False
