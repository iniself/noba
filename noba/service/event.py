#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/3/5  
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function, unicode_literals)
from noba.snippet import *

class EventHub:
    hubs = {}
    def __init__(self, event, name=None):
        if not is_list(event):
            event = [event]
        self._event = event
        self._listeners = list()
        if name and self._single(name):
            EventHub.hubs[name] = self

    def _single(self, name):
        if name in EventHub.hubs:
            print(f"[Error] EventHub '{name}' already exists!")
            exit()
        else:
            return True

    def name(self, name=None):
        if name and self._single(name):
            self._name = name
            EventHub.hubs[name] = self
        return self

    @classmethod
    def hub(cls, event, name=None):
        return cls(event, name)

    @classmethod
    def get_all_hub(cls):
        return cls.hubs

    @classmethod
    def drop(cls, name):
        del EventHub.hubs[name]

    @classmethod
    def get_hub(cls, name):
        try:
            return EventHub.hubs[name]
        except KeyError as e:
            print(f"EventHub '{name}' non-existent")
            exit()

    def get_events(self):
        return self._event

    def get_name(self):
        return get_key_by_value(EventHub.hubs, self)[0]

    @property
    def manager(self):
        return self.__class__

    def drop_me(self):
        del EventHub.hubs[self.get_name()]

    def watch(self, event, handler, always=False):
        if not event in self._event:
            print(f'[EventHub] watch，attempt to watch an invalid event：{event}. List of valid events: {self._event}')
            return

        self._listeners.append({
            'event': event,
            'always': always,
            'handler': handler,
            'trigger_count': 0,
            'limit_count': 1 if not always else  0
        })

    def fire(self, event, data=None):
        if not event in self._event:
            print(f'[EventHub] fire，attempt to trigger an invalid event：{event}. List of valid events: {self._event}')
            return

        for listener in self._listeners:
            if not listener['event'] == event:
                continue

            try:
                listener['handler'](data)

            except Exception as e:
                print(f"[EventHub] caught err when exec handler, err:, {e}, event:, {event}, handler:, {listener.handler}")

            listener['trigger_count'] += 1

        self._listeners = [listener for listener in self._listeners if not (listener['limit_count'] > 0 and listener['limit_count'] <= listener['trigger_count'])]

    def unwatch(self, event, handler):
        self._listeners = [listener for listener in self._listeners if not (listener['event'] == event)]









