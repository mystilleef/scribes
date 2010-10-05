#! /usr/bin/env python
# -*- coding: utf8 -*-

def main():
	print "Removing byte compiled python objects please wait..."
	__remove(__byte_compile_files())
	return

def __byte_compile_files():
	from os import walk, getcwd
	from os.path import join
	__files = []
	for root, dirs, files in walk(getcwd()):
		for filename in files:
			if filename.endswith(".pyc") or filename.endswith(".pyo"):
				_file = join(root, filename)
				__files.append(_file)
	return __files

def __remove(files):
	from os import remove
	[remove(path) for path in files]
	print "Removed byte compiled python objects"
	return

if __name__ == "__main__":
	from sys import argv
	main()
