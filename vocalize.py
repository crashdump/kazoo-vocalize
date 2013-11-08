#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Adrien Pujol - http://www.crashdump.fr/"
__copyright__ = "Copyright 2013, Adrien Pujol"
__license__ = "Mozilla Public License"
__version__ = "0.1-alpha"
__email__ = "adrien.pujol@crashdump.fr"
__status__ = "Development"
__doc__ = """
Vocalize is a client for Crossbar, the Kazoo's RESTfull API.
It lets you get Kazoo up and running quickly for the shell.

Dependencies:
 - argparse: https://pypi.python.org/pypi/argparse 
 - kazoo-api: https://pypi.python.org/pypi/kazoo-api
"""

import sys
import json
import kazoo
import argparse

class Client(kazoo.Client):
    """ Client class inherited from kazoo.Client Object. Allow us to set
        api_url: Client(api_url, api_key=None, password=None,
        account_name=None, username=None) """
    def __init__(self, api_url=None, *args):
        super(Client, self).__init__(*args)
        self.BASE_URL = api_url if api_url else 'http://localhost:8000/v1'


class Account(object):
    def __init__(self, acct_id):
        self.acct_id = acct_id
        self.api = Client(args.api_url, args.api_key)
        self.api.authenticate()

    def create_callflow(self, args=[]):
        """ args: number, flow"""
        if len(args) < 1:
            print 'cmd usage: ./vocalize.py api_key account_id', \
                    'create_callflow number flow'
            return False
        try:
            return self.api.create_callflow(self.acct_id, args[0])
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def create_phone_number(self, args=[]):
        """ args: number"""
        if len(args) < 1:
            print 'cmd usage: ./vocalize.py api_key account_id', \
                    'create_phone_number number'
            return False
        try:
            return self.api.create_phone_number(self.acct_id, args[0])
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def create_voicemail_box(self, args=[]):
        """ args: number"""
        if len(args) < 1:
            print 'cmd usage: ./vocalize.py api_key account_id', \
                    'create_voicemail_box data'
            return False
        try:
            return self.api.create_voicemail_box(self.acct_id, args[0])
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def delete_callflow(self, args=[]):
        """ args: callflow_id"""
        if len(args) < 1:
            print 'cmd usage: ./vocalize.py api_key account_id', \
                    'delete_callflow callflow_id'
            return False
        try:
            return self.api.delete_callflow(self.acct_id, args[0])
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_account(self, args=[]):
        """ args: none """
        try:
            return self.api.get_account(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_all_devices_status(self, args=[]):
        """ args: none """
        try:
            return self.api.get_all_devices_status(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_callflows(self, args=[]):
        """ args: none """
        try:
            return self.api.get_callflows(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_users(self, args=[]):
        """ args: none """
        try:
            return self.api.get_users(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False      


def display_json(json_data):
    print 'Request status: %s' % json_data['status']
    print 'Response content:'
    print json.dumps(json_data['data'], indent=4, ensure_ascii=True,
            sort_keys=True)


if __name__ == "__main__":
    cmd_list = [f for f in dir(Account) if not f.startswith('_')]

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--api-url', dest='api_url', action='store', 
                      default='http://localhost:8000/v1',
                      help='Crossbar API URL. http://localhost:8000/v1')
    parser.add_argument('-v', action='count', dest='verbosity', default=0)
    parser.add_argument('api_key', action='store', help='API Key')
    parser.add_argument('acct_id', action='store', help='Account ID')
    parser.add_argument('cmd', choices=cmd_list)
    parser.add_argument('cmd_arg', nargs='?', default=[],
            help='argument for the command, if needed')
    args = parser.parse_args()

    # @todo: Implement username/password/account login
    #client = kazoo.Client(username="myusername", password="mypassword",
    #                      account_name="my account name")

    account = Account(args.acct_id)

    do = getattr(account, args.cmd)(*args.cmd_arg)
    display_json(do) if do else 'err'


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
