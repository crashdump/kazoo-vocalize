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

    def __repr__(self):
        return str(self.acct_id)

    def _get_user_input(self, question, is_mandatory, def_val):
        """ Ask a question to the user and return the answer or None"""
        try:
            # If it's not mandatory, offer the user to pass on.
            if not is_mandatory:
                if raw_input('Set %s (y/N)?' % question).lower() != 'y':
                    return None

            # Get the user's input and return it (in unicode)
            input = raw_input('%s (ex: %s)? ' % (question, def_val))
            return input.encode('utf-8') if len(input) > 1 else def_val

        except ValueError, e:
            print ("Invalid input: %s" % e)
            return None

    def _get_user_input_multi(self, d):
        """ Get a dict and feed _get_user_input() with it. Returns a dict."""
        # If it's a dict, let's dig...
        if isinstance(d, dict):
            # Sort the questions: mandatory fields first
            for k, v in d.items():
                # Not a tuple, keep diging
                if isinstance(v, dict):
                    d[k] = self._get_user_input_multi(v)
                else:
                    (question, is_mandatory, def_val) = v
                    a = self._get_user_input(question, is_mandatory, def_val)
                    # Update the value if answered, else pop it.
                    if a is None:
                        del d[k]
                    else:
                        d[k] = a
        return d

    def create_device(self, args=[]):
        """ inputs: name, sip/realm, sip/method, sip/username,
                    sip/password, caller_id/external/number,
                    owner_id"""

        properties = {
            'name': ("Name", True, u"Joe's Office Phone"),
            'owner_id': ("Owner ID", True, u"4152ed2b42"),
            'sip': {
                'realm': ("SIP Realm", True, u"whistle.yourdomain.net"),
                'method': ("SIP Auth method", True, u"password"),
                'username': ("SIP Username", True, u"user_abcd1"),
                'password': ("SIP Password", True, u"1234"),
                'invite_format': ("SIP Invite format", False, u"username"),
            },
            'media': {
                'progress_timeout': ("Media progress timeout", False, u"6"),
                'bypass_media': ("Media bypass", False, u"false")
            },
            'caller_id': {
                'external': {
                    'number': ("External caller ID", True, u"5555555555")
                }
            }
        }

        data = self._get_user_input_multi(properties)

        print data

        try:
            return self.api.create_voicemail_box(self.acct_id, data) \
                if data else False
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def create_phone_number(self, args=[]):
        """ inputs: phone_number"""
        phone_number = self._get_user_input("Phone number", True, "+44132...")
        try:
            return self.api.create_phone_number(self.acct_id, phone_number) \
                if phone_number else False
        except kazoo.exceptions.KazooApiError, e:
            print 'Err: %s' % e
        return False

    def create_voicemail_box(self, args=[]):
        """ inputs: mailbox, name """
        properties = {
            'mailbox': ("Mailbox number", True, u"9001"),
            'name': ("Mailbox name", True, u"Mailbox 9001"),
            'pin': ("Pin", False, u"1234"),
            'timezone': ("Timezone", False, u"Europe/London"),
            'require_pin': ("Require pin", False, u"true"),
            'check_if_owner': ("Check if owner", False, u"true"),
            'skip_greeting': ("Skip greeting", False, u"true"),
            'skip_instructions': ("Skip instructions", False, u"false"),
            'owner_id': ("Owner id", False, u"1b5edd11f3464...")
        }

        data = self._get_user_input_multi(properties)

        try:
            return self.api.create_voicemail_box(self.acct_id, data) \
                if data else False
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def delete_callflow(self, args=[]):
        """ inputs: callflow_id"""
        callfow_id = self._get_user_input("Callflaw ID", True, "9cef8acde...")
        try:
            return self.api.delete_callflow(self.acct_id, callfow_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_account(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_account(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_account_children(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_account_children(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_account_descendants(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_account_descendants(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_all_devices_status(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_all_devices_status(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_all_media(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_all_media(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e

    def get_callflow(self, args=[]):
        """ inputs: callflow id """
        callfow_id = self._get_user_input("Callflaw ID", True, "9cef8acde...")
        try:
            return self.api.get_callflow(self.acct_id, callfow_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_callflows(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_callflows(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_device(self, args=[]):
        """ inputs: callflow id """
        device_id = self._get_user_input("Device ID", True, "9cef8acde...")
        try:
            return self.api.get_device(self.acct_id, device_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_devices(self, args=[]):
        """ inputs: none """
        try:
            return self.api.get_devices(self.acct_id)
        except kazoo.exceptions.KazooApiError, e:
            print 'ERR (KazooApiError): %s' % e
        return False

    def get_users(self, args=[]):
        """ inputs: none """
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
