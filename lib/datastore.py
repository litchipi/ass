import os
import sys

class Datastore:
    def __init__(self, *subd):
        self.data_root = os.path.abspath(
            os.path.join(os.path.expanduser("~/.local/share"), *subd)
        )
        os.makedirs(self.data_root, exist_ok=True)

        self.cache_root = os.path.abspath(
            os.path.join(os.path.expanduser("~/.cache"), *subd)
        )
        os.makedirs(self.cache_root, exist_ok=True)

    def cache_path(self, *path):
        return os.path.join(self.cache_root, *path)

    def data_path(self, *path):
        return os.path.join(self.data_root, *path)

    def edit_data(self, *path):
        if not os.getenv("EDITOR"):
            raise Exception("EDITOR environment variable not set")
        os.system("$EDITOR {}".format(self.data_path(*path)))

def setup_edit(subp):
    subp.add_argument("category", help="Category of the file", type=str)
    subp.add_argument("name", help="File to edit", type=str)

def autocomplete_datastore(args):
    datastore = Datastore("ass")
    data_dir = datastore.data_root
    if len(args) >= 1:
        for arg in args[:-1]:
            data_dir = os.path.join(data_dir, arg)
            if not os.path.isdir(data_dir):
                return

        if os.path.isfile(os.path.join(data_dir, args[-1])):
            return

        if os.path.isdir(os.path.join(data_dir, args[-1])):
            data_dir = os.path.join(data_dir, args[-1])
        
    for (root, dirs, files) in os.walk(data_dir):
        print(" ".join(dirs + files))
        return
