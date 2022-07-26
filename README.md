# WireGuard Reconnect

[![PyPI](https://img.shields.io/pypi/v/wireguard-reconnect?label=latest)](https://pypi.org/project/wireguard-reconnect/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wireguard-reconnect)
![PyPI - Status](https://img.shields.io/pypi/status/wireguard-reconnect)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/fernandoenzo/wireguard-reconnect)
![PyPI - License](https://img.shields.io/pypi/l/wireguard-reconnect)

This program performs unattended handling of selected WireGuard interfaces, bringing them up and down depending on whether there is connectivity to the server or not, or simply bringing them up and
keeping them up.

Works great combined with systemd.

## Table of contents

<!--ts-->

* [Installation](#installation)
* [Use case](#use-case)
* [How to use it](#how-to-use-it)
    * [With systemd](#with-systemd)
* [Packaging](#packaging)
    * [Autopackage](#autopackage)
    * [PyInstaller](#pyinstaller)
* [Contributing](#contributing)
* [License](#license)

<!--te-->

## Installation

Use the package manager [**pip**](https://pip.pypa.io/en/stable/) or [**pipx**](https://github.com/pypa/pipx) to install it:

```bash
sudo pip install wireguard-reconnect
```

Alternatively, you can use one of the two portable versions provided on the releases page.

- The lightest one has been packaged using [**autopackage**](https://pypi.org/project/autopackage/) and will require you to have Python 3.7+ installed.
- The heavier one has been packaged using [**PyInstaller**](https://pyinstaller.org) and has no external dependencies, so it doesn't matter if you don't have Python installed, or if your version is
  lower than 3.7.

See [Packaging](#packaging) for more information.

## Use case

I have two VPNs installed simultaneously on my computers, one with OpenVPN (in TCP mode, device `tun0`) and the other with WireGuard (UDP, device `wg0`), which allow me to access the same subnets
behind certain computers.

Knowing the great advantage in speed and ease of use of WireGuard over OpenVPN, one might wonder what's the point of having OpenVPN installed as well and maintaining this redundant network scheme,
and the answer is very simple: compatibility. Both at my work and on many public Wi-Fi networks, UDP traffic is blocked and the only way I can access the aforementioned subnets is by using OpenVPN.

The configuration that I have made of both programs prioritizes in the routing table, for access to said subnets, the use of WireGuard over OpenVPN, giving it a lower metric, so that the link used
is the fastest possible. Something like this:

```commandline
192.168.1.0/24 dev wg0 metric 1000 
192.168.1.0/24 dev tun0 metric 2000 
10.4.0.0/24 dev wg0 metric 1000 
10.4.0.0/24 dev tun0 metric 2000 
```

The problem arises when, with UDP traffic blocked, the routing table insists on using WireGuard instead of OpenVPN. It's in those cases where it's necessary, to allow the traffic flow,
that the WireGuard interface disappears from the system. And, if at any point we switch to a Wi-Fi network where WireGuard can work on, we'll want its interface back up.

Of course, I could do all of this by hand, bringing up and down the WireGuard interface depending on whether I detect that the Wi-Fi I'm on allows UDP traffic or not (beyond DNS,
obviously), but instead I preferred to make a small Python program that, by the way, had a good integration with systemd.

## How to use it

If you want to bring up a WireGuard interface called `wg0` and just check every 30 seconds (default is 20 seconds) that it's still up, run the following command. You probably want this behaviour
on your WireGuard server, but not on clients.

```commandline
sudo wireguard-reconnect -i wg0 -p 30
```

If instead you want to set up a WireGuard interface called `wg1` and check every minute whether the server is reachable (using its WireGuard local IP `10.4.0.1`) so that,
in case there is no connectivity, the `wg1` interface is removed from the system, and then try to bring it up back again if the connection to the server can be reestablished,
then run this command:

```commandline
sudo wireguard-reconnect -i wg1 -g 10.4.0.1 -p 60
```

In any case, if the program is stopped by a SIGINT (2) signal (Control+C) or a SIGTERM (15) signal (such as those sent by `systemctl stop` or `kill` commands), the WireGuard interface will be
removed from the system.

There is also a `--help/-h` option in the program. Don't forget to read it if you forget something:

```commandline
sudo wireguard-reconnect -h
```

### With systemd

It's strongly advised to manage this program using the provided systemd service template in this repository.

You just need to copy the file called `wireguard-reconnect@.service` to your `/etc/systemd/system` folder and run the following commands to bring up interface `wg0`
checking connectivity to server `10.4.0.1`:

```commandline
sudo systemctl daemon-reload
sudo systemctl start wireguard-reconnect@wg0-10.4.0.1.service
```

To make the service to start at system boot, execute:

```commandline
sudo systemctl enable wireguard-reconnect@wg0-10.4.0.1.service
```

To watch the program log:

```commandline
sudo journalctl -u wireguard-reconnect@wg0-10.4.0.1.service -f
```

## Packaging

In this section we are going to explain how to replicate the packaging process.

### Autopackage

To generate the program lightest portable version, which is available in this GitHub repository, install first `autopackage` with `pip`:

```commandline
pip install autopackage
```

Then run the following commands:

```commandline
autopackage -s setup.py -p
```

### PyInstaller

To generate the program heaviest portable version, which is also available in this GitHub repository, install `pyinstaller` with `pip`:

```
pip install pyinstaller
```

Then run:

```
pyinstaller --onefile --bootloader-ignore-signals __main__.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

![PyPI - License](https://img.shields.io/pypi/l/wireguard-reconnect)

This library is licensed under the
[GNU Affero General Public License v3 or later (AGPLv3+)](https://choosealicense.com/licenses/agpl-3.0/)
