"""
EXPERIMENTAL

Try to get all raw data files in a given raw data path
"""

import os

for dirname, dirnames, filenames in os.walk("raw_data"):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    #    print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        raw_file = os.path.join(dirname, filename)
        if raw_file[-3:] == "raw":
            print(raw_file)

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if ".git" in dirnames:
        # don't go into any .git directories.
        dirnames.remove(".git")
