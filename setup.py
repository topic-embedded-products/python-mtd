# SPDX-License-Identifier: MIT
from distutils.core import setup, Extension

setup(
    ext_modules=[Extension("mtd", ["python-mtd.c"])],
    py_modules=['mtdutil']
)
