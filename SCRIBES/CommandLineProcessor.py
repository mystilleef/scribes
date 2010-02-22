def get_uris(args, newfile):
	if not args: return []
	uris = __uris_from(args)
	existent_uris, nonexistent_uris = __categorize(uris)
	new_uris = __create(nonexistent_uris) if newfile else __ignore(nonexistent_uris)
	uris = existent_uris + new_uris
	if not uris: raise SystemExit
	return uris

def __uris_from(args):
	from gio import File
	return [File(arg.strip()).get_uri() for arg in args]

def __categorize(uris):
	existent_uris, nonexistent_uris = [], []
	for uri in uris: existent_uris.append(uri) if __exists(uri) else nonexistent_uris.append(uri)
	return existent_uris, nonexistent_uris

def __exists(uri):
	# Do not perform checks on remote files.
	from gio import File
	if File(uri).get_uri_scheme() != "file": return True
	from os.path import exists
	return exists(File(uri).get_path())

def __ignore(uris):
	if not uris: return []
	from gio import File
	for uri in uris: print File(uri).get_path(), " does not exists"
	return []

def __new(uri):
	try:
		from gio import File
		if File(uri).get_uri_scheme() != "file": raise ValueError
		File(uri).replace_contents("")
	except ValueError:
		print "Error: %s is a remote file. Cannot create remote files from \
		terminal" % File(uri).get_path()
	except:
		print "Error: could not create %s" % File(uri).get_path()
	return uri

def __create(uris):
	return [__new(uri) for uri in uris]
