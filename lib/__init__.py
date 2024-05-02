import argparse

# TODO    Add autocompletion with external lib on this

# TODO    Pomodoro timer
# TODO    Add notes

from . import priorize

def setup_edit_parser(subp):
    # TODO    Add existing categories to possible choices
    subp.add_argument("category", help="Category of the file", type=str)

    # TODO    Add existing names to possible choices
    subp.add_argument("name", help="File to edit", type=str)

def get_args(commands):
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

    for cmd, data in commands.items():
        cmd_parser = subparser.add_parser(
            cmd,
            help = data["short_help"],
            aliases = data["aliases"],
        )

        data["setup_parser"](cmd_parser)

    return parser.parse_args()
