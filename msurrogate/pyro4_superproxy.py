"""
"""
from __future__ import division, print_function, unicode_literals
from declarative.utilities.future_from_2 import unicode, str
import Pyro4
import numpy as np
import numbers


class NeedsSubSuper(Exception):
    pass


@Pyro4.expose
class SuperProxy(object):
    #these are used for garbage collection
    protect = False
    done    = False

    def __init__(
            self,
            daemon,
            obj,
            register = True,
            protect  = None,
    ):
        self.daemon = daemon

        if isinstance(register, (str, unicode)):
            self.uri = self.daemon.register(self, register)
            if protect is None:
                protect = True
        elif register:
            #automatic registration!
            self.uri = self.daemon.register(self)

            if protect is None:
                protect = False
        else:
            self.uri = None
            if protect is None:
                protect = False

        #only assign in the rare event of True
        if protect:
            self.protect = protect

        self.obj = obj
        return

    def pyrosuper_getattr(self, name):
        val = getattr(self.obj, name)
        return self.pyrosuper_wrap(val)

    def pyrosuper_setattr(self, name, val):
        unval = self.pyrosuper_unwrap(val)
        return setattr(self.obj, name, unval)

    def pyrosuper_getitem(self, idx):
        idx = self.pyrosuper_unwrap(idx)
        val = self.obj[idx]
        return self.pyrosuper_wrap(val)

    def pyrosuper_setitem(self, idx, val):
        idx = self.pyrosuper_unwrap(idx)
        unval = self.pyrosuper_unwrap(val)
        self.obj[idx] = unval
        return

    def pyrosuper_call(self, name, *args, **kwargs):
        if name is None:
            val = self.obj
        else:
            val = getattr(self.obj, name)
        unargs = self.pyrosuper_unwrap(args)
        unkwargs = self.pyrosuper_unwrap(kwargs)
        ret = val(*unargs, **unkwargs)
        return self.pyrosuper_wrap(ret)

    def pyrosuper_done(self):
        if not self.protect and self.done:
            raise RuntimeError("done set twice!")
        self.done = True

    def pyrosuper_wrap(self, obj, throw = False):
        """
        throw causes an exception instead of creating a sub SuperProxy
        """
        if isinstance(obj, np.ndarray):
            return obj
        elif isinstance(obj, numbers.Number):
            return obj
        elif isinstance(obj, list):
            try:
                sublist = [self.pyrosuper_wrap(o, throw = True) for o in obj]
            except NeedsSubSuper:
                if throw:
                    raise
                else:
                    return SuperProxy(self.daemon, obj)
            else:
                return sublist
        elif isinstance(obj, tuple):
            try:
                subtup = tuple((self.pyrosuper_wrap(o, throw = True) for o in obj))
            except NeedsSubSuper:
                if throw:
                    raise
                else:
                    return SuperProxy(self.daemon, obj)
            else:
                return subtup
        elif isinstance(obj, dict):
            try:
                subdict = dict()
                for k, v in obj.items():
                    subdict[k] = self.pyrosuper_wrap(v, throw = True)
            except NeedsSubSuper:
                if throw:
                    raise
                else:
                    return SuperProxy(self.daemon, obj)
            else:
                return subdict
        if throw:
            raise NeedsSubSuper()

        return SuperProxy(self.daemon, obj)

    def pyrosuper_unwrap(self, obj):
        """
        throw causes an exception instead of creating a sub SuperProxy
        """
        if isinstance(obj, list):
            sublist = [self.pyrosuper_unwrap(o) for o in obj]
            return sublist
        elif isinstance(obj, tuple):
            subtup = tuple((self.pyrosuper_unwrap(o) for o in obj))
            return subtup
        elif isinstance(obj, dict):
            subdict = dict()
            for k, v in obj.items():
                subdict[k] = self.pyrosuper_unwrap(v)
            return subdict
        elif isinstance(obj, SuperProxy):
            return obj.obj
        elif isinstance(obj, Pyro4.Proxy):
            uri = obj._pyroUri
            uri = str(uri)
            name, loc = uri.split('@')
            if not name.startswith('PYRO:'):
                raise RuntimeError("Proxy unwrapping can't recognize proxy")
            name = name[5:]
            obj = self.daemon.objectsById[name]
            if isinstance(obj, SuperProxy):
                return obj.obj
            else:
                return obj
        else:
            return obj
