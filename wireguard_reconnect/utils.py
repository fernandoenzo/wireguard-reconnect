# /usr/bin/env python3
# encoding:utf-8


import subprocess


def print_flush(*args, **kwargs):
    kwargs['flush'] = True
    return print(*args, **kwargs)


def header(title: str):
    hyphens = '-' * (len(title) + 2)
    return f' {hyphens}\n  {title}\n {hyphens}'


def run_command(command, systemd=False):
    cmd = []
    if systemd:
        cmd = ['systemd-run', '--scope', '--quiet']
    cmd.extend(command)
    return subprocess.run(cmd, capture_output=True, start_new_session=True, text=True)
