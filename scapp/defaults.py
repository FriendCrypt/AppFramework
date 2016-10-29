"""
FriendCrypt Application framework
Copyright (C) 2016 Gareth Nelson

This file is part of the FriendCrypt Application Framework

The FriendCrypt Application Framework is free software: you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 2 of the License, 
or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

""" This file contains defaults used by app.py
    You may override them by overriding the relevant method in the App class when inheriting from it
    At runtime these defaults may also be overridden by the end user
    Most of these settings use a simple template system too:
      %APPNAME% translates to the application name
      %APPVER%  translates to the application version
      %DATADIR% translates to the application's data directory
    If a default is using a template, it uses the function fillin() below to fillin these fields
"""

def fillin(s,app):
    """ Fill in the template fields in the provided string using the settings from the app
        Return the filled in string
    """
    s = s.replace('%APPNAME%',app.app_name)
    s = s.replace('%APPVER%', app.app_version)
    s = s.replace('%DATADIR%',app.data_dir)
    return s

def fillin_dict(d,app):
    """ Like fillin() above, but does it for the values in a dict
    """
    retval = dict(d.items())
    for k,v in retval.items():
        if type(v) is str:
           retval[k] = fillin(retval[k],app)
    return retval

import logging
log_fmt_string = '%(asctime)8s: %(levelname)-8s %(message)s'
logging_config = {'filename':'%DATADIR%/debug.log',
                  'level'   :logging.DEBUG,
                  'format'  :log_fmt_string}

import os
datadir = os.path.expanduser('~/.%APPNAME%-%APPVER%')

config_file = '%DATADIR%/%APPNAME%-config.json'

# you should REALLY override default_config_settings() in the App class
config_settings = {}
