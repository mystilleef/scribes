#! /usr/bin/env python
# -*- coding: utf8 -*-

from compileall import compile_dir
compile_dir("GenericPlugins/", force=True)
compile_dir("LanguagePlugins/", force=True)
