# encoding:utf-8


import ipaddress
import textwrap
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawTextHelpFormatter


class ARGS:
    INTERFACE = None
    GATEWAY = None
    PERIOD = None
    SYSTEMD = None


class CustomArgumentFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    # https://stackoverflow.com/a/65891304
    """Formats argument help which maintains line length restrictions as well as appends default value if present."""

    def _split_lines(self, text, width):
        text = super()._split_lines(text, width)
        new_text = []

        # loop through all the lines to create the correct wrapping for each line segment.
        for line in text:
            if not line:
                # this would be a new line.
                new_text.append(line)
                continue

            # wrap the line's help segment which preserves new lines but ensures line lengths are
            # honored
            new_text.extend(textwrap.wrap(line, width))

        return new_text


def sort_argparse_help(parser: ArgumentParser):
    for g in parser._action_groups:
        g._group_actions.sort(key=lambda x: x.dest)


parser = ArgumentParser(prog='wireguard-reconnect', description='This program performs unattended handling of selected WireGuard interfaces, '
                                                                'bringing them up and down depending on whether there is connectivity to the server or not, '
                                                                'or simply bringing them up and keeping them up.\nWorks great combined with systemd.', formatter_class=CustomArgumentFormatter)
parser.add_argument('--interface', '-i', default='wg0', type=lambda x: x.strip(), help='the interface to be set and kept up')
parser.add_argument('--gateway', '-g', metavar='IP', type=lambda x: str(ipaddress.ip_address(x.strip())),
                    help='if specified, the program pings periodically this IP through the selected WireGuard interface. If there is no response, the WireGuard interface is removed.')
parser.add_argument('--period', '-p', metavar='SECONDS', default=20, type=float,
                    help='- If the specified WireGuard interface is not set, this is how long to wait before trying to bring it up.\n'
                         '•• If a gateway has been specified and there is no connection to it, the interface will not be set up.\n\n'
                         '- If the specified WireGuard interface is up, this is how long to wait before checking that it is still up.\n'
                         '•• If a gateway has been specified and there is no connection to it, the interface will be removed.')

sort_argparse_help(parser)


def parse_args():
    args = parser.parse_args()
    ARGS.INTERFACE = args.interface
    ARGS.GATEWAY = args.gateway
    ARGS.PERIOD = args.period
