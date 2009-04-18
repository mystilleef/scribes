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

SUBDIRS = . GUI URILoader SaveSystem SaveProcess

scribes_PYTHON = \
	Globals.py \
	__init__.py \
	BarObjectManager.py \
	BusyManager.py \
	ColorThemeMetadata.py \
	CommandLineInfo.py \
	CommandLineProcessor.py \
	ContentDetector.py \
	CursorMetadata.py \
	DBusService.py \
	DialogFilters.py \
	DisplayRightMarginMetadata.py \
	Editor.py \
	EditorImports.py \
	EncodingComboBoxDataManager.py \
	EncodingErrorComboBox.py \
	EncodingErrorManager.py \
	EncodingErrorOpenButton.py \
	EncodingErrorCloseButton.py \
	EncodingErrorLoader.py \
	EncodingErrorTitleLabel.py \
	EncodingErrorWindow.py \
	EncodedFilesMetadata.py \
	EncodingGuessListMetadata.py \
	EncodingManager.py \
	EncodingMetadata.py \
	Exceptions.py \
	FileModificationMonitor.py \
	FileSaver.py \
	FontMetadata.py \
	ForkScribesMetadata.py \
	FullScreenManager.py \
	GladeObjectManager.py \
	GlobalStore.py \
	InstanceManager.py \
	i18n.py \
	LanguageManager.py \
	LanguagePluginManager.py \
	License.py \
	Main.py \
	MarginPositionMetadata.py \
	MinimalModeMetadata.py \
	OutputProcessor.py \
	OutputWriter.py \
	SaveCommunicator.py \
	SaveManager.py \
	SaveProcessMonitor.py \
	SaveProcessorDBusService.py \
	SchemeManager.py \
	ServicesInitializer.py \
	ScribesSaveProcessor.py \
	SIGNALS.py \
	SpellCheckMetadata.py \
	SupportedEncodings.py \
	SupportedEncodingsDatabaseManager.py \
	SupportedEncodingsGUIManager.py \
	SupportedEncodingsTreeView.py \
	SupportedEncodingsWindow.py \
	PluginSystemInitializer.py \
	PositionMetadata.py \
	TabWidthMetadata.py \
	TextWrappingMetadata.py \
	Trigger.py \
	TriggerManager.py \
	URIManager.py \
	PluginManager.py \
	RegistrationManager.py \
	ReadonlyManager.py \
	RecentManager.py \
	Usage.py \
	UseTabsMetadata.py \
	Utils.py \
	Word.py

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = Globals.py.in 
