import sys
import argparse
from nubia import Nubia, PluginInterface, Options

import tool.cli.commands

class POECLI(Nubia):
    def _parse_args(self, cli_args=sys.argv):
        args = super()._parse_args(cli_args)
        setattr(args, "verbose", True)
        setattr(args, "stderr", True)
        return args


class POEToolPlugin(PluginInterface):
    def get_opts_parser(self, add_help=True):
        opts_parser = argparse.ArgumentParser(
            description="PoE data tool",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=add_help,
        )
        return opts_parser


def main():
    shell = POECLI(
        name="poe_tool",
        command_pkgs=tool.cli.commands,
        plugin=POEToolPlugin(),
        options=Options(persistent_history=True),
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()