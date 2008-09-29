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
This module contains functions that perform word operations. The functions are
designed to be generic and thus can be used accross this project or in any
PyGTK+ project.

For the purpose of this project, a word is a sequence of alphanumeric characters
that, optionally, may contain an underscore ("_") or a dash ("-") character.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def starts_word(iterator, pattern):
	iterator = iterator.copy()
	character = iterator.get_char()
	if not pattern.match(character): return False
	if iterator.starts_line(): return True
	iterator.backward_char()
	character = iterator.get_char()
	if pattern.match(character): return False
	return True

def ends_word(iterator, pattern):
	iterator = iterator.copy()
	if iterator.starts_line(): return False
	character = iterator.get_char()
	if pattern.match(character): return False
	iterator.backward_char()
	character = iterator.get_char()
	if pattern.match(character): return True
	return False

def inside_word(iterator, pattern):
	iterator = iterator.copy()
	if starts_word(iterator, pattern) or ends_word(iterator, pattern): return True
	character = iterator.get_char()
	if pattern.match(character): return True
	return False

def get_word_boundary(iterator, pattern):
	start = iterator.copy()
	end = iterator.copy()
	while starts_word(start, pattern) is False:
		start.backward_char()
	while ends_word(end, pattern) is False:
		end.forward_char()
	return start, end
