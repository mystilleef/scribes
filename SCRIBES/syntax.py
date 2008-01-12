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
	fgcolor, bgcolor, bold, italic, underline  = style_elements
	from gtk.gdk import color_parse
	if fgcolor:	style.foreground = color_parse(fgcolor)
	if bgcolor: style.background = color_parse(bgcolor)
	if bold: style.bold = bold
	if italic: style.italic = italic
	if underline: style.underline = underline
	return style

def set_language_style(language, syntax_properties):
	"""
	Use syntax highlight color found in GConf.

	This function modifies the default language style set by gtksourceview.
	Language style represent the style of highlighted keywords in source code
	file. This function uses the style attributes found in the GConf database
	instead.

	@param language: An object representing the language for a source code.
	@type language: A gtksourceview.SourceLanguage object.

	@param syntax_properties: Entries found for a particular language in the GConf database.
	@type syntax_properties: A gconf.Entry object.

	@return: An object representing the language for a source code file.
	@rtype: A gtksourceview.SourceLanguage object.
	"""
	for dictionary in syntax_properties:
		style = get_style(dictionary.values()[0])
		language.set_tag_style(dictionary.keys()[0], style)
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
		if not language: return False
		from SyntaxColorsMetadata import get_value
		syntax_properties = get_value(language.get_id())
		if not syntax_properties: raise ValueError
		textbuffer.set_language(set_language_style(language, syntax_properties))
	except ValueError:
		textbuffer.set_language(language)
	return False
