import os
import subprocess
import pathlib

from appdirs import user_config_dir


def main():
    config_dir = pathlib.Path(user_config_dir('FTPd'))
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    config = config_dir / "settings.py"
    if not config.exists():
        with config.open('w') as fh:
            fh.write(r"""
SERVER_ROOT_DIR = r"d:\ftp"

SERVER_USER_PERMS = "elradfmw"
SERVER_USER_AUTH_URL = "???"
SERVER_USER_AUTH_KEY = "???"

SERVER_PORT = 2121
SERVER_MAX_CONS = 256
SERVER_MAX_CONS_PER_IP = 5
SERVER_BANNER = "Welcome to FTPd"

# Specify a masquerade address and the range of ports to use for
# passive connections (in case you're behind a NAT).
# SERVER_MASQUERADE_ADDRESS = '123.123.123.123'
# SERVER_PASSIVE_PORTS = range(60000, 65535)
""")
    subprocess.check_call(["cmd", "/c", "start", "notepad", str(config)])

if __name__ == "__main__":
    main()