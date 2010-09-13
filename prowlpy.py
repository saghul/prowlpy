#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, Jaccob Burch
# Copyright (c) 2010, Olivier Hervieu
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# * Neither the name of the University of California, Berkeley nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Prowlpy V0.42 originally written by Jacob Burch, modified by Olivier Hervieu.

Python Prowlpy is a python module that implement the public api of Prowl to
send push notification to iPhones.

See http://prowl.weks.net for information about Prowl.

The prowlpy module respect the API of prowl. So prowlpy provides a Prowl class
which implements two methods :
- post, to push a notification to an iPhone,
- verify_key, to verify an API key.
"""

__author__ = 'Jacob Burch'
__author_email__ = 'jacoburch@gmail.com'
__maintainer__ = 'Olivier Hervieu'
__maintainer_email__ = 'olivier.hervieu@gmail.com'
__version__ = '0.42'

from httplib import HTTPSConnection, HTTPException
from urllib import urlencode

API_DOMAIN = 'prowl.weks.net'

class ProwlError(Exception): pass
class ProwlAuthError(ProwlError): pass
class Prowl(object):

    def __init__(self, apikey, providerkey=None):
        self.apikey = apikey
        self.providerkey = providerkey

        # Set User-Agent
        self.headers = {'User-Agent': "Prowlpy/%s" % __version__,
                        'Content-type': "application/x-www-form-urlencoded"}

    def post(self, application=None, event=None, description=None, priority=0):
        """
        Post a notification..

        You must provide either event or description or both.
        The parameters are :
        - application ; The name of your application or the application
          generating the event.
        - priority (optional) : default value of 0 if not provided.
          An integer value ranging [-2, 2] representing:
             -2. Very Low
             -1. Moderate
              0. Normal
              1. High
              2. Emergency (note : emergency priority messages may bypass
                            quiet hours according to the user's settings)
        - event : the name of the event or subject of the notification.
        - description : a description of the event, generally terse.
        """
        h = HTTPSConnection(API_DOMAIN)
        data = {
            'apikey': self.apikey,
            'application': application,
            'event': event,
            'description': description,
            'priority': priority
        }
        if self.providerkey is not None:
            data['providerkey'] = providerkey
        h.request("POST",
                  "/publicapi/add",
                  headers = self.headers,
                  body = urlencode(data))
        try:
            response = h.getresponse()
        except HTTPException, e:
            raise ProwlError("Error sending request: %s" % str(e))
        else:
            status = response.status
            if status == 200:
                pass
            elif status == 401: 
                raise ProwlAuthError("Auth Failed: %s" % response.reason)
            else:
                raise ProwlError("Unknown error")

    def verify_key(self):
        h = HTTPSConnection(API_DOMAIN)
        data = {'apikey' : self.apikey}
        if self.providerkey is not None:
            data['providerkey'] = providerkey
        h.request("GET",
                  "/publicapi/verify?"+ urlencode(data),
                  headers=self.headers)
        try:
            response = h.getresponse()
        except HTTPException, e:
            raise ProwlError("Error verifying key: %s" % str(e))
        else:
            if response.status != 200:
                raise ProwlAuthError("Invalid API Key %s" % self.apikey)


