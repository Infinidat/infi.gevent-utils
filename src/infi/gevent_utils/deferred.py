import sys
import gevent


__PY3 = sys.version_info[0] == 3


def _py3_raise_value(result):
    return result[0](result[1]).with_traceback(result[2])


def _py2_raise_value(result):
    return result[0], result[1], result[2]

if __PY3:
    _to_raise_value = _py3_raise_value
else:
    _to_raise_value = _py2_raise_value


def create_threadpool_executed_func(original_func):
    """
    Returns a function wrapper that defers function calls execute inside gevent's threadpool but keeps any exception
    or backtrace in the caller's context.
    :param original_func: function to wrap
    :returns: wrapper function
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = original_func(*args, **kwargs)
            return True, result
        except:
            return False, sys.exc_info()

    def new_func(*args, **kwargs):
        status, result = gevent.get_hub().threadpool.apply(wrapped_func, args, kwargs)
        if status:
            return result
        else:
            raise(_to_raise_value(result))
    new_func.__name__ = original_func.__name__
    new_func.__doc__ = "(gevent-friendly)" + (" " + original_func.__doc__ if original_func.__doc__ is not None else "")
    return new_func
