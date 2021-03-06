"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from functools import wraps
from typing import Any, Callable
from sims4communitylib.exceptions.common_stacktrace_utils import CommonStacktraceUtil
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonExceptionHandler:
    """A class for catching and logging custom exceptions to a file on the system.

    """

    @staticmethod
    def log_exception(mod_name: str, exception_message: str, exception: Exception=None) -> bool:
        """log_exception(mod_name, exception_message, exception=None)

        Log an exception with a custom message

        :param mod_name: The name of the mod logging the exception.
        :type mod_name: str
        :param exception_message: The message to log alongside the exception.
        :type exception_message: str
        :param exception: The exception being logged.
        :type exception: Exception
        :return: True, if the message was successfully logged. False, if the message was not successfully logged.
        :rtype: bool
        """
        exceptions = CommonStacktraceUtil.get_full_stack_trace()
        stack_trace = '{}{} -> {}: {}\n'.format(''.join(exceptions), exception_message, type(exception).__name__, exception)
        from sims4communitylib.utils.common_log_registry import CommonLogUtils
        file_path = CommonLogUtils.get_exceptions_file_path(mod_name)
        result = CommonExceptionHandler._log_stacktrace(mod_name, stack_trace, file_path)
        if result:
            CommonExceptionHandler._notify_exception_occurred(file_path, mod_name=mod_name)
        return result

    @staticmethod
    def _log_stacktrace(mod_name: str, _traceback, file_path: str) -> bool:
        exception_traceback_text = '[{}] {} {}\n'.format(mod_name, CommonRealDateUtils.get_current_date_string(), _traceback)
        return CommonIOUtils.write_to_file(file_path, exception_traceback_text, ignore_errors=True)

    @staticmethod
    def catch_exceptions(mod_name: str, fallback_return: Any=None) -> Callable[..., Any]:
        """catch_exceptions(mod_name, fallback_return=None)

        A decorator for catching exceptions thrown by functions.

        Decorate functions with this decorator to catch and log exceptions

        :param mod_name: An identifier to indicate which mod it occurs in.
        :type mod_name: str
        :param fallback_return: A value to return upon an exception being caught.
        :type fallback_return: Any
        :return: A function wrapped to catch and log exceptions.
        :rtype: Callable[..., Any]
        """

        def _catch_exception(exception_function):
            @wraps(exception_function)
            def _wrapper(*args, **kwargs):
                try:
                    return exception_function(*args, **kwargs)
                except Exception as ex:
                    CommonExceptionHandler.log_exception(mod_name, 'Exception caught while invoking: {}'.format(exception_function.__name__), exception=ex)
                return fallback_return
            return _wrapper
        return _catch_exception

    @staticmethod
    def _notify_exception_occurred(file_path: str, mod_name: str=None):
        from ui.ui_dialog_notification import UiDialogNotification
        from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
        from sims4communitylib.enums.strings_enum import CommonStringId
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if not CommonZoneSpinEventDispatcher.get().game_loaded:
            return
        if mod_name is None or not mod_name:
            mod_name = ModInfo.get_identity().name
        basic_notification = CommonBasicNotification(
            CommonStringId.EXCEPTION_OCCURRED_TITLE_FOR_MOD,
            CommonStringId.EXCEPTION_OCCURRED_TEXT,
            title_tokens=(mod_name,),
            description_tokens=(file_path,),
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        basic_notification.show()
