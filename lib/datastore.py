import os
import sys

class Datastore:
    def __init__(self, subd, root=None):
        if root is None:
            self.root = os.path.abspath(
                os.path.join(os.path.expanduser("~/.local/share"), subd)
            )
        os.makedirs(self.root, exist_ok=True)
        print("Data stored under {}".format(self.root))

    def cache_path(self, *path):
        return os.path.join(self.root, "cache", *path)

    def data_path(self, *path):
        return os.path.join(self.root, "data", *path)

    def edit_data(self, *path):
        fpath = os.path.join(self.root, "data", *path)
        if not os.getenv("EDITOR"):
            raise Exception("EDITOR environment variable not set")
        os.system(f"$EDITOR {fname}")

def setup_edit(subp):
    subp.add_argument("category", help="Category of the file", type=str)
    subp.add_argument("name", help="File to edit", type=str)

def autocomplete_datastore(args):
    data_dir = get_data_path()
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
