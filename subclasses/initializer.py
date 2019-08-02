'''
SHAMELESSLY STOLEN FROM https://stackoverflow.com/a/43946725
'''

###  StdLib  ###
from functools import wraps
import inspect
import json


###########################################################################################################################
#//////|   Decorator   |//////////////////////////////////////////////////////////////////////////////////////////////////#
###########################################################################################################################

def initializer(function):

    @wraps(function)
    def wrapped(self, *args, **kwargs):
        _assign_args(self, list(args), kwargs, function)
        function(self, *args, **kwargs)

    return wrapped


def represent(cls):
    def __repr__(self):
        data = self.__dict__
        for k in data:
            if isinstance(data[k], tuple):
                data[k] = data[k][0]
            if not isinstance( data[k], str):
                data[k] = str(data[k])
            try:
                data[k] = json.loads(data[k])
            except Exception:
                continue
        
        return json.dumps(data, indent=2)

    cls.__repr__ = __repr__
    return cls


def comparable(cls):
    """ Class decorator providing generic comparison functionality """

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    cls.__eq__ = __eq__
    cls.__ne__ = __ne__
    return cls


###########################################################################################################################
#//////|   Utils   |//////////////////////////////////////////////////////////////////////////////////////////////////////#
###########################################################################################################################

def _assign_args(instance, args, kwargs, function):

    def set_attribute(instance, parameter, default_arg):
        if not(parameter.startswith("_")):
            setattr(instance, parameter, default_arg)

    def assign_keyword_defaults(parameters, defaults):
        for parameter, default_arg in zip(reversed(parameters), reversed(defaults)):
            set_attribute(instance, parameter, default_arg)

    def assign_positional_args(parameters, args):
        for parameter, arg in zip(parameters, args.copy()):
            set_attribute(instance, parameter, arg)
            args.remove(arg)

    def assign_keyword_args(kwargs):
        for parameter, arg in kwargs.items():
            set_attribute(instance, parameter, arg)

    def assign_keyword_only_defaults(defaults):
        return assign_keyword_args(defaults)

    def assign_variable_args(parameter, args):
        set_attribute(instance, parameter, args)

    POSITIONAL_PARAMS, VARIABLE_PARAM, _, KEYWORD_DEFAULTS, _, KEYWORD_ONLY_DEFAULTS, _ = inspect.getfullargspec(
        function)
    POSITIONAL_PARAMS = POSITIONAL_PARAMS[1:]  # remove 'self'

    if(KEYWORD_DEFAULTS):
        assign_keyword_defaults(
            parameters=POSITIONAL_PARAMS,  defaults=KEYWORD_DEFAULTS)
    if(KEYWORD_ONLY_DEFAULTS):
        assign_keyword_only_defaults(defaults=KEYWORD_ONLY_DEFAULTS)
    if(args):
        assign_positional_args(parameters=POSITIONAL_PARAMS,  args=args)
    if(kwargs):
        assign_keyword_args(kwargs=kwargs)
    if(VARIABLE_PARAM):
        assign_variable_args(parameter=VARIABLE_PARAM,      args=args)
