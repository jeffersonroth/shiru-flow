"""Logging Utils."""

from typing import Optional

from settings import DEBUG_MODE_ON


def _traceback_exception(exc: Exception):
    """
    Traceback an Exception.

    Args
    ----
        exc (Exception): Exception.

    Returns
    -------
        None.
    """
    import traceback

    return traceback.print_exc()


def debug(
    message: Optional[str] = None,
    debug_mode_on: bool = bool(DEBUG_MODE_ON),
    stack: int = 0,
    exc: Optional[Exception] = None,
):
    """
    Write INFO LoggingMixin to logs if debug_mode_on.

    Args
    ----
        message (str): Message to log.
        debug_mode_on (bool): Debug mode on, if True writes to logs.
        stack (int): number of stack layers to print.
        exc (Optional[Exception]): Exception.

    Returns
    -------
        None.
    """
    from airflow.utils.log.logging_mixin import LoggingMixin

    try:
        import inspect

        if message and debug_mode_on:
            LoggingMixin().log.info(message)

            if stack > 0:
                LoggingMixin().log.info(
                    f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
                )

            if exc:
                _traceback_exception(exc)
        else:
            LoggingMixin().log.debug(message)

            if stack > 0:
                LoggingMixin().log.debug(
                    f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
                )

    except ValueError as e:
        _traceback_exception(exc=e)

    except Exception as e:
        _traceback_exception(exc=e)


def info(
    message: Optional[str] = None,
    stack: int = 0,
    exc: Optional[Exception] = None,
):
    """
    Write INFO LoggingMixin to logs.

    Args
    ----
        message (str): Message to log.
        stack (int): number of stack layers to print.
        exc (Optional[Exception]): Exception.

    Returns
    -------
        None.
    """
    from airflow.utils.log.logging_mixin import LoggingMixin

    try:
        import inspect

        if message:
            LoggingMixin().log.info(message)

        if stack > 0:
            LoggingMixin().log.info(
                f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
            )

        if exc:
            _traceback_exception(exc)

    except ValueError as e:
        _traceback_exception(exc=e)

    except Exception as e:
        _traceback_exception(exc=e)


def warning(
    message: Optional[str] = None,
    stack: int = 0,
    exc: Optional[Exception] = None,
):
    """
    Write WARNING LoggingMixin to logs.

    Args
    ----
        message (str): Message to log.
        stack (int): number of stack layers to print.
        exc (Optional[Exception]): Exception.

    Returns
    -------
        None.
    """
    from airflow.utils.log.logging_mixin import LoggingMixin

    try:
        import inspect

        if message:
            LoggingMixin().log.warning(message)
        if stack > 0:
            LoggingMixin().log.warning(
                f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
            )
        if exc:
            _traceback_exception(exc)

    except ValueError as e:
        _traceback_exception(exc=e)

    except Exception as e:
        _traceback_exception(exc=e)


def error(
    message: Optional[str] = None,
    stack: int = 0,
    exc: Optional[Exception] = None,
):
    """
    Write ERROR LoggingMixin to logs.

    Args
    ----
        message (str): Message to log.
        stack (int): number of stack layers to print.
        exc (Optional[Exception]): Exception.

    Returns
    -------
        None.
    """
    from airflow.utils.log.logging_mixin import LoggingMixin

    try:
        import inspect

        if message:
            LoggingMixin().log.error(message)

        if stack > 0:
            LoggingMixin().log.error(
                f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
            )

        if exc:
            _traceback_exception(exc)

    except ValueError as e:
        _traceback_exception(exc=e)

    except Exception as e:
        _traceback_exception(exc=e)


def critical(
    message: Optional[str] = None,
    stack: int = 0,
    exc: Optional[Exception] = None,
):
    """
    Write CRITICAL LoggingMixin to logs.

    Args
    ----
        message (str): Message to log.
        stack (int): number of stack layers to print.
        exc (Optional[Exception]): Exception.

    Returns
    -------
        None.
    """
    from airflow.utils.log.logging_mixin import LoggingMixin

    try:
        import inspect

        if message:
            LoggingMixin().log.critical(message)

        if stack > 0:
            LoggingMixin().log.critical(
                f"[Stack] {[inspect.stack()[n].function for n in range(1, stack)]}"
            )

        if exc:
            _traceback_exception(exc)

    except ValueError as e:
        _traceback_exception(exc=e)

    except Exception as e:
        _traceback_exception(exc=e)
