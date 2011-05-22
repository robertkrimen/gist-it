#!/usr/bin/env python
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Memcache wrapper that transparently adds app version

This wraps google.appengine.api.memcache, adding a namespace
parameter to all calls that is based on the app version 
environment variable (os.environ["CURRENT_VERSION_ID"]). This
means new versions of the app will not access cached entries
from an old version, so no cache flushing is required when
changing app versions.
"""

# Pylint doesn't like the names memcache uses -- disable those warnings
# Also disabling no docstring warning
# pylint: disable-msg=C0111
# pylint: disable-msg=W0622

import os

from google.appengine.api import memcache

#
# Wrap memcache API calls with calls that set the namespace to
# the App Engine version string, obtained from the environment
# variables.
#
# These calls do not support a namespace parameter, so as not
# to confuse the user.
#
# The Client() object is not supported by this wrapper either.
#

def get(key):
  return memcache.get(key, 
    namespace=os.environ["CURRENT_VERSION_ID"])

def get_multi(keys, key_prefix=''):
  return memcache.get_multi(keys, key_prefix,
    namespace=os.environ["CURRENT_VERSION_ID"])

def delete(key, seconds=0):
  return memcache.delete(key, seconds,
    namespace=os.environ["CURRENT_VERSION_ID"])

def delete_multi(keys, seconds=0, key_prefix=''):
  return memcache.delete_multi(keys, seconds, key_prefix,
    namespace=os.environ["CURRENT_VERSION_ID"])

def set(key, value, time=0, min_compress_len=0):
  return memcache.set(key, value, time, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def add(key, value, time=0, min_compress_len=0):
  return memcache.add(key, value, time, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def replace(key, value, time=0, min_compress_len=0):
  return memcache.replace(key, value, time, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def set_multi(mapping, time=0, key_prefix='', min_compress_len=0):
  return memcache.set_multi(mapping, time, key_prefix, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def add_multi(mapping, time=0, key_prefix='', min_compress_len=0):
  return memcache.add_multi(mapping, time, key_prefix, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def replace_multi(mapping, time=0, key_prefix='', min_compress_len=0):
  return memcache.replace_multi(mapping, time, key_prefix, min_compress_len,
    namespace=os.environ["CURRENT_VERSION_ID"])

def incr(key, delta=1, initial_value=None):
  return memcache.incr(key, delta,
    namespace=os.environ["CURRENT_VERSION_ID"],
    initial_value=initial_value)

def decr(key, delta=1, initial_value=None):
  return memcache.decr(key, delta,
    namespace=os.environ["CURRENT_VERSION_ID"],
    initial_value=initial_value)

def flush_all():
  return memcache.flush_all()

def get_stats():
  return memcache.get_stats()

