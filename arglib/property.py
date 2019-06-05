import logging
from functools import wraps
from inspect import signature

def add_properties(*names):

    def decorator(cls):
        for name in names:
            setattr(cls, name, property(lambda self, name=name: getattr(self, f'_{name}'))) # NOTE The keyword is necessary.
        return cls

    return decorator

def set_properties(*names, **values):

    def decorator(self):
        for name in names:
            setattr(self, f'_{name}', values[name])

        return self
        
    return decorator

def has_properties(*names):

    def decorator(cls):
        cls = add_properties(*names)(cls)
        old_init = cls.__init__

        @wraps(old_init)
        def new_init(self, *args, **kwargs):

            func_sig = signature(old_init)
            bound = func_sig.bind(self, *args, **kwargs)
            bound.apply_defaults()
            all_args = bound.arguments
            self = set_properties(*names, **all_args)(self)
            old_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    return decorator