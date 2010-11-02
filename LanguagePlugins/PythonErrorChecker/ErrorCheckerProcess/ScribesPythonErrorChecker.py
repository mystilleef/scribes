#! /usr/bin/env python
# -*- coding: utf8 -*-

if __name__ == "__main__":
	from os import nice
	nice(19)
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	from gobject import MainLoop, threads_init
	threads_init()
	from Manager import Manager
	Manager()
	MainLoop().run()
