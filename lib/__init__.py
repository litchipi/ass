import argparse

# TODO    Add autocompletion with external lib on this

from . import priorize

def setup_edit_parser(subp):
    # TODO    Add data to parser
    # Add choice for category, add choice for name
    #    With list for autocompletion, but allow to step out of the list for creation
    pass

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
    
    # if len(sys.argv) < 2:
    #     print("Usage: {} <command> [args]".format(sys.argv[0]))
    #     sys.exit(1)

    # command = get_command(sys.argv[1])
    # if not command:
    #     print(f"Command not found")
    #     print("Available commands:")
    #     for cmd, data in COMMANDS.items():
    #         print("- {}: {}".format(cmd, data["short_help"]))
    #     sys.exit(1)

