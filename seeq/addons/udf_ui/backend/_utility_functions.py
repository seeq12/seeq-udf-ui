from typing import Callable
from functools import wraps
import threading
import re
from enum import Enum


def return_func_if_callable(fn, template_name):
    if isinstance(fn, Callable):
        return fn
    else:
        raise NotImplementedError(f'One or more call-back functions are not implemented for \'{template_name}\' or '
                                  f'{fn} is not a callable')


def debounce_with_timer(wait_time=0.3):
    def debounce(orig_func):
        @wraps(orig_func)
        def wrapper(*args, **kwargs):
            thread = threading.Timer(interval=wait_time, function=orig_func, args=args, kwargs=kwargs)
            thread.start()

        return wrapper

    return debounce


def formula_parser(formula):
    split = re.split(r'(\$\w*)', formula)
    ignore_vars = [v for n, v in enumerate(split) if '$' in v and "=" in split[n + 1]]
    variables = [v.replace('$', '') for n, v in enumerate(split) if '$' in v if v not in ignore_vars]
    unique_params = [i for n, i in enumerate(variables) if i not in variables[:n]]

    parsed_params_and_types = [{'name': name, 'type': 'Signal'} for name in unique_params]

    return parsed_params_and_types


class MessageType(Enum):
    INFORMATION = 1
    ERROR = 2
    SUCCESS = 3

