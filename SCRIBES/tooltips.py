# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
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
All tooltips for Scribes are contained in this module.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com

"""


from internationalization import msg0097, msg0098, msg0099, msg0100, msg0101
from internationalization import msg0102, msg0103, msg0104, msg0105, msg0106
from internationalization import msg0107, msg0108, msg0109, msg0110, msg0111
from internationalization import msg0112, msg0113, msg0114, msg0115, msg0116
from internationalization import msg0117, msg0118, msg0119, msg0120, msg0121
from internationalization import msg0314, msg0315, msg0316, msg0317, msg0318
from internationalization import msg0319, msg0320, msg0326, msg0327, msg0328
from internationalization import msg0435, msg0447, msg0460


# Tooltips for the toolbar buttons
new_button_tip = msg0097 + " (Ctrl - n)"
open_button_tip = msg0098 + " (Ctrl - o)"
save_button_tip = msg0099 + " (Ctrl - Shift - s)"
print_button_tip = msg0100 + " (Ctrl - p)"
undo_button_tip = msg0101 + " (Ctrl - z)"
redo_button_tip = msg0102 + " (Ctrl - Shift -z)"
find_button_tip = msg0103 + " (Ctrl - f)"
replace_button_tip = msg0104 + " (Ctrl - r)"
goto_button_tip = msg0105 + " (Ctrl - i)"
pref_button_tip = msg0106 + " (F12)"
help_button_tip = msg0107 + " (F1)"
arrow_button_tip = msg0326

# Tooltips for the recent menu
recent_menu_tip = msg0460
# Tooltips for the preferences menu
color_button_tip = msg0327
template_button_tip = msg0328

# Tooltips for the findbar
previous_button_tip = msg0108
next_button_tip = msg0109
match_case_button_tip = msg0110
match_word_button_tip = msg0111
entry_tip = msg0112

# Tooltips for the replacebar

replace_entry_tip = msg0113
replace_button_tips = msg0114
replaceall_button_tip = msg0115

# Tooltips for the preference dialog
font_button_tip = msg0116
tab_spin_button_tip = msg0117
tab_check_button_tip = msg0435
tw_check_button_tip = msg0118
margin_check_button_tip = msg0119
margin_spin_button_tip = msg0120
spell_check_button_tip = msg0121

# Tooltips for the color editor.
theme_check_button_tip = msg0314
foreground_button_tip = msg0315
background_button_tip = msg0316
syntax_button_tip = msg0317
bold_check_button_tip = msg0318
italic_check_button_tip = msg0319
reset_button_tip = msg0320
underline_check_button_tip = msg0447

def create_tooltips():
	"""
	Create a tooltip object

	@return: a tooltip object
	@rtype: GTK Tooltips
	"""

	from gtk import Tooltips
	tips = Tooltips()
	tips.enable()

	return tips

