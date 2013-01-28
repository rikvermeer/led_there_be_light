#!/usr/bin/env python

from distutils.core import setup, Extension

setup(	name="lpd8806",
	version="0.1",
	description="Python bindings for the lpd8806 driven ledstrip",
	author="Rik Vermeer",
	author_email="mail@rikvermeer.nl",
	maintainer="Rik Vermeer",
	maintainer_email="mail@rikvermeer.nl",
	license="GPLv2",
	url="http://www.github.com/rikvermeer",
	include_dirs=["/usr/src/linux/include"],
	scripts=[],
	ext_modules=[Extension("lpd8806", ["pylpd8806.c"],extra_compile_args=['-g'])])
