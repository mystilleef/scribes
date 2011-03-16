#! /usr/bin/env python
# -*- coding: utf8 -*-

if __name__ == "__main__":
	from SCRIBES.Utils import fork_process
	fork_process()
	# from sys import argv, path
	# python_path = argv[1]
	# path.insert(0, python_path)
	from gobject import MainLoop, threads_init
	threads_init()
	from signal import signal, SIGINT, SIG_IGN
	signal(SIGINT, SIG_IGN)
	from Manager import Manager
	Manager()
	MainLoop().run()
