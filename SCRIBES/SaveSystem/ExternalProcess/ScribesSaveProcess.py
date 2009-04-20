#! /usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
	from sys import argv, path
	path.insert(0, argv[1])
	from Main import main
	main()
