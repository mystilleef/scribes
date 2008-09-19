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
Translatable strings for Scribes.

This modules contains user visible string eligible for translation. The strings
are defined by a unique identifier or format:

	msgXXXX = u"string eligible for translation"

XXXX is a number between 0001 and 9999.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gettext import gettext as _

# From module accelerators.py
msg0003 = _("Cannot redo action")#.decode(encoding).encode("utf-8")


msg0024 = _("Leave Fullscreen")#.decode(encoding).encode("utf-8")

# From module editor_ng.py, fileloader.py, timeout.py
msg0025 = _("Unsaved Document")#.decode(encoding).encode("utf-8")

# From module filechooser.py

msg0027 = _("All Documents")#.decode(encoding).encode("utf-8")
msg0028 = _("Python Documents")#.decode(encoding).encode("utf-8")
msg0029 = _("Text Documents")#.decode(encoding).encode("utf-8")

# From module fileloader.py
msg0030 = _('Loaded file "%s"')#.decode(encoding).encode("utf-8")
msg0032 = _("Loading file please wait...")#.decode(encoding).encode("utf-8")
# From module fileloader.py, savechooser.py
msg0034 = _(" <READONLY>")#.decode(encoding).encode("utf-8")

# From module main.py
msg0038 = _("Unrecognized option: '%s'")#.decode(encoding).encode("utf-8")
msg0039 = _("Try 'scribes --help' for more information")#.decode(encoding).encode("utf-8")
msg0040 = _("Scribes only supports using one option at a time")#.decode(encoding).encode("utf-8")
msg0042 = _("Scribes version %s")#.decode(encoding).encode("utf-8")
msg0043 = _("%s does not exist")#.decode(encoding).encode("utf-8")

# From module timeout.py
msg0044 = _('The file "%s" is open in readonly mode')#.decode(encoding).encode("utf-8")
msg0045 = _('The file "%s" is open')#.decode(encoding).encode("utf-8")

msg0085 = _('Saved "%s"')#.decode(encoding).encode("utf-8")

msg0089 = _("Copied selected text")#.decode(encoding).encode("utf-8")
msg0090 = _("No selection to copy")#.decode(encoding).encode("utf-8")
msg0091 = _("Cut selected text")#.decode(encoding).encode("utf-8")
msg0092 = _(u"No selection to cut")#.decode(encoding).encode("utf-8")
msg0093 = _("Pasted copied text")#.decode(encoding).encode("utf-8")
msg0094 = _("No text content in the clipboard")#.decode(encoding).encode("utf-8")

# From module tooltips.py
msg0097 = _("Open a new window")#.decode(encoding).encode("utf-8")
msg0098 = _("Open a file")#.decode(encoding).encode("utf-8")
msg0099 = _("Rename the current file")#.decode(encoding).encode("utf-8")
msg0100 = _("Print the current file")#.decode(encoding).encode("utf-8")
msg0101 = _("Undo last action")#.decode(encoding).encode("utf-8")
msg0102 = _("Redo undone action")#.decode(encoding).encode("utf-8")
msg0103 = _("Search for text")#.decode(encoding).encode("utf-8")
msg0104 = _("Search for and replace text")#.decode(encoding).encode("utf-8")
msg0105 = _("Go to a specific line")#.decode(encoding).encode("utf-8")
msg0106 = _("Configure the editor")#.decode(encoding).encode("utf-8")
msg0107 = _("Launch the help browser")#.decode(encoding).encode("utf-8")
msg0108 = _("Search for previous occurrence of the string")#.decode(encoding).encode("utf-8")
msg0109 = _("Search for next occurrence of the string")#.decode(encoding).encode("utf-8")
msg0110 = _("Find occurrences of the string that match upper and lower cases \
only")#.decode(encoding).encode("utf-8")
msg0111 = _("Find occurrences of the string that match the entire word only")#.decode(encoding).encode("utf-8")
msg0112 = _("Type in the text you want to search for")#.decode(encoding).encode("utf-8")
msg0113 = _("Type in the text you want to replace with")#.decode(encoding).encode("utf-8")
msg0114 = _("Replace the selected found match")#.decode(encoding).encode("utf-8")
msg0115 = _("Replace all found matches")#.decode(encoding).encode("utf-8")
msg0116 = _("Click to specify the font type, style, and size to use for text.")#.decode(encoding).encode("utf-8")
msg0117 = _("Click to specify the width of the space that is inserted when \
you press the Tab key.")#.decode(encoding).encode("utf-8")
msg0118 = _("Select to wrap text onto the next line when you reach the \
text window boundary.")#.decode(encoding).encode("utf-8")
msg0119 = _("Select to display a vertical line that indicates the right \
margin.")#.decode(encoding).encode("utf-8")
msg0120 = _("Click to specify the location of the vertical line.")#.decode(encoding).encode("utf-8")
msg0121 = _("Select to enable spell checking")#.decode(encoding).encode("utf-8")


# From module usage.py
msg0124 = _("A text editor for GNOME.")#.decode(encoding).encode("utf-8")
msg0125 = _("usage: scribes [OPTION] [FILE] [...]")#.decode(encoding).encode("utf-8")
msg0126 = _("Options:")#.decode(encoding).encode("utf-8")
msg0127 = _("display this help screen")#.decode(encoding).encode("utf-8")
msg0128 = _("output version information of Scribes")#.decode(encoding).encode("utf-8")
msg0129 = _("create a new file and open the file with Scribes")#.decode(encoding).encode("utf-8")
msg0130 = _("get debuggin information for scribes")#.decode(encoding).encode("utf-8")

# From error.py
msg0133 = _("error")#.decode(encoding).encode("utf-8")

# From module actions.py
msg0145 = _("Cannot perform operation in readonly mode")#.decode(encoding).encode("utf-8")

# From encoding.py
msg0157 = _("Character _Encoding: ")#.decode(encoding).encode("utf-8")
msg0158 = _("Add or Remove Encoding ...")#.decode(encoding).encode("utf-8")
msg0159 = _("Recommended (UTF-8)")#.decode(encoding).encode("utf-8")
msg0160 = _("Add or Remove Character Encoding")#.decode(encoding).encode("utf-8")
msg0161 = _("Language and Region")#.decode(encoding).encode("utf-8")
msg0162 = _("Character Encoding")#.decode(encoding).encode("utf-8")
msg0163 = _("Select")#.decode(encoding).encode("utf-8")

# From filechooser.py
msg0187 = _("Closed dialog window")#.decode(encoding).encode("utf-8")

# From encoding.py
msg0208 = _("English")#.decode(encoding).encode("utf-8")
msg0209 = _("Traditional Chinese")#.decode(encoding).encode("utf-8")
msg0210 = _("Traditional Chinese")#.decode(encoding).encode("utf-8")
msg0211 = _("English")#.decode(encoding).encode("utf-8")
msg0212 = _("Hebrew")#.decode(encoding).encode("utf-8")
msg0213 = _("English")#.decode(encoding).encode("utf-8")
msg0214 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0215 = _("Greek")#.decode(encoding).encode("utf-8")
msg0216 = _("Baltic languages")#.decode(encoding).encode("utf-8")
msg0217 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0218 = _("Central and Eastern Europe")#.decode(encoding).encode("utf-8")
msg0219 = _("Bulgarian, Macedonian, Russian, Serbian")#.decode(encoding).encode("utf-8")
msg0220 = _("Hebrew")#.decode(encoding).encode("utf-8")
msg0221 = _("Turkish")#.decode(encoding).encode("utf-8")
msg0222 = _("Portuguese")#.decode(encoding).encode("utf-8")
msg0223 = _("Icelandic")#.decode(encoding).encode("utf-8")
msg0224 = _("Hebrew")#.decode(encoding).encode("utf-8")
msg0225 = _("Canadian")#.decode(encoding).encode("utf-8")
msg0226 = _("Arabic")#.decode(encoding).encode("utf-8")
msg0227 = _("Danish, Norwegian")#.decode(encoding).encode("utf-8")
msg0228 = _("Russian")#.decode(encoding).encode("utf-8")
msg0229 = _("Greek")#.decode(encoding).encode("utf-8")
msg0230 = _("Thai")#.decode(encoding).encode("utf-8")
msg0231 = _("Greek")#.decode(encoding).encode("utf-8")
msg0232 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0233 = _("Korean")#.decode(encoding).encode("utf-8")
msg0234 = _("Traditional Chinese")#.decode(encoding).encode("utf-8")
msg0235 = _("Urdu")#.decode(encoding).encode("utf-8")
msg0236 = _("Turkish")#.decode(encoding).encode("utf-8")
msg0237 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0238 = _("Central and Eastern Europe")#.decode(encoding).encode("utf-8")
msg0239 = _("Bulgarian, Macedonian, Russian, Serbian")#.decode(encoding).encode("utf-8")
msg0240 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0241 = _("Greek")#.decode(encoding).encode("utf-8")
msg0242 = _("Turkish")#.decode(encoding).encode("utf-8")
msg0243 = _("Hebrew")#.decode(encoding).encode("utf-8")
msg0244 = _("Arabic")#.decode(encoding).encode("utf-8")
msg0245 = _("Baltic languages")#.decode(encoding).encode("utf-8")
msg0246 = _("Vietnamese")#.decode(encoding).encode("utf-8")
msg0247 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0248 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0249 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0250 = _("Korean")#.decode(encoding).encode("utf-8")
msg0251 = _("Simplified Chinese")#.decode(encoding).encode("utf-8")
msg0252 = _("Unified Chinese")#.decode(encoding).encode("utf-8")
msg0253 = _("Unified Chinese")#.decode(encoding).encode("utf-8")
msg0254 = _("Simplified Chinese")#.decode(encoding).encode("utf-8")
msg0255 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0256 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0257 = _("Japanese, Korean, Simplified Chinese")#.decode(encoding).encode("utf-8")
msg0258 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0259 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0260 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0261 = _("Korean")#.decode(encoding).encode("utf-8")
msg0262 = _("West Europe")#.decode(encoding).encode("utf-8")
msg0263 = _("Central and Eastern Europe")#.decode(encoding).encode("utf-8")
msg0264 = _("Esperanto, Maltese")#.decode(encoding).encode("utf-8")
msg0265 = _("Baltic languagues")#.decode(encoding).encode("utf-8")
msg0266 = _("Bulgarian, Macedonian, Russian, Serbian")#.decode(encoding).encode("utf-8")
msg0267 = _("Arabic")#.decode(encoding).encode("utf-8")
msg0268 = _("Greek")#.decode(encoding).encode("utf-8")
msg0269 = _("Hebrew")#.decode(encoding).encode("utf-8")
msg0270 = _("Turkish")#.decode(encoding).encode("utf-8")
msg0271 = _("Nordic languages")#.decode(encoding).encode("utf-8")
msg0272 = _("Baltic languages")#.decode(encoding).encode("utf-8")
msg0273 = _("Celtic languages")#.decode(encoding).encode("utf-8")
msg0274 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0275 = _("Korean")#.decode(encoding).encode("utf-8")
msg0276 = _("Russian")#.decode(encoding).encode("utf-8")
msg0277 = _("Ukrainian")#.decode(encoding).encode("utf-8")
msg0278 = _("Bulgarian, Macedonian, Russian, Serbian")#.decode(encoding).encode("utf-8")
msg0279 = _("Greek")#.decode(encoding).encode("utf-8")
msg0280 = _("Icelandic")#.decode(encoding).encode("utf-8")
msg0281 = _("Central and Eastern Europe")#.decode(encoding).encode("utf-8")
msg0282 = _("Western Europe")#.decode(encoding).encode("utf-8")
msg0283 = _("Turkish")#.decode(encoding).encode("utf-8")
msg0284 = _("Kazakh")#.decode(encoding).encode("utf-8")
msg0285 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0286 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0287 = _("Japanese")#.decode(encoding).encode("utf-8")
msg0288 = _("All languages")#.decode(encoding).encode("utf-8")
msg0289 = _("All Languages (BMP only)")#.decode(encoding).encode("utf-8")
msg0290 = _("All Languages (BMP only)")#.decode(encoding).encode("utf-8")
msg0291 = _("All Languages")#.decode(encoding).encode("utf-8")
msg0292 = _("None")#.decode(encoding).encode("utf-8")

# From tooltips.py
msg0314 = _("Select to use themes' foreground and background colors")#.decode(encoding).encode("utf-8")
msg0315 = _("Click to choose a new color for the editor's text")#.decode(encoding).encode("utf-8")
msg0316 = _("Click to choose a new color for the editor's background")#.decode(encoding).encode("utf-8")
msg0317 = _("Click to choose a new color for the language syntax element")#.decode(encoding).encode("utf-8")
msg0318 = _("Select to make the language syntax element bold")#.decode(encoding).encode("utf-8")
msg0319 = _("Select to make the language syntax element italic")#.decode(encoding).encode("utf-8")
msg0320 = _("Select to reset the language syntax element to its default \
settings")#.decode(encoding).encode("utf-8")

# From syntaxcoloreditor.py


# From readonly.py
msg0322 = _("Toggled readonly mode on")#.decode(encoding).encode("utf-8")
msg0324 = _("Toggled readonly mode off")#.decode(encoding).encode("utf-8")

# From tooltips.py
msg0326 = _("Menu for advanced configuration")#.decode(encoding).encode("utf-8")
msg0327 = _("Configure the editor's foreground, background or syntax colors")#.decode(encoding).encode("utf-8")
msg0328 = _("Create, modify or manage templates")#.decode(encoding).encode("utf-8")

# From cursor.py
msg0329 = _("Ln %d col %d")#.decode(encoding).encode("utf-8")

# From fileloader.py
msg0335 = _("Loading \"%s\"...")

# From dialogfilter.py
msg0343 = _("Ruby Documents")
msg0344 = _("Perl Documents")
msg0345 = _("C Documents")
msg0346 = _("C++ Documents")
msg0347 = _("C# Documents")
msg0348 = _("Java Documents")
msg0349 = _("PHP Documents")
msg0350 = _("HTML Documents")
msg0351 = _("XML Documents")
msg0352 = _("Haskell Documents")
msg0353 = _("Scheme Documents")

msg0354 = _("INS")
msg0355 = _("OVR")

msg0428 = _("No bookmarks found")
msg0435 = _("Use spaces instead of tabs for indentation")
msg0447 = _("Select to underline language syntax element")
msg0460 = _("Open recently used files")
msg0468 = _("Failed to save file")

msg0469 = _("Save Error: You do not have permission to modify this file \
or save to its location.")
msg0470 = _("Save Error: Failed to transfer file from swap to permanent location.")
msg0471 = _("Save Error: Failed to create swap location or file.")
msg0472 = _("Save Error: Failed to create swap file for saving.")
msg0473 = _("Save Error: Failed to write swap file for saving.")
msg0474 = _("Save Error: Failed to close swap file for saving.")
msg0475 = _("Save Error: Failed decode contents of file from \"UTF-8\" to Unicode.")
msg0476 = _("Save Error: Failed to encode contents of file. Make sure \
the encoding of the file is properly set in the save dialog. Press \
(Ctrl - s) to show the save dialog.")

msg0477 = _("File: %s")
msg0478 = _("Failed to load file.")
msg0479 = _("Load Error: You do not have permission to view this file.")
msg0480 = _("Load Error: Failed to access remote file for permission reasons.")
msg0481 = _("Load Error: Failed to get file information for loading. \
Please try loading the file again.")
msg0482 = _("Load Error: File does not exist.")
msg0483 = _("Damn! Unknown Error")
msg0484 = _("Load Error: Failed to open file for loading.")
msg0485 = _("Load Error: Failed to read file for loading.")
msg0486 = _("Load Error: Failed to close file for loading.")
msg0487 = _("Load Error: Failed to decode file for loading. The file \
your are loading may not be a text file. If you are sure it is a text \
file, try to open the file with the correct encoding via the open \
dialog. Press (control - o) to show the open dialog.")
msg0488 = _("Load Error: Failed to encode file for loading. Try to \
open the file with the correct encoding via the open dialog. Press \
(control - o) to show the open dialog.")

msg0489 = _("Reloading %s")
msg0490 = _("'%s' has been modified by another program")
