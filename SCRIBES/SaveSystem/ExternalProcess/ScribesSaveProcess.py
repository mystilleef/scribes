#! /usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
	from sys import argv, path
	path.insert(0, argv[1])
	from gobject import MainLoop, threads_init
	threads_init()
	from signal import signal, SIGINT, SIG_IGN
	signal(SIGINT, SIG_IGN)
	from Main import main
	main()
