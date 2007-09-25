class Error(Exception):
	pass

class FileNotFoundError(Error):
	pass

class InvalidFileError(Error):
	pass

class ValidationError(Error):
	pass

class ExportPermissionError(Error):
	pass

class ExportSelectionError(Error):
	pass

class EntryError(Error):
	pass

class SameTriggerError(Error):
	pass

class DragDropError(Error):
	pass

class NoDataError(Error):
	pass
