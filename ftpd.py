import os
import sys
import logging
import traceback
import msvcrt
import pathlib

from pyftpdlib.authorizers import AuthenticationFailed
from pyftpdlib import handlers
from pyftpdlib.servers import FTPServer
import requests


class Authorizer(object):
    def __init__(self, auth_key, auth_url, root, perms):
        self.auth_key = auth_key
        self.auth_url = auth_url
        self.root = root
        self.perms = perms

    def validate_authentication(self, user, password, handler):
        response = requests.post(self.auth_url, data=dict(
            key=self.auth_key,
            user=user,
            password=password,
        ), headers={
            'User-Agent': 'Mozilla/5.0',
        })
        json = response.json()
        if json['result'] != 'success':
            raise AuthenticationFailed("Wrong username/password combination.")

    def get_home_dir(self, username):
        path = self.root / username
        if not path.exists():
            path.mkdir(parents=True)
        return str(path)

    def get_msg_login(self, username):
        return "Login successful."

    def get_msg_quit(self, username):
        return "Goodbye."

    def get_perms(self, username):
        return self.perms

    def has_perm(self, username, perm, path=None):
        return perm in self.get_perms(username)

    def impersonate_user(self, username, password):
        pass

    def terminate_impersonation(self, username):
        pass


def main():
    try:
        logging.basicConfig(level="DEBUG")
        import settings

        class FTPHandler(handlers.FTPHandler):
            authorizer = Authorizer(
                settings.SERVER_USER_AUTH_KEY,
                settings.SERVER_USER_AUTH_URL,
                pathlib.Path(settings.SERVER_ROOT_DIR),
                settings.SERVER_USER_PERMS
            )
            banner = settings.SERVER_BANNER
            if hasattr(settings, 'SERVER_MASQUERADE_ADDRESS'):
                masquerade_address = settings.SERVER_MASQUERADE_ADDRESS
            if hasattr(settings, 'SERVER_PASSIVE_PORTS'):
                passive_ports = settings.SERVER_PASSIVE_PORTS

        server = FTPServer((settings.SERVER_HOST, settings.SERVER_PORT), FTPHandler)
        server.max_cons = settings.SERVER_MAX_CONS
        server.max_cons_per_ip = settings.SERVER_MAX_CONS_PER_IP
        server.serve_forever()
    except Exception as exc:
        print("""
*******************************************************************************
*** INTERNAL FAILURE: {} ***
*******************************************************************************
""".format(exc))

        traceback.print_exc()

        print("""
*******************************************************************************
**************************** PRESS ANY KEY TO EXIT ****************************
*******************************************************************************
""")
        msvcrt.getch()


if __name__ == '__main__':
    main()
