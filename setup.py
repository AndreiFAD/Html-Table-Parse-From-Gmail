# !/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Fekete Andras Demeter'

import sys, os
from cx_Freeze import setup, Executable


includefiles = ['config.json']
build_exe_options = {
                     "packages": ["idna.idnadata", "imaplib", "datetime", "base64", "email", "json", "logging", "time", "socket", "os", "multiprocessing", "email.header", "html_table_parser"],
                     'build_exe': 'Gmail_Tables_Read',
                     'include_files' : includefiles
                     }
base = None

setup(
    name = "Gmail_Tables_Read",
    version = "1.0" ,
    description = "Gmail_Tables_Read" ,
    options = {"build_exe": build_exe_options},
    executables = [Executable("Gmail_Tables_Read.py", base=base)]
)


