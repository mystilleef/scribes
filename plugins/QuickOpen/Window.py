import os
import gtk
from gtk import Dialog
from gettext import gettext as _
STATUS_MESSAGE = _("Quickly Open Files")

class QuickOpenWindow(Dialog) :

	def __init__(self, editor) :
		self.__editor = editor
		Dialog.__init__(self)
		self.build()
		self.__signal_id_1 = self.connect("close", self.__close_cb)
		self.__signal_id_2 = self.connect("response", self.__close_cb)
		self.cancel_button.connect("clicked", self.hide_dialog)
		self.open_button.connect("clicked", self.open_selected_file)
		self.search_string_entry.connect("key-release-event", self.on_pattern_entry)
		self.hit_list.connect("select-cursor-row", self.on_select_from_list)
		self.hit_list.connect("button_press_event", self.on_list_mouse)
		self.max_result = 50

	def show_dialog(self) :
		self.__editor.busy()
		self.__editor.set_message(STATUS_MESSAGE, "open")
		self.search_string_entry.set_text('')
		self.hit_list_store.clear()
		if self.__editor.uri and self.__editor.uri.startswith("file:///") :
			self.current_path = os.path.dirname(self.__editor.uri.replace("file:///", "/"))
			self.enable_dialog()
			self.current_path_label.set_text(self.current_path)
		else :
			self.disable_dialog()
			self.current_path = None
			self.current_path_label.set_text = "Remote or Unrecognised Path"
		self.show_all()
		self.run()
		return

	def hide_dialog(self, emitter = None) :
		self.__editor.busy(False)
		self.__editor.unset_message(STATUS_MESSAGE, "open")
		self.hide()
		return

	def enable_dialog(self) :
		self.valid_path = True
		self.search_string_entry.set_sensitive(True)
		self.open_button.set_sensitive(True)
		self.list_hidden_files.set_sensitive(True)

	def disable_dialog(self) :
		self.valid_path = False
		self.search_string_entry.set_sensitive(False)
		self.open_button.set_sensitive(False)
		self.list_hidden_files.set_sensitive(False)

	def foreach(self, model, path, iter, selected):
		self.__editor.response()
		selected.append(model.get_value(iter, 1))

	def open_selected_file(self, emitter = False) :
		selected_files = []
		uris = []
		self.hit_list.get_selection().selected_foreach(self.foreach, selected_files)
		for selected_file in selected_files:
			self.__editor.response()
			uris.append("file://%s/%s" % ( self.current_path, selected_file ))
		self.__editor.open_files(uris)
		self.hide_dialog()

	def on_pattern_entry( self, widget, event ):
		oldtitle = self.get_title().replace(" * too many hits", "")
		if event.keyval == gtk.keysyms.Return:
			self.open_selected_file( event )
			return
		if event.keyval == gtk.keysyms.Up :
			self.move_current_path_up()
		pattern = self.search_string_entry.get_text()
		pattern = pattern.replace(" ","*")
		#modify lines below as needed, these defaults work pretty well
		filefilter = " | grep -s -v \"/\.\""
		cmd = ""
		if self.list_hidden_files.get_active():
			filefilter = ""
		if len(pattern) > 0:
			cmd = "cd " + self.current_path + "; find . -maxdepth 10 -depth -type f -iwholename \"*" + pattern + "*\" " + filefilter + " | grep -v \"~$\" | head -n " + repr(self.max_result + 1) + " | sort"
			self.set_title("Searching ... ")
		else:
			self.set_title("Enter pattern ... ")
		#print cmd
		self.__editor.response()
		self.hit_list_store.clear()
		self.__editor.response()
		maxcount = 0
		hits = os.popen(cmd).readlines()
		for file in hits:
			self.__editor.response()
			file = file.rstrip().replace("./", "") #remove cwd prefix
			name = os.path.basename(file)
			self.hit_list_store.append([name, file])
			if maxcount > self.max_result:
				break
			maxcount = maxcount + 1
		if maxcount > self.max_result:
			oldtitle = oldtitle + " * too many hits"
		self.set_title(oldtitle)

		selected = []
		self.hit_list.get_selection().selected_foreach(self.foreach, selected)

		if len(selected) == 0:
			iter = self.hit_list_store.get_iter_first()
			if iter != None:
				self.hit_list.get_selection().select_iter(iter)

	def move_current_path_up(self) :
		if self.current_path == "/" : return
		self.current_path, current_dir = os.path.split(self.current_path)
		self.current_path_label.set_text(self.current_path)

	def on_list_mouse( self, widget, event ):
		if event.type == gtk.gdk._2BUTTON_PRESS:
			self.open_selected_file( event )

	#key selects from list (passthrough 3 args)
	def on_select_from_list(self, widget, event):
		self.open_selected_file(event)

	def build(self) :
		self.set_default_size(500, 400)
		self.set_property("window-position", gtk.WIN_POS_CENTER_ON_PARENT)
		self.set_keep_above(True)
		self.set_title("Quick Open")

		self.current_path_label = gtk.Label("Remote or Unrecognised Path")
		self.vbox.add(self.current_path_label)

		self.search_string_entry = gtk.Entry()
		self.vbox.add(self.search_string_entry)

		self.hit_list_store = gtk.ListStore(str, str)
		self.hit_list = gtk.TreeView(self.hit_list_store)
		col = gtk.TreeViewColumn("Name" , gtk.CellRendererText(), text=0)
		col.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		col2 = gtk.TreeViewColumn("File", gtk.CellRendererText(), text=1)
		col2.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		self.hit_list.append_column(col)
		self.hit_list.append_column(col2)
		self.hit_list.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		sw = gtk.ScrolledWindow()
		sw.add(self.hit_list)
		sw.set_property("height_request", 250)
		self.vbox.add(sw)

		self.list_hidden_files = gtk.CheckButton("Include Hidden Files")
		self.vbox.add(self.list_hidden_files)

		self.cancel_button = gtk.Button("Cancel", gtk.STOCK_CANCEL)
		self.open_button = gtk.Button("Open", gtk.STOCK_OPEN)

		self.bottom_buttons = gtk.HButtonBox()
		self.bottom_buttons.pack_end(self.cancel_button)
		self.bottom_buttons.pack_end(self.open_button)
		self.vbox.add(self.bottom_buttons)

		self.disable_dialog()

		return

	def __close_cb(self, *args) :
		self.hide_dialog()
		return False
