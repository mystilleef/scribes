from SCRIBES.SignalConnectionManager import SignalManager
from operator import itemgetter
import gtk
import pango

class ShortcutWindow(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __shortcutWindow(self):
		# Tests if shortcut window already exists from previous view
		# If so, just show it instead of re-creating it
		# Prevents memory leaks (tested) & instant access after init
		try:
			if self.window:
				# Window already exists, show it
				self.__show()
		except:
			# Window does not exist, create it
			self.__createShortcutWindow()
		return False

	def __createShortcutWindow(self):

		# Colors
		self.textcolor = gtk.gdk.color_parse("white")
		self.highlightcolor = gtk.gdk.color_parse("yellow")
		self.windowcolor = gtk.gdk.color_parse('#000000')

		# Padding
		self.box_padding = "    "

		# Create shortcut top
		shortcut_top = self.__createShortcutTop()

		# Create shortcut table
		shortcut_table = self.__createShortcutTable()

		# Create window box
		windowbox = gtk.VBox()
		# Pack window box
		windowbox.pack_start(shortcut_top)
		windowbox.pack_start(shortcut_table)

		# Create Window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#		self.window.set_default_size(800, 600)

		# Set window opacity
		self.window.set_opacity(0.95)

		# Add Window Title (just incase)
		self.window.set_title("Shortcuts")

		# Turn Off Window Decoration
		self.window.set_decorated(False)

		# Bind with Scribes' window
		self.window.set_transient_for(self.__editor.window)
		self.window.set_destroy_with_parent(True)
		self.window.set_property("skip-taskbar-hint", True)

		self.window.add(windowbox)
		from gtk import WIN_POS_CENTER_ALWAYS
		self.window.set_position(WIN_POS_CENTER_ALWAYS)

		self.window.connect('key-press-event', self.__event_cb)

		# hides help window when focus changes to something else
#		self.window.connect('focus-out-event', self.__hide_cb)

		# show window
		self.__show()

		# Prints to stdout triggers with missing information
		#self.__getShortcutsMissing()

		return False

	def __createShortcutTable(self):

		# Widgets
		tablebox = gtk.HBox()
		table_columns = 3
		table = gtk.Table(1,table_columns, False)

		# Create left & right tablebox padding
		mb_buf_left = self.__setTextBuffer(self.box_padding)
		mb_view_left = self.__setTextView(mb_buf_left, self.textcolor)
		mb_buf_right = self.__setTextBuffer(self.box_padding)
		mb_view_right = self.__setTextView(mb_buf_right, self.textcolor)

		# Add left tablebox padding
		tablebox.pack_start(mb_view_left)

		# Category & Column Properties
		category_check = ""
		column_cutoff = 20 # len after which no new categories will be created
		column_count = 0
		separator = " : "
		self.key_separator = "+"
		self.table_rows = 0 # used for table expanding

		shortcuts = self.__getShortcutsSorted()

		for s in shortcuts:
			self.__editor.refresh(False)
			# Strip whitespaces
			name = s[0].strip()
			key = s[1].strip()
			cat = s[2].strip()

			if cat != category_check:
				# Create new catagory group

				if column_count > column_cutoff:
					# Padding to fill in missing space on bottom (if needed)
					# Make room for bottom column padding
					self.table_rows = self.table_rows + 1
					table.resize(self.table_rows, table_columns)

					# Setup bottom padding view
					padbuf = self.__setTextBuffer("")
					botview = self.__setTextView(padbuf, self.textcolor)

					# Add bottom padding view
					table.attach(botview, 0, 3, self.table_rows - 1, self.table_rows, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)


					# Add previously created column (old table)
					tablebox.pack_start(table)

					# Create new column (new table)
					table = gtk.Table(1,table_columns, False)

					# Reset table rows
					self.table_rows = 0

					# Reset column count
					column_count = 0

				# Set category_check to current category
				category_check = cat

				# Make room for column padding
				self.table_rows = self.table_rows + 1
				table.resize(self.table_rows, table_columns)

				# Setup padding view
				padbuf = self.__setTextBuffer("")
				padview = self.__setTextView(padbuf, self.textcolor)

				# Add padding view
				table.attach(padview, 0, 3, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)

				# Setup catagory view
				catbuf = self.__setTextBuffer(cat)
				self.__setTags(catbuf, gtk.JUSTIFY_LEFT)
				catview = self.__setTextView(catbuf, self.highlightcolor)

				# Setup blank key view
				blankbuf = self.__setTextBuffer("")
				blankview = self.__setTextView(blankbuf, self.textcolor)

				# Make room for title
				self.table_rows = self.table_rows + 1
				table.resize(self.table_rows, table_columns)

				# Add catagory title view
				# (child, left_attach, right_attach, top_attach, bottom_attach)
				table.attach(catview, 2, 3, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)

				# Add blank view
				table.attach(blankview, 0, 2, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)
				self.__editor.refresh(False)
			# Setup key view
			keybuf = self.__setTextBuffer(key)
			self.__setTags(keybuf, gtk.JUSTIFY_RIGHT)
			self.__formatKey(keybuf)
			keyview = self.__setTextView(keybuf, self.highlightcolor)

			# Setup separator view
			sepbuf = self.__setTextBuffer(separator)
			sepview = self.__setTextView(sepbuf, self.textcolor)

			# Setup name view
			namebuf = self.__setTextBuffer(name)
			self.__setTags(namebuf, gtk.JUSTIFY_LEFT)
			nameview = self.__setTextView(namebuf, self.textcolor)

			# Make room for views
			self.table_rows = self.table_rows + 1
			table.resize(self.table_rows, table_columns)

			# Add views
			table.attach(keyview, 0, 1, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)
			table.attach(sepview, 1, 2, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)
			table.attach(nameview, 2, 3, self.table_rows - 1, self.table_rows, xoptions=gtk.FILL, yoptions=gtk.FILL)

			# Set column count
			column_count = column_count + 1
			self.__editor.refresh(False)
		# Padding to fill in missing space on bottom (when needed)
		# Make room for bottom column padding
		self.table_rows = self.table_rows + 1
		table.resize(self.table_rows, table_columns)

		# Setup bottom padding view
		padbuf = self.__setTextBuffer("")
		botview = self.__setTextView(padbuf, self.textcolor)

		# Add bottom padding view
		table.attach(botview, 0, 3, self.table_rows - 1, self.table_rows, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL)

		# Add the remaining column
		tablebox.pack_start(table)

		# Add right tablebox padding
		tablebox.pack_start(mb_view_right)

		return tablebox

	def __createShortcutTop(self):
		# Widgets
		topbox = gtk.VBox()
		textbox = gtk.HBox()

		# Text
		title = self.box_padding + "Scribes Keyboard Shortcuts"
		link = "show user guide" + self.box_padding

		# Create views
		titleview = self.__createTitleView(title)
		linkview = self.__createLinkView(link)

		# Setup padding view
		padbuf = self.__setTextBuffer(" ")
		padview = self.__setTextView(padbuf, self.textcolor)

		# Pack text views
		textbox.pack_start(titleview)
		textbox.pack_start(linkview)

		# Pack topbox
		topbox.pack_start(padview)
		topbox.pack_start(textbox)

		return topbox

	def __createLinkView(self, text):
		# Setup  buffer
		buf = self.__setTextBuffer(text)
		self.__setTags(buf, gtk.JUSTIFY_RIGHT)

		# Get link word count
		text_split = text.split()
		word_count = len(text_split)

		# Setup  buffer text format tags
		start = buf.get_start_iter()
		end = start.copy()
		end.forward_word_ends(word_count)
		tag = buf.create_tag(weight=pango.WEIGHT_BOLD)
		tag = buf.create_tag(underline=pango.UNDERLINE_SINGLE)
		buf.apply_tag(tag, start, end)

		# Setup view
		view = gtk.TextView(buf)
		view.set_editable(False) # Disable editability
		view.set_cursor_visible(False) # Disable mouse cursor
		view.modify_base(gtk.STATE_NORMAL, self.windowcolor)
		view.modify_text(gtk.STATE_NORMAL, self.highlightcolor)

		# Setup connect "link"
		view.connect('button-press-event', self.__openHelp_cb)

		return view

	def __createTitleView(self, text):
		# Setup buffer
		buf = self.__setTextBuffer(text)
		self.__setTags(buf, gtk.JUSTIFY_LEFT)
		# Setup buffer text format tags
		start = buf.get_start_iter()
		end = buf.get_end_iter()
		tag = buf.create_tag(weight=pango.WEIGHT_BOLD)
		tag = buf.create_tag(scale=pango.SCALE_LARGE)
		buf.apply_tag(tag, start, end)
		# Setup view
		view = self.__setTextView(buf, self.textcolor)
		return view

	def __getShortcuts(self):
		# create a shortcut list
		#
		# each trigger is an entry in the shortcut list
		# one shortcut list that contains a tuple for every trigger
		# every trigger tuple contains trigger name, accel, cat, and desc
		#
		# trigger tuple format:
		#	name, shortcut, category, description
		triggerlist = self.__editor.triggers
		shortcuts = []
		for trigger in triggerlist:
			self.__editor.refresh(False)
			# Create tuple of format: name, accel, category, desc
			trigger_tuple = (
				self.__formatName(trigger.name),
				self.__formatAccel(trigger.accelerator),
				trigger.category,
				trigger.description
			)
			shortcuts.append(trigger_tuple)
			self.__editor.refresh(False)
		from Utils import DEFAULT_TRIGGERS
		return shortcuts + DEFAULT_TRIGGERS

	def __getShortcutsSorted(self):
		# sort according to category, shortcut
		# 	format:
		#		name	shortcut	category	description
		#		0		1			2			3
		shortcuts = self.__cleanShortcuts()
		shortcuts_sorted = sorted(shortcuts, key=itemgetter(2,1))
		return shortcuts_sorted

	def __cleanShortcuts(self):
		cleaned = []
		s = self.__getShortcuts()
		for e in s:
			self.__editor.refresh(False)
			if e[0] and e[1] and e[2] and e[3]: cleaned.append(e)
			self.__editor.refresh(False)
		return cleaned

	def __getShortcutsMissing(self):
		# print information for all shortcuts missing an entry
		 # 0 = name, 1 = shortcut, 2 = category, 3 = description
		shortcuts = self.__getShortcuts()
		for e in shortcuts:
			self.__editor.refresh(False)
			# check if anything is missing
			if not e[0] or not e[1] or not e[2] or not e[3]:
				if e[0]:
					print e[0] + " is:"
				else:
					print "name missing!"
					if e[1]:
						print "(shortcut " + e[1] + ")"
				if not e[1]:
					print "missing shortcut"
				if not e[2]:
					print "missing category"
				if not e[3]:
					print "missing description"
				print "-----"
			self.__editor.refresh(False)

	def __setTextBuffer(self, text):
		textbuf = gtk.TextBuffer()
		textbuf.set_text(text)
		return textbuf

	def __setTags(self, textbuf, justify):
		# Tags to justify
		# justify = gtk.JUSTIFY_RIGHT or gtk.JUSTIFY_LEFT
		start = textbuf.get_start_iter()
		end = textbuf.get_end_iter()

		tag = textbuf.create_tag(justification=justify)

		textbuf.apply_tag(tag, start, end)

		return textbuf

	def __formatKey(self, textbuf):
		# Tags to format key separator
		iter_start = textbuf.get_start_iter()
		iter_end = textbuf.get_end_iter()

		# Make sure separator exists
		text = iter_start.get_visible_text(iter_end)
		text_count = text.count(self.key_separator)
		if text_count > 0:
			# Get start and end iter's of separator
			start, end = iter_start.forward_search(self.key_separator, gtk.TEXT_SEARCH_TEXT_ONLY)

			tag = textbuf.create_tag(foreground_gdk=self.textcolor)

			textbuf.apply_tag(tag, start, end)

		return textbuf

	def __setTextView(self, textbuf, textcolor):
		# Create textview
		textview = gtk.TextView(textbuf)

		# Disable editability
		textview.set_editable(False)

		# Disable mouse cursor
		textview.set_cursor_visible(False)

		# Set texview base color
		textview.modify_base(gtk.STATE_NORMAL, self.windowcolor)

		# Set textview text color
		textview.modify_text(gtk.STATE_NORMAL, textcolor)

		# close help window on mouse button press
		# textview.connect('button-press-event', self.__hide_cb)

		return textview

	def __formatAccel(self, accel):
		accel_str = str(accel)
		accel_str = accel_str.replace("<", "")
		format = accel_str.replace(">", "+")
#		format = self.__rreplace(accel_str, ">", "> + ", 1)
		return format

	def __formatName(self, name):
		name_str = str(name)
		format = name_str.replace("_", " ")
		format = format.replace("-", " ")
		format = format.title()
		return format

	def __rreplace(self, s, old, new, occurance):
		# replaces old with new n-occurances from the LAST occurance
		li = s.rsplit(old, occurance)
		return new.join(li)

	def __show(self):
		self.window.show_all()
		return True

	def __hide(self):
		self.window.hide()
		return True

	def __openHelp(self):
		self.__editor.help()
		return

	def __event_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval == Escape : self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return True

	def __hide_cb(self, *args):
		self.__hide()
		return True

	def __openHelp_cb(self, *args):
		self.__openHelp()
		self.__hide()
		return True

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate_cb(self, *args):
		self.__shortcutWindow()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
