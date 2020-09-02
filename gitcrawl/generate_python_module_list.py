#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs to be executed only when a new python version has appeared.
chmod +x has been set

Execution:
$ ./generate_python_module_list.py
"""

from sys import version
from bs4 import BeautifulSoup
import requests
import re
import pickle
import argparse

def write_modules_list(python_version=3.10):
	"""
	This script parses https://docs.python.org/3.10/py-modindex.html# and creates a static list containing all the module names. 
	This list is used by determine_disjunct_module_names(src_rep) to compare against external modules within a given repository.

	Parameters
	----------
	python_version : str
		major+minor version e.g 3.7, 1.9, 3.10
	"""	
	try:
		page = requests.get(f'https://docs.python.org/{python_version}/py-modindex.html#')
		page.raise_for_status()

	except requests.exceptions.HTTPError as err:
		raise SystemExit(err)
	except requests.exceptions.RequestException as err:
		#catastrophic error. bail.
		raise SystemExit(err)

	content = page.text

	soup = BeautifulSoup(content, features="html.parser")
	#print(soup.prettify())

	#Fancy regex that emerged _before reading the docs of bs4 ^^
	#<code class="xref">\s*([\d\w_]+)\s*<\/code>
	pattern = soup.find_all("code", "xref")

	modules_lst = []
	for i, elem in enumerate(pattern):
		#print(f"element :{elem}, i : {i}")
		#This regex filters the module name out of the embeddings
		match = re.search(r'(?P<code0><code class="xref">)(?P<modulename>\s*([\d\w_.]+)\s*)(?P<code1><\/code>)', str(elem))
		modulename = match.group('modulename')
		modules_lst.append(modulename)

	#with open(f'python{python_version}-modules.txt', 'w') as f:
	#	modules_lst = map(lambda x:x+'\n', modules_lst)
	#	f.writelines(modules_lst)

	# append package name
	# only include the module name, e.g only skimage instead of skimage.filters
	modules_lst = list(set([ x.split('.')[0] for x in modules_lst]))
	pickle.dump(modules_lst, open('python_module_index.pickle', 'wb'))

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='''
								This script parses https://docs.python.org/3.10/py-modindex.html# 
								and creates a static list containing all the module names. 
												''')

	parser.add_argument('-v', '--version-number', required=True, type=str,
		help='''
				Provide a valid python version number. 
					Format: major+minor, e.g 3.7, 3.8, 3.10
			''')
	
	args = parser.parse_args()
	v_num = args.version_number

	write_modules_list(v_num)
