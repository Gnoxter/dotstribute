#!/usr/bin/env python
import os
from optparse import OptionParser

def main():
    # add option: add files for exlusion
    # don't symlink these, because they are not your dotfiles (I hope)
    EXCLUDE = ["license", ".git", ".gitignore", "readme.md"]

    # add option: custom file
    dotexclude = ".dotexclude"
    if os.path.exists(dotexclude):
        with open(dotexclude) as f:
            EXCLUDE += f.read().split()
    EXCLUDE.append(dotexclude)

    # add option: operatate from any directory
    # maybe no flags = current dir
    files = [f for f in os.listdir(".") if f.lower() not in EXCLUDE]

    for f in files:
        to = os.environ["HOME"] + "/"
        if not f.startswith("."):
            to += "."
        to += f

        # for correct symlinking
        f = os.path.abspath(f)

        # add option: replace (ask)
        # add option: force replace (no ask)
        # add option: chmod symlink
        if not os.path.exists(to):
            os.symlink(f, to)
        else:
            print "skipping", f

if __name__ == "__main__":
    main()

