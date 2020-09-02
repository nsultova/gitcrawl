#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import tqdm
import argparse
import json
import re
import yaml
from .core_functions import determine_disjunct_module_names, search_conda_channel, create_env, search_pip
from .helpers import clean_list, dir_path, start_menu, parse_requirements,replace_names


def main():
	parser = argparse.ArgumentParser(description='''
													Extracts import statements from a python repository and returns a list of additionally added modules 
													(Future: creates a valid environment.yml file that can later be installed via conda and pip
												''')

	parser.add_argument('-s', '--src-repository', required=True, type=dir_path,
		help='''
				Provide a valid path to the source-code you want to parse e.g /path/to/my/src
			''')

	parser.add_argument('-l', '--leave-me-alone', action='store_true',default=False, 
		help='''
				Hides the decision query for each package/channel, sparing you a bit of interaction. 
				Good for lazy mode or for irritable moods.
				Be aware that it takes definitely longer tho.
			''')
	
	args = parser.parse_args()
	src_rep = args.src_repository
	leave_me_alone = args.leave_me_alone

	#check if the repository contains a requirements.txt
	pip_packages = parse_requirements(src_rep)

	#we might not need this due to default argument
	#leave_me_alone = True if leave_me_alone else False

	channel_lst = []
	name, additional_channel_lst = start_menu()
	default_channel_lst = ["conda-forge", "anaconda"]

	if additional_channel_lst:
		channel_lst = additional_channel_lst + default_channel_lst
	else:
		channel_lst = default_channel_lst

	print(f"channel_lst : {channel_lst}")


	# disjunct_modules, same_modules = determine_added_modules(src_rep,python_version)
	disjunct_modules = determine_disjunct_module_names(src_rep)

	disjunct_modules = replace_names(disjunct_modules)

	if pip_packages:
		disjunct_modules = list(set(disjunct_modules).union(pip_packages))

	print(f"Disjunct modules: {disjunct_modules}")


	# For each module-name, determine installation candidates (if available)
	# for now only one consider splitting for conda-forge/anaconda.

	conda_lst = []
	pip_lst = []
	module_not_found_lst = []

	for i,elem in enumerate(disjunct_modules):
		count = len(channel_lst)

		for channel in channel_lst:
			pname, skip = search_conda_channel(channel, elem, leave_me_alone)
			if pname is not None:
				conda_lst.append(pname)
				break
			else:
				if count > 0 and skip is True:
					print("Cancel search. Skip to next channel...")
					count -= count
					continue #break
				if count <= 0 or skip is False:
					module_not_found_lst.append(elem)
	
	module_not_found_lst = set(module_not_found_lst)

	
	for i, elem in enumerate(module_not_found_lst):
		pname, skip= search_pip(elem, leave_me_alone)
		if pname is not None:
			pip_lst.append(pname)
			continue
		else:
			if skip is True:
				print("Cancel search. Skip to next package...")
				continue
			else:
				print(f"{elem} not found within pip.")

	conda_lst = clean_list(conda_lst)
	if pip_lst:
		pip_lst = clean_list(pip_lst)

	print(f"conda candidates : {conda_lst}")
	print(f"pip candidates : {pip_lst}")
	print(f"the rest : {module_not_found_lst}")

	create_env(conda_lst,pip_lst,name,channel_lst)

if __name__ == "__main__":
	main()