# -*- coding: utf-8 -*-

import os

def check_for_executable(filename):
    """Return True if the file exists and is executable"""
    return os.access(filename, os.X_OK)

def is_update_available(atom):
    return False

def preserved_libs():
    return False
