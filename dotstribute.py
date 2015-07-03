#!/usr/bin/env python
import os
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-d", "--dotexe", dest = "dot_exclude",
            help = "Exclude files, given by .dotexclude file")
    parser.add_option("-f", "--force", dest = "force", default = False,
            action = "store_true", help = "Force override the previous links")

    (options, args) = parser.parse_args()

    # option for custom dotexclude file
    dotexclude = ".dotexclude"
    if options.dot_exclude:
        dotexclude = options.dot_exclude

    # prepare list of files not to link to $HOME
    EXCLUDE = []
    if os.path.exists(dotexclude):
        with open(dotexclude) as f:
            EXCLUDE = f.read().split()
    EXCLUDE.append(dotexclude)

    print "EXCLUDE:", EXCLUDE
    print args

    # add option: operatate from any directory
    # maybe no flags = current dir
    # get files not in exclude list
    files = [f for f in os.listdir(".") if f not in EXCLUDE]

    # by default place dotfiles in your $HOME
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

