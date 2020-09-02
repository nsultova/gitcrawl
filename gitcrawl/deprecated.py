"""
Contains code no longer used but kept for review/further reuse
--- imports need to be re-added ---
"""

def determine_disjuct_modules_alternative(src_rep):
	"""
		Potentially get rid of determine_added_modules and get_modules_lst()
	"""
	findimports_output = subprocess.check_output(['findimports', src_rep])
	findimports_output = findimports_output.decode('utf-8').splitlines()

	custom_modules_lst = []
	for i, elem in enumerate(findimports_output):
		if ':' in elem:
			continue
		elem = elem.rstrip('\n').split('.',1)[0].strip()
		#print(f" element : {elem}")
		custom_modules_lst.append(elem)

	custom_modules_lst = set(custom_modules_lst)

	#beautify this 
	disjunct_modules = []
	for i, elem in enumerate(custom_modules_lst):
		if elem in sys.modules:
			continue
		else:
			disjunct_modules.append(elem)
	
	return disjunct_modules

def determine_added_modules(src_rep, python_version):
	"""
	Determine overlapping and disjunct modules between the ones shipped by the specified python version and the ones found in the source repository specified.
	For now we rely on findimports providing the needed dependency tree within the source repository.
  	Links to tool : https://github.com/mgedmin/findimports, https://pypi.org/project/findimports/
	"""
	
	python_modules_lst = get_modules_list(python_version)

	findimports_output = subprocess.check_output(['findimports', src_rep])
	findimports_output = findimports_output.decode('utf-8').splitlines()

	custom_modules_lst = []
	for i, elem in enumerate(findimports_output):
		if ':' in elem:
			continue
		elem = elem.rstrip('\n').split('.',1)[0].strip()
		#print(f" element : {elem}")
		custom_modules_lst.append(elem)

	custom_modules_lst = set(custom_modules_lst)

	not_common = [val for val in custom_modules_lst if val not in python_modules_lst]
	common = [val for val in custom_modules_lst if val in python_modules_lst]

	return not_common, common