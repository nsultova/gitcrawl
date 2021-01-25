# Gitcrawl 
* exports required modules from python code 
* bakes you a nice environments.yml for your conda
* aims to ease the headache that comes with transferring conda environments
* allows you to create a neat environments.yml for any python project you feed it

[Docs](https://nsultova.github.io/gitcrawl/)

## Motivation
Currently there is no way known to me to transfer conda environments in a non-cumbersome way across operating systems. The current commands as stated in the official docs are:

```
conda env export > environment.yml 

conda env export --no-builds > environment.yml 

conda env export --from-history.yml

```

Example:

Within your environment, call `conda install numpy=1.17.5`

`conda env export` produces a .yml file including version numbers, local dependencies + hashes: 
```
- numpy=1.19.5=py38h6ced74f_1
- olefile=0.46=pyh9f0ad1d_1
...
```

`conda env export --no-builds` produces a .yml file including version numbers and local dependencies: 
```
- numpy=1.19.5
- olefile=0.46
...
```

`conda env export --from-history` produces a .yml file with no version information included, Also it includes only packages which have ben manually installed into the environment. 

```
- numpy
- pandas
...
```

If you want to get a better grasp of the commands [here](https://github.com/nsultova/conda_reproduce_testcase) is a small test-case.


Above behavior makes transferring conda environments across systems often quite challenging. More often than not, you'll end up writing the entire environment.yml by hand. 

## Gitcrawl

I wrote gitcrawl out of the desire to make life a bit easier for my colleagues and me, as we often exchange/test/experiment with various code. 

Gitcrawl offers another handy feature: You can clone any python repository and it will create a environment.yml for you, thus saving you a lot of time and helping you keep your system neat and tidy when you just simply want to test some code. 
(Especially nice, if not even a requirements.txt is provided)

### Note:
* This tool is a workaround  and PoC, keep this in mind
* Adjusting the resulting environment.yml is sometimes unavoidable


## Install: 


**Way 0:**

`pip install gitcrawl`

**Way 1**
The manual way (if you want to tinker around):

Clone the repository:

`git clone https://github.com/nsultova/gitcrawl.git`

Use the provided gitcrawl-env.yml to create a conda environment:

`conda env create -f gitcrawl-env.yml`

Activate the new environment: 
`conda activate gitcrawl-env`

Verify that the new environment was installed correctly:
`conda env list`

(If you prefer to use pip you should be able to extract what you need from the environments.yml)

## Usage:

**Way 0**

`gitcrawl -s ../repo/to/be/parsed`

**Way 1**

`cd <path/to/gitcrawl>`

`python3 -m gitcrawl.gitcrawl -s ../repo/to/be/parsed`


The code is designed in a heavily interactive way. If you're lazy you can set the `--leave-me-alone` flag. This will make gitcrawl run trough all channels and ask you only if there are several installation candidates to choose from.

*In either ways `--help` and the docs are your friends. <3* [Have a look](https://nsultova.github.io/gitcrawl/)


## Workflow

<img src="https://raw.githubusercontent.com/nsultova/gitcrawl/master/imgs/workflow.png" width="50%">

## Notes

This code relies on:
* [findimports](https://github.com/mgedmin/findimports)
* [requirements-parser](https://github.com/davidfischer/requirements-parser)
* [pip_search](https://pypi.org/project/pip-search/#files) ..as for now pip-search is 

Make sure you have them installed!
