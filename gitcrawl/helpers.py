"""
Script containing various additional helper functions
"""
import pkgutil
import os
import sys
from bs4 import BeautifulSoup
import requests
import requirements
import re
import subprocess
import yaml
import json

def extract_keys(nested_dict):
	"""
	This function is used in order to parse the.json output generated by executing conda search <package-name>
	for potential install candidates.

	Parameters
	----------
	nested_dict : dictionary
		.json file

	Returns
	-------
	key_lst: list
		list containing only the keys (the potential installation candidates)
	"""
	key_lst = []
	for key, value in nested_dict.items():
		key_lst.append(key)
		if isinstance(value, dict):
			extract_keys(value)
	return key_lst

def dir_path(str):
	"""
	Check if path leads to a valid directory

	Parameters
	----------
	str : str
		path to directory

	Returns
	-------
	str
		input if directory exists
	"""
	if os.path.isdir(str):
		return str
	else:
		raise NotADirectoryError(str)

def replace_names(module_lst):
	"""
	Load name-assignment.txt and compare against extracted import modules
	If a match is found, replace with value. (which is the according package name for conda/pip)
	As for now this is the way to approach the discrepancy between
	module names as and package names as described in:
	https://stackoverflow.com/questions/38733220/difference-between-scikit-learn-and-sklearn

	Parameters
	----------
	module_lst : list
		Contains module names extracted from import statements

	Returns
	-------
	module_lst
	"""

	name_assign_dict = {}
	module_names_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'module-names.txt')
	with open(module_names_path, 'r') as f:
		for line in f:
			(key, val) = line.split()
			name_assign_dict[key] = val

	for i, elem in enumerate(module_lst):
		if elem in name_assign_dict:
			module_lst[i] = name_assign_dict[elem]

	return module_lst

def display_options(numbered_lst, elem):
	"""
	Displays command options and selection choices.
	

	Parameters
	----------
	numbered_lst : list
		enumerated installation candidates for elem
	elem : str
		package name to be installed
	"""
	print(f"I found several options for {elem}")
	print(f"Please select a choice: ") 
	print("'s' for skip channel")
	print("'c' for cancel search for this package")
	print("'n' for adding a custom package name instead")
	print("'q' for quit")

	for option in numbered_lst:
		print(option)

def enumerate_installation_candidates(installation_candidates):
	"""
	Parameters
	----------
	installation_candidates : list

	Returns
	-------
	install_candidates_numbered: list
	"""
	install_candidates_numbered = [f"[{i}] {elem}" for i, elem in enumerate(installation_candidates)]
	return install_candidates_numbered

def start_menu():
	"""
	Displays menu at execution start.

	Returns
	-------
	name: str
		if provided custom environment name, else "test-env"
	channel_lst: lst
		if provided, contains additional conda-channels to install from
	"""
	print("Hello :)")
	#What kind of checks to add here?
	name = input("Please provide a name for the new environment: [e.g testenv, test-env, TestEnv] ")
	if not name:
		name = "test-env"
	choice = input("Do you want to specify any additional conda-channels to use? [y/n]")
	if choice.casefold() == "y".casefold():
		channel_lst = input("Please enter the conda-channels you want to use, separated by ',' ")
		channel_lst = channel_lst.split(',')
	else:
		channel_lst = None

	return name, channel_lst

def menu(num_installation_candidates, elem):
	"""
	Main menu displayed at every action taken.	

	Parameters
	----------
	num_installation_candidates : list
		enumerated installation candidates
	elem : str
		package to be installed

	Note: I think the current return can be done better.
	(Something for more extra time) 

	Returns
	-------
	choice: string | int
		choice depending
	"""
	display_options(num_installation_candidates, elem)
	choice = input("Choice :")
	if choice.casefold() == "q".casefold():
		sys.exit("Bye :)")

	# In case you choose a command..
	if choice.isalpha():
		return choice.lower()

	elif not re.match("\d{1,3}", choice):
			print("Invalid input")
			# Is this ok or dangerous?
			display_options(num_installation_candidates,elem)
	else:
		if int(choice) > len(num_installation_candidates):
			print("Invalid number")
			display_options(num_installation_candidates,elem)

	#..else your choice was an installation candidate..
	return int(choice)

def clean_list(enumerated_lst):
	"""
	Parameters
	----------
	enumerated_lst: list
		enumerated installation candidates

	Returns
	-------
	cleaned_lst: list
		cleans up weird naming within installation candidates
	"""
	cleaned_lst = [re.sub(r'(\[\d+\]\s)', '', elem) for elem in enumerated_lst]
	return cleaned_lst

def choose_custom_name(elem):
	"""
	Insert custom package name.
	Example: cv2 is extracted from the imports and the tool has no chance to know 
	that the package name is 'opencv'. If you know this right away, you can add this here.

	Note: Part of this is mitigated by using replace_names(). If you know more assignments,
	feel free to add them to module-names.txt
	
	Parameters
	----------
	elem : str
		chosen installation candidate

	Returns
	-------
	name: str
		custom name for package
	"""
	name = input(f"Please provide an alternative name for {elem} :")
	#TODO: checks and tests
	return name

def parse_requirements(src_rep):
	"""
	If the repository contains a requirements.txt we happily parse it

	Parameters
	----------
	src_rep : str | list
		repository to be parsed by findimports
		
	Returns
	-------
	pip_packages: list
		extracted package names
	"""
	pip_packages = []
	try:
		with open(os.path.join(src_rep,'requirements.txt'), 'r') as f:
			for req in requirements.parse(f):
				pip_packages.append(req.name)
			
			print("finished parsing requirements.txt")

		return pip_packages

	except FileNotFoundError:
		print("Could not find requirements.txt within specified src directory")