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
This module contains a set of functions responsible for performing text
operations relating to space and tab characters.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def convert_spaces_to_tabs(sourceview):
	"""
	Convert beginning space characters in a gtksourceview buffer to tab characters.

	The function converts space characters to tab characters and then indents
	lines to the earliest tab stop.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@return: A list of converted lines if any.
	@rtype: A List object.
	"""
	converted_lines = []
	sourceview.set_property("editable", False)
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	use_response = False
	if last_line - first_line > 3000:
		use_response = True
		from SCRIBES.utils import response
	sourcebuffer.begin_user_action()
	for line in range(first_line, last_line+1):
		if use_response:
			response()
		result = convert_spaces_to_tabs_on_line(sourceview, line)
		if result:
			converted_lines.append(line)
	sourcebuffer.end_user_action()
	sourceview.set_property("editable", True)
	return converted_lines

def convert_spaces_to_tabs_on_line(sourceview, line_number):
	"""
	Convert beginning space characters to tab characters on a line.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@param line_number: The line to perform conversion operation on.
	@type line_number: An Integer object.

	@return: True if the line was converted.
	@rtype: An Boolean object.
	"""
	sourcebuffer = sourceview.get_property("buffer")
	tab_width = sourceview.get_property("tabs-width")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	space_list = []
	tab_list = []
	while True:
		if transition_position.get_char() in (" "):
			space_list.append(" ")
		elif transition_position.get_char() in ("\t"):
			tab_list.append("\t")
		else:
			break
		transition_position.forward_char()
	if transition_position.equal(begin_position):
		return False
	number_of_spaces = len(space_list)
	number_of_tabs = len(tab_list)
	if not number_of_spaces:
		return False
	if number_of_spaces < tab_width:
		string = "".join(tab_list)
	else:
		tabs = number_of_spaces / tab_width
		tab_list.append("\t" * tabs)
		string = "".join(tab_list)
	sourcebuffer.delete(begin_position, transition_position)
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	sourcebuffer.insert(begin_position, string)
	return True

def convert_tabs_to_spaces(sourceview):
	"""
	Convert beginning tab characters in a gtksourceview buffer to space characters.

	The function converts tab characters to space characters and then indents
	lines to the earliest tab stop.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@return: A list of converted lines if any.
	@rtype: A List object.
	"""
	converted_lines = []
	sourceview.set_property("editable", False)
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	use_response = False
	if last_line - first_line > 3000:
		use_response = True
		from SCRIBES.utils import response
	sourcebuffer.begin_user_action()
	for line in range(first_line, last_line+1):
		if use_response:
			response()
		result = convert_tabs_to_spaces_on_line(sourceview, line)
		if result:
			converted_lines.append(line)
	sourcebuffer.end_user_action()
	sourceview.set_property("editable", True)
	return converted_lines

def convert_tabs_to_spaces_on_line(sourceview, line_number):
	"""
	Convert beginning tab characters to space characters on a line.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@param line_number: The line to perform conversion operation on.
	@type line_number: An Integer object.

	@return: True if the line was converted.
	@rtype: An Boolean object.
	"""
	sourcebuffer = sourceview.get_property("buffer")
	tab_width = sourceview.get_property("tabs-width")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	space_list = []
	tab_list = []
	while True:
		if transition_position.get_char() in (" "):
			space_list.append(" ")
		elif transition_position.get_char() in ("\t"):
			tab_list.append("\t")
		else:
			break
		transition_position.forward_char()
	if transition_position.equal(begin_position):
		return False
	number_of_spaces = len(space_list)
	number_of_tabs = len(tab_list)
	if number_of_tabs:
		for tab in tab_list:
			space_list.append(" " * tab_width)
	if not len(space_list):
		return False
	if number_of_spaces % tab_width:
		for space in range(number_of_spaces % tab_width):
			space_list.remove(" ")
	string = "".join(space_list)
	sourcebuffer.delete(begin_position, transition_position)
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	sourcebuffer.insert(begin_position, string)
	return True

def remove_trailing_spaces(sourceview):
	"""
	Remove spaces at the end of lines in a gtksourceview buffer.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@return: A list of lines operated upon, if any.
	@rtype: A List object.
	"""
	affected_lines = []
	sourceview.set_property("editable", False)
	sourcebuffer = sourceview.get_property("buffer")
	begin, end = sourcebuffer.get_bounds()
	first_line = begin.get_line()
	last_line = end.get_line()
	use_response = False
	if last_line - first_line > 3000:
		use_response = True
		from SCRIBES.utils import response
	sourcebuffer.begin_user_action()
	for line in range(first_line, last_line+1):
		if use_response:
			response()
		result = remove_trailing_spaces_on_line(sourceview, line)
		if result:
			affected_lines.append(line)
	sourcebuffer.end_user_action()
	sourceview.set_property("editable", True)
	return affected_lines

def remove_trailing_spaces_on_line(sourceview, line_number):
	"""
	Convert beginning tab characters to space characters on a line.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@param line_number: The line to perform conversion operation on.
	@type line_number: An Integer object.

	@return: True if the line was converted.
	@rtype: An Boolean object.
	"""
	sourcebuffer = sourceview.get_property("buffer")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	transition_position.forward_to_line_end()
	if transition_position.equal(begin_position):
		return False
	while True:
		transition_position.backward_char()
		if not transition_position.get_char() in (" ", "\t"):
			transition_position.forward_char()
			break
	if transition_position.equal(end_position):
		return False
	sourcebuffer.delete(transition_position, end_position)
	return True
