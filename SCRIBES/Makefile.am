edit = sed \
	-e 's,@pixmapsdir\@,$(pixmapsdir),g' \
	-e 's,@scribes_prefix\@,$(prefix),g' \
	-e 's,@scribes_data_path\@,$(datadir),g' \
	-e 's,@scribes_sysconfdir\@,$(sysconfdir),g' \
	-e 's,@python_path\@,$(pythondir),g' \
	-e 's,@VERSION\@,$(VERSION),g'

# dnl Generate "Globals.py" from "Globals.py.in."
python_files = Globals.py
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
	Globals.py \
	__init__.py \
	ColorThemeMetadata.py \
	CommandLineInfo.py \
	CommandLineProcessor.py \
	CursorMetadata.py \
	DBusService.py \
	DisplayRightMarginMetadata.py \
	Editor.py \
	EncodingComboBoxDataManager.py \
	EncodingErrorManager.py \
	EncodingErrorLoader.py \
	EncodedFilesMetadata.py \
	EncodingGuessListMetadata.py \
	EncodingManager.py \
	EncodingMetadata.py \
	Exceptions.py \
	FileLoader.py \
	FileSaver.py \
	FontMetadata.py \
	ForkScribesMetadata.py \
	GlobalStore.py \
	InstanceManager.py \
	i18n.py \
	License.py \
	Main.py \
	MarginPositionMetadata.py \
	MessageWindow.py \
	OutputProcessor.py \
	OutputWriter.py \
	SaveCommunicator.py \
	SaveManager.py \
	SaveProcessMonitor.py \
	SaveProcessorDBusService.py \
	ScribesSaveProcessor.py \
	SpellCheckMetadata.py \
	SupportedEncodings.py \
	PositionMetadata.py \
	TabWidthMetadata.py \
	TextWrappingMetadata.py \
	TextBuffer.py \
	TextView.py \
	Usage.py \
	UseTabsMetadata.py \
	Utils.py \
	Window.py
EXTRA_DIST = Globals.py.in
