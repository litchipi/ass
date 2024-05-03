import argparse

try:
    from . import priorize
    from . import datastore
except ImportError:
    import priorize
    import datastore

COMMANDS = {
    "priorize": {
        "aliases": ["p", "prio"],
        "short_help": "Pick things to do based on priorities set",
        "setup_parser": priorize.setup,
        "autocomplete": priorize.autocomplete,
    },
    "edit": {
        "aliases": ["e"],
        "short_help": "Edit a data file contained in the assistant data dir",
        "setup_parser": datastore.setup_edit,
        "autocomplete": datastore.autocomplete_datastore,
    },
}

def get_command(raw):
    if raw in COMMANDS:
        return raw
    else:
        for cmd, data in COMMANDS.items():
            if raw in data["aliases"]:
                return cmd
        return None

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Display additionnal informations',
    )

    subparser = parser.add_subparsers(
        help = "Commands",
        dest = "command",
        required = True,
    )

    for cmd, data in COMMANDS.items():
        cmd_parser = subparser.add_parser(
            cmd,
            help = data["short_help"],
            aliases = data["aliases"],
        )

        data["setup_parser"](cmd_parser)

    return parser.parse_args()

def autocomplete_command():
    print(" ".join(COMMANDS.keys()))
    
if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) < 3:
        autocomplete_command()
    elif len(args) == 3 and (not (args[2] in COMMANDS)):
        autocomplete_command()
    else:
        command = get_command(args[2])
        if command:
            data = COMMANDS[command]
            data["autocomplete"](args[3:])
