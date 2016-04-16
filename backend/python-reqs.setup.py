"""
Project: flask-rest
Author: Saj Arora
Description: Set up all the python requirements found in
python-reqs.txt file
"""

import os
import shutil
import sys
from dircache import listdir

###############################################################################
# Directories
###############################################################################

DIR_MAIN = os.path.dirname(os.path.realpath(__file__))
DIR_LIB = os.path.join(DIR_MAIN, 'pylibs')
FILE_REQUIREMENTS = 'python-reqs.txt'


###############################################################################
# Helpers
###############################################################################
def make_dirs(directory):
    """Creates directories"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def exec_pip_commands(command):
    """Executes pip command on system"""
    script = []
    script.append('echo %s' % command)
    script.append(command)
    script = '/bin/bash -c "%s"' % ';'.join(script)
    os.system(script)


def install_py_libs():
    """Installs requirements from requirements file and then copies them
    from site-packages folder into main/lib folder
    Alse excludes files that don't need to be deployed"""
    make_dirs(DIR_LIB)
    exec_pip_commands('pip install -t %s -r %s' % (DIR_LIB, FILE_REQUIREMENTS))


def run():
    """Runs this script"""
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    install_py_libs()

if __name__ == '__main__':
    run()