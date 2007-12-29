edit = sed \
	-e 's,@pixmapsdir\@,$(pixmapsdir),g' \
	-e 's,@scribes_prefix\@,$(prefix),g' \
	-e 's,@scribes_data_path\@,$(datadir),g' \
	-e 's,@scribes_sysconfdir\@,$(sysconfdir),g' \
	-e 's,@python_path\@,$(pythondir),g' \
	-e 's,@VERSION\@,$(VERSION),g'

# dnl Generate "info.py" from "info.py.in."
python_files = info.py
python_in_files = $(python_files).in
scribesdir = $(pythondir)/SCRIBES

$(python_files): Makefile $(python_in_files)
	rm -f $(python_files) $(python_files).tmp
	$(edit) $(python_in_files) > $(python_files).tmp
	mv $(python_files).tmp $(python_files)
	if [ -d $(scribesdir) ]; then \
		echo "removing " $(scribesdir) ;\
		rm -rf $(scribesdir) ;\
		echo "removed " $(scribesdir) ;\
	fi

scribes_PYTHON = \
	info.py \
	__init__.py \
	bar.py \
	commandline.py \
	cursor.py \
	cursor_metadata.py \
	dialog.py \
	dialogfilter.py \
	DBusService.py \
	edialog.py \
	Editor.py \
	EncodingManager.py \
	ErrorDialog.py \
	encoding_metadata.py \
	encodingbox.py \
	encodingdialog.py \
	error.py \
	escape.py \
	Exceptions.py \
	Feedback.py \
	FileSaver.py \
	FileLoader.py \
	FileModificationMonitor.py \
	FontMetadata.py \
	fsbutton.py \
	GlobalStore.py \
	InstanceManager.py \
	internationalization.py \
	license.py \
	lines.py \
	Main.py \
	MessageDialog.py \
	MainContainer.py \
	ModificationDialog.py \
	NewFileSaver.py \
	mdialog.py \
	OutputProcessor.py \
	OutputWriter.py \
	popupsubmenu.py \
	position_metadata.py \
	PreferenceMenu.py \
	PluginManager.py \
	RecentManager.py \
	RecentMenu.py \
	sdialog.py \
	SaveProcessMonitor.py \
	SaveProcessorDBusService.py \
	ScribesSaveProcessor.py \
	StatusContainer.py \
	syntax.py \
	Spinner.py \
	StatusBar.py \
	Store.py \
	TabWidthMetadata.py \
	TextBuffer.py \
	TextView.py \
	Toolbar.py \
	ToolbarContainer.py \
	toolbuttons.py \
	tooltips.py \
	Trigger.py \
	TriggerManager.py \
	txtutils.py \
	UseTabsMetadata.py \
	usage.py \
	utils.py \
	ViewContainer.py \
	Window.py \
	word.py
EXTRA_DIST = info.py.in
