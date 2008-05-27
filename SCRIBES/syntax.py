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
	if not language: return False
	textbuffer.set_language(language)
	return False
