#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/2/28  
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
from functools import reduce
from noba.snippet import *
from noba.Core import core

class Pipeline:
    def __init__(self, container=core):
        self.container = container
        self.method = 'handle'
        self.pipes = list()
        self._pipeline_folder = 'pipeline'

    def folder(self, folder):
        self._pipeline_folder = folder
        return self

    def send(self, passable):
        self.passable = passable
        return self

    def through(self, pipes, *args):
        self.pipes = pipes if isinstance(pipes, list) else list(args)
        return self


    def pipe(self, pipes, *args):
        (self.pipes).extend(pipes if is_list(pipes) else list(args))
        return self

    def via(self, method):
        self.method = method
        return self

    def then(self, destination):
        pipeline = reduce(
            self.__carry(), self._pipes()[::-1], self._prepare_destination(destination)
        )

        return pipeline(self.passable)

    def then_return(self):
        return self.then(lambda passable:passable)


    def _prepare_destination(self, destination):
        def func(passable):
            try:
                return destination(passable)
            except Exception as e:
                return self._handle_exception(passable, e)
        return func

    def __carry(self):
        def one_func(stack, piper):
            def two_func(passable):
                pipe = piper
                try:
                    if (is_function(pipe)):
                        # If the pipe is a callable, then we will call it directly, but otherwise we
                        # will resolve the pipes out of the dependency container and call it with
                        # the appropriate method and arguments, returning the results back out.
                        return pipe(passable, stack)
                    elif (is_str(pipe)):
                        name, parameters_r = self._parse_pipe_string(pipe)
                        # If the pipe is a string we will parse the string and resolve the class out
                        # of the dependency injection container. We can then build a callable and
                        # execute the pipe function giving in the parameters that are required.
                        pipe = self._get_container().make(name)
                        # parameters = [passable, stack].extend(parameters)
                        parameters = [passable, stack]
                        parameters.extend(parameters_r)
                    else:
                        # If the pipe is already an object we'll just make a callable and pass it to
                        # the pipe as-is. There is no need to do any extra parsing and formatting
                        # since the object we're given was already a fully instantiated object.
                        parameters = [passable, stack]

                    # print(parameters)
                    carry = getattr(pipe, self.method)(*parameters) if hasattr(pipe, self.method) else pipe(*parameters)
                    return self._handle_carry(carry)

                except Exception as e:
                    return self._handle_exception(passable, e)

            return two_func
        return one_func

    def _parse_pipe_string(self, pipe):
        split = [x for x in pipe.split(':', 2)]

        if len(split) < 2:
            split.append([])
        name, parameters = split

        if is_str(parameters):
            parameters = parameters.split(',')

        if not self._pipeline_folder in name:
            name = self._pipeline_folder + '.' + name
        return [name, parameters]

    def _pipes(self):
        return self.pipes

    def _get_container(self):
        if (not self.container):
            raise RuntimeError('A container instance has not been passed to the Pipeline.')

        return self.container

    def set_container(self, container):
        self.container = container
        return self

    def _handle_carry(self, carry):
        return carry

    def _handle_exception(self, passable, e):
        raise e