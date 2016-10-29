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

import eventlet
import json
import os
from eventlet.green import thread
import logging
import sys
import argparse

import defaults

class App:
   def __init__(self,app_name='myapp',version='0.1',app_desc='My application that does nothing'):
       self.app_name    = app_name
       self.app_desc    = app_desc
       self.app_version = '0.1'
       self.data_dir    = ''
       self.init_cmdline()
       print 'Starting up %s, version %s' % (self.app_name,self.app_version)
       self.init_data_dir()
       self.init_logger()
       self.load_config()
       self.exc_count = 0
       self.running = True
       self.run_mainloop()
   def run_mainloop(self):
       """ Don't override this
       """
       while self.running:
          try:
             self.iter_loop()
          except Exception,e:
             logging.exception('Error in application main loop')
             self.exc_count += 1
             if self.exc_count >= 10:
                logging.critical('Too many exceptions')
                self.running = False
   def iter_loop(self):
       """ Override this to do stuff
       """
       raise Exception('test')
   def init_cmdline(self):
       """ Don't override this
       """
       parser = argparse.ArgumentParser(description=self.app_desc)
       parser.add_argument("-c", "--config", help="specify which config file to use")
       parser.add_argument("-D", "--debug", help="show debug information on the console",action="store_true")
       parser.add_argument("-d", "--datadir", help="specify the path to the data directory")
       self.args = parser.parse_args()
   def default_logging_config(self):
       """ Override this if you want a different default logging config
       """
       retval = defaults.logging_config
       return defaults.fillin_dict(retval,self)
   def default_datadir_path(self):
       """ Override this if you want a different default data directory path
           It should be obvious that this can not be overridden at runtime by config files
           Only by command line parameters
       """
       retval = defaults.fillin(defaults.datadir,self)
       return retval
   def default_config_file(self):
       """ Override this if you want to load your config file from somewhere weird
       """
       retval = defaults.fillin(defaults.config_file,self)
       return retval
   def default_config_settings(self):
       """ Please do override this with sane stuff
       """
       retval = defaults.fillin_dict(defaults.config_settings,self)
       return retval
   def init_data_dir(self):
       if self.args.datadir != None:
          self.data_dir = self.args.datadir
       else:
          self.data_dir = self.default_datadir_path()
       if not os.path.exists(self.data_dir):
          print 'Could not find data directory, recreating...'
          os.mkdir(self.data_dir)
   def init_logger(self):
       self.logging_config    = self.default_logging_config()
       logging.basicConfig(**self.logging_config)
       self.console_log       = logging.StreamHandler()
       self.console_logfmt    = self.logging_config.get('format',defaults.log_fmt_string)
       self.console_formatter = logging.Formatter(self.console_logfmt)
       self.console_log.setFormatter(self.console_formatter)
       self.console_log.setLevel(logging.INFO)
       logging.getLogger('').addHandler(self.console_log)
       logging.info('Logging system started')
   def load_config(self):
       if self.args.config != None:
          self.config_file = self.args.config
       else:
          self.config_file = self.default_config_file()
       if not os.path.exists(self.config_file):
          logging.info('Config file %s found, writing a default' % self.config_file)
          self.config_settings = self.default_config_settings()
          json_data = json.dumps(self.config_settings,sort_keys=True,indent=4)
          fd = open(self.config_file,'w')
          fd.write(json_data)
          fd.close()
          logging.info('Wrote config file to disk at %s' % self.config_file)
       else:
          logging.info('Loading configuration from %s' % self.config_file)
          fd = open(self.config_file,'r')
          json_data = fd.read()
          fd.close()
          self.config_settings = json.loads(json_data)
          logging.info('Loaded configuration from disk')
       

if __name__=='__main__':
   my_app = App()
