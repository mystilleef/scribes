#! /usr/bin/env python
# -*- coding: utf8 -*-

from compileall import compile_dir
compile_dir("plugins/", force=True)
