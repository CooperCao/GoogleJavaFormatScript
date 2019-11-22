#!/usr/bin/env python2.7

# Purpose:
# Format all .java files in the directory, including child
# directories and their .java files, or just a single .java
# file.
#
# Instruction:
# Script can be called from python interpreter or aliased
# and used as any other UNIX tools, like 'cd' or 'cat'.
#
# In order to use this script like 'UNIX tool':
# $ chmod +x jfmt.py
# And add alias to your profile or rc file:
# alias jfmt="~/path/to/jfmt.py"
#
#
# Behaviour:
# When script called in directory without arguments, or on
# directory it will format every .java file in current
# (or provided) directory AND child directories.
# 
# When script called with argument which is path to .java
# file, only this file will be formated.
# Get script location path in order to find
# a real path of the google-java-format.

from __future__ import print_function
import sys, os
import argparse

try:
    # Python2
    from urllib import urlencode  
    from urllib import quote
    from urllib import urlretrieve
    from urllib import urlopen
except ImportError:
    # Python3
    from urllib.parse import urlencode  
    from urllib.parse import quote
    from urllib.request import urlretrieve
    from urllib.request import urlopen


GJF = "google-java-format-1.7-all-deps.jar"
url= "https://github.com/google/google-java-format/releases/download/google-java-format-1.7/google-java-format-1.7-all-deps.jar"

def origin_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

google_java_format_jar = os.path.join(origin_path(),GJF)
base_command = ['java','-jar',google_java_format_jar,'--skip-sorting-imports','--replace','--aosp']
verbose = False

def format_files(p):
    for (dirpath, dnames, fnames) in os.walk(p):
        for fname in fnames:
            if fname.endswith('.java'):
                fpath = os.path.join(dirpath,fname)
                format_file(fpath)

def format_file(p):
    global verbose
    if verbose:
        print("Format file: ", p)
    base_command.append(p)    
    command=" ".join(base_command)
    os.system(command)

def parse_argv():
    parser = argparse.ArgumentParser(
        description='Format all .java files in the directory,' +
        ' including child directories and their .java files, ' +
        'or just a single .java file.')
    parser.add_argument('--verbose',
                        '-v',
                        action='store_true',
                        help='verbose flag')
    parser.add_argument('file',
                        nargs='?',
                        default='none',
                        help='path to .java file or folder')                  
    p = parser.parse_args()
    global verbose
    verbose = p.verbose
    if len(sys.argv) == 1 or len(sys.argv) == 2 and p.verbose:
        path = os.getcwd()
        if verbose:
            print("Path: ", path)
        format_files(path)

    if p.file != 'none':
        if os.path.isfile(p.file):
            format_file(p.file)
            return
          
        if os.path.isdir(p.file):
            if verbose:
                print("Format dir: ", p.file)
            format_files(p.file)
            return

def isGoogleJavaFormatJar():
    if os.path.isfile(google_java_format_jar):
        return True
    else:
        return False


def download_report(count, block_size, total_size):
    total_size = total_size/1024
    downloaded = count * block_size/1024
    percent = 100. * downloaded / total_size
    percent = min(100, percent)
    print('downloaded %dK-%dK, %.2f%% completed' % (downloaded,total_size, percent))


def main():
    if not isGoogleJavaFormatJar():
        print("Downloading %s from Github..."%GJF)
        urlretrieve(url,google_java_format_jar,reporthook=download_report)
    parse_argv()
    print("Format Done")

if __name__ == '__main__':
    main()