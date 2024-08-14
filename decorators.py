import functools
import logging

logging.basicConfig(level=logging.DEBUG)


def logger_exception_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr, kwargs_repr)
        # logging.basicConfig(level=logging.DEBUG)
        # logging.info(f"{func.__name__}. {[]*args}, {[]**kwargs}")
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper
