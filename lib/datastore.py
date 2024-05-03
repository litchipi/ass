import os
import sys

def get_data_path():
    data_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    comp = data_dir.split("/")[1:]
    for n in range(0, len(comp)):
        gitdir = os.path.join(data_dir, "../" * n, ".git")
        if os.path.isdir(gitdir):
            d = os.path.abspath(os.path.join(data_dir, "../" * n, "data"))
            os.makedirs(d, exist_ok=True)
            return d
    raise Exception("Source directory not found, cannot get data path")
    

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

        if os.path.isdir(os.path.join(data_dir, args[-1])):
            data_dir = os.path.join(data_dir, args[-1])
        
    for (root, dirs, files) in os.walk(data_dir):
        print(" ".join(dirs + files))
        return
