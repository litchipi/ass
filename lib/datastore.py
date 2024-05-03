
def setup_edit(subp):
    # TODO    Add existing categories to possible choices
    subp.add_argument("category", help="Category of the file", type=str)

    # TODO    Add existing names to possible choices
    subp.add_argument("name", help="File to edit", type=str)

def autocomplete_datastore(args):
    # TODO    Autocomplete datastore
    print("foo bar")
