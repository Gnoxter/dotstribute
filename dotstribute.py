#!/usr/bin/env python
import os
from optparse import OptionParser

class Dot():
    def __init__(self, git_dir):
        self.git_dir = git_dir

    def get_files(self, dotignore=".dotignore"):
        # use the .dotignore file IN the git directory, not in cwd
        ignore_file = dotignore
        if self.git_dir != ".":
            ignore_file = self.git_dir + "/" + dotignore

        # prepare list of files NOT to link to $HOME
        # based on the contents of the .dotignore file
        IGNORE = []
        if os.path.exists(ignore_file):
            with open(ignore_file) as f:
                IGNORE = f.read().split()

        # still never add the .dotignore file to $HOME
        IGNORE.append(dotignore)

        # compile a list of full paths to begin with
        # this will make other operations much simpler
        self.git_links  = []
        self.home_links = []

        for f in os.listdir(self.git_dir):
            if f in IGNORE:
                continue

            # by default place dotfiles in your $HOME
            to = os.environ["HOME"] + "/"

            # make them dotfiles, it they do not begin with dots
            if not f.startswith("."):
                to += "."
            to += f

            # this is basically strjoin(cwd + parameter)
            # but it doesn't end in a slash for some reason
            f = os.path.abspath(self.git_dir) + "/" + f

            self.git_links.append(f)
            self.home_links.append(to)

    def link(self, ask=False):
        for i, f in enumerate(self.git_links):

            # make sure to ask nicely
            if ask and not os.path.exists(self.home_links[i]):
                if raw_input("Link %s to home (y/N)? > " % f).lower() == "y":
                    os.symlink(f, self.home_links[i])

            # don't ask, just do
            elif not os.path.exists(self.home_links[i]):
                os.symlink(f, self.home_links[i])

            else:
                print "skipping", f

    def unlink(self, ask=False):
        for f in self.home_links:

            # ask to delete
            if ask and os.path.exists(f):
                if raw_input("Unlink %s (y/N)? > " % f).lower() == "y":
                    os.unlink(f)

            # don't ask, just do
            elif os.path.exists(f):
                os.unlink(f)

            else:
                print "Does not exist:", f

def main():
    parser = OptionParser()
    parser.add_option("-d", "--dotignore", dest = "dot_ignore",
            help = "Exclude files, given by .dotignore file")
    parser.add_option("-a", "--ask", dest = "ask", default = False,
            action = "store_true", help = "Ask if you want the " +
            "files to be linked or unlinked")
    parser.add_option("-u", "--unlink", dest = "unlink", default = False,
            action = "store_true", help = "Remove the previous links")

    (options, args) = parser.parse_args()

    dotignore = ".dotignore"
    if options.dot_ignore:
        dotignore = options.dot_ignore

    # path to dotfiles as command line argument
    git_dir = "."
    if len(args) == 1 and os.path.exists(args[0]):
        git_dir = args[0]

    # if the path isn't there, ask to use this dir
    elif len(args) == 1 and not os.path.exists(args[0]):
        print "That directory does not exist"
        print "Use the current working directory? (y/N)"
        if raw_input("> ").lower() != "y":
            print "Now exiting"
            return

    d = Dot(git_dir)
    d.get_files(dotignore)

    # no flag == don't ask
    if options.unlink:
        d.unlink(options.ask)
    else:
        d.link(options.ask)

if __name__ == "__main__":
    main()

