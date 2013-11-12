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

    def __init__(self, api_url='http://localhost:8000/v1', *args):
        super(Client, self).__init__(*args)
        self.BASE_URL = api_url


class Account(object):
    def __init__(self, acct_id):
        self.acct_id = acct_id
        self.verbosity = 0
        self.api = Client(args.api_url, args.api_key)
        self.api.authenticate()

    def __repr__(self):
        return str(self.acct_id)

    def _get_user_input(self, question, is_mandatory, def_val):
        """ Ask user for input.
            (str, bool, str) -> str or None"""

        try:
            # If it's not mandatory, offer the user to pass on.
            if not is_mandatory:
                if raw_input('Set %s (y/N)?' % question).lower() != 'y':
                    return None

            # Get the user's input and return it (in unicode)
            input = raw_input('%s (ex: %s)? ' % (question, def_val))
            return input.encode('utf-8') if len(input) else def_val

        except ValueError, e:
            print ("Invalid input: %s" % e)

        return None

    def _get_user_input_multi(self, d):
        """ Fills nested dict with _get_user_input() and pop() non
            mandatory keys.
            (dict containing tuples) -> dict"""

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

    def _api_send_req(self, cmd, data=None):
        """ Calls kazoo-api functions. See
        https://kazoo-api.readthedocs.org/en/latest/
        (str, str or dict) -> str or False"""

        if self.verbosity > 0:
            print " -> kazoo.api.%s(%s, %s)" % (cmd, self.acct_id, data)

        try:
            if data: 
                return getattr(self.api, cmd)(self.acct_id, data)
            else:
                return getattr(self.api, cmd)(self.acct_id)

        except kazoo.exceptions.KazooApiError, e:
            print ' * ERR (KazooApiError): %s' % e
        except kazoo.exceptions.KazooApiBadDataError, e:
            print ' * ERR (ApiBadDataError): %s' % e

        return False

    def create_device(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Devices+API
            () -> dict or False"""

        properties = {
            'name': ("Name", True, u"Joe's Office Phone"),
            'owner_id': ("Owner ID", True, u"1b5edd11f3464..."),
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
        properties = self._get_user_input_multi(properties)
        return self._api_send_req('create_voicemail_box', properties)

    def create_phone_number(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Phone+Number+APIs
            () -> dict or False"""

        phone_number = self._get_user_input("Phone number", True, "+44132...")
        return self._api_send_req('create_phone_number', phone_number)

    def create_voicemail_box(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Build+a+Voicemail+Service
            () -> dict or False"""

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
        properties = self._get_user_input_multi(properties)
        return self._api_send_req('create_voicemail_box', properties)

    def delete_callflow(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Callflows+API
            () -> dict or False"""

        callfow_id = self._get_user_input("Callflaw ID", True, "9cef8acde...")
        return self._api_send_req('delete_callflow', callfow_id)

    def get_account(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Accounts+API
            () -> dict or False"""

        return self._api_send_req('get_account')

    def get_account_children(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Accounts+API
            () -> dict or False"""

        return self._api_send_req('get_account_children')

    def get_account_descendants(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Accounts+API
            () -> dict or False"""

        return self._api_send_req('get_account_descendants')
        

    def get_all_devices_status(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Devices+API
            () -> dict or False"""

        return self._api_send_req('get_all_devices_status')

    def get_all_media(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Resources+API
            () -> dict or False"""

        return self._api_send_req('get_all_media')

    def get_callflow(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Callflows+API
            () -> dict or False"""

        callfow_id = self._get_user_input("Callflaw ID", True, "9cef8acde...")
        return self._api_send_req('get_callflow', callfow_id)

    def get_callflows(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Callflows+API
            () -> dict or False"""

        return self._api_send_req('get_callflows')

    def get_device(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Devices+API
            () -> dict or False"""

        device_id = self._get_user_input("Device ID", True, "9cef8acde...")
        return self._api_send_req('get_device', device_id)

    def get_devices(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Devices+API
            () -> dict or False"""

        return self._api_send_req('get_devices')

    def get_users(self, args=[]):
        """ https://2600hz.atlassian.net/wiki/display/docs/Devices+API
            () -> dict or False"""

        return self._api_send_req('get_users')


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
    account.verbosity = args.verbosity

    do = getattr(account, args.cmd)(*args.cmd_arg)
    display_json(do) if do else 'err'


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
