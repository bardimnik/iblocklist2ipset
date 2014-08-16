# -*- coding: utf-8 -*-


from __future__ import print_function

import functools
import time
import sys
import os
import os.path
import posixpath
import re

from .settings import TIME_TO_SLEEP


def try_if_empty(count):
    assert count >= 1

    def outer_decorator(func):
        @functools.wraps(func)
        def inner_decorator(*args, **kwargs):
            for attempt in xrange(count - 1):
                try:
                    result = func(*args, **kwargs)
                except Exception as exc:
                    print(u"[{}/{}] Error during parsing: {}".format(
                        attempt, count, exc
                    ), file=sys.stderr)
                    time.sleep(TIME_TO_SLEEP)
                else:
                    return result
            return func(*args, **kwargs)

        return inner_decorator
    return outer_decorator


def script_example_header(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        print("#!/bin/bash\nset -e", end="\n\n")

        if os.getenv("VIRTUAL_ENV"):
            script_path = posixpath.join(
                os.getenv("VIRTUAL_ENV"), "bin", "activate"
            )
            print('source {}'.format(printable_path(script_path)), end="\n\n")

        return func(*args, **kwargs)
    return decorator


def printable_path(path):
    abspath = os.path.abspath(path)
    if re.search(r"\s", abspath) is not None:
        abspath = '"' + abspath.replace('"', r'\"') + '"'
    return abspath
