def main(argv):
	if argv[0] != "plugins": raise RuntimeError
	files = __get_i18n_files(argv[0])
	__write(files)
	return

def __get_i18n_files(folder):
	from os import walk
	i18n_files = []
	for root, dirs, files in walk(folder):
		for filename in files:
			if filename.endswith("glade") or filename == "i18n.py":
				_file = root + "/" + filename + "\n"
				i18n_files.append(_file)
	return i18n_files

def __write(files):
	string = "".join(files)
	handle = open("i18n_plugin_files.txt", "w")
	handle.write(string)
	handle.close()
	return

if __name__ == "__main__":
	from sys import argv
	main(argv[1:])
