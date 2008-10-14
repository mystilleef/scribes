class Error(Exception):
	pass

class PermissionError(Error):
	pass

class LoadFileError(Error):
	pass

class FileNotFound(Error):
	pass

class SwapError(Error):
	pass

class FileCreateError(Error):
	pass

class FileWriteError(Error):
	pass

class FileCloseError(Error):
	pass

class TransferError(Error):
	pass

class NewFileError(Error):
	pass

class DoNothingError(Error):
	pass

class FileInfoError(Error):
	pass

class GenericError(Error):
	pass

class NotFoundError(Error):
	pass

class AccessDeniedError(Error):
	pass

class OpenFileError(Error):
	pass

class ReadFileError(Error):
	pass

class CloseFileError(Error):
	pass

class GnomeVfsError(Error):
	pass

class PluginError(Error):
	pass

class FileModificationError(Error):
	pass

class PluginFolderNotFoundError(Error):
	pass

class PluginModuleValidationError(Error):
	pass

class DuplicatePluginError(Error):
	pass

class DoNotLoadError(Error):
	pass

class InvalidTriggerNameError(Error):
	pass

class InvalidLanguagePluginError(Error):
	pass
	
class DuplicateTriggerNameError(Error):
	pass

class DuplicateTriggerRemovalError(Error):
	pass

class DuplicateTriggerAcceleratorError(Error):
	pass

class GlobalStoreObjectExistsError(Error):
	pass

class GlobalStoreObjectDoesNotExistError(Error):
	pass

class BarBoxAddError(Error):
	pass

class BarBoxInvalidObjectError(Error):
	pass
