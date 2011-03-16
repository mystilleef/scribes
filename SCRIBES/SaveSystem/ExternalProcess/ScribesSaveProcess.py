#! /usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
	from SCRIBES.Utils import fork_process
	fork_process()
	# from sys import argv, path
	# path.insert(0, argv[1])
	from signal import signal, SIGINT, SIG_IGN
	signal(SIGINT, SIG_IGN)
	from Main import main
	main()
