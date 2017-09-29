# -*- coding: utf-8 -*-

import os

import oam.pkg

def check_for_executable(filename):
    """return True if the file exists and is executable"""
    return os.access(filename, os.X_OK)

def is_update_available(atom):
    """return True if there is an update available for atom"""
    return oam.pkg.Pkg().is_update_available(atom)

def preserved_libs():
    """return True if there are preserved libraries"""
    return len(oam.pkg.Pkg().preserved_libs())>0
