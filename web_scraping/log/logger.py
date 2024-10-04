import logging

from typing import Callable

from web_scraping.log.handlers import (
    CustomStreamHandler,
    LogDBHandler,
    LogSlackHandler,
)


class ScrapeLogger(logging.getLoggerClass()):
    """Custom logger class for scraping operations.

    This class is responsible for dispatching the log messages to specified destinations:
    Database, Console and Slack channel. Each destination is handled by appropriate handler object.

    By default, messages will be sent to different places, depending on the severity level:

        DEBUG(10) - only to the console (without severity level);
        INFO(20) - to the console (with severity level) and to the Slack channel (without severity level);
        WARNING(30) - to the console and to the Slack channel;
        ERROR(40) - to the console, to the Slack channel and to the Database;
        CRITICAL(50) - to the console, to the Slack channel and to the Database;

    But it could be changed in the calling function by turning ON/OFF the corresponding flags.

    Args:
        name (str): The name of the logger.
        level (int): The logging level for the logger.

    """

    def __init__(self, name: str, level: int = logging.NOTSET):
        """Initialize the ScrapeLogger instance."""
        super().__init__(name, level)
        # Specifies the lowest-severity log message a logger will handle
        self.setLevel(logging.DEBUG)

        # Create Database handler, Slack handler and Console handler
        self._database_handler = LogDBHandler()
        self._slack_handler = LogSlackHandler()
        self._stdout_handler = CustomStreamHandler()

        # Add handlers
        self.addHandler(self._database_handler)
        self.addHandler(self._slack_handler)
        self.addHandler(self._stdout_handler)

        # Set formatter
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        self._slack_handler.setFormatter(formatter)
        self._stdout_handler.setFormatter(formatter)

        # Flags
        self._send_to_slack = True
        self._save_to_database = True
        self._print_to_console = True

    def disable_console_output(self):
        """Disable console output for logging."""
        self._print_to_console = False
        self.removeHandler(self._stdout_handler)

    def enable_console_output(self):
        """Enable console output for logging."""
        self._print_to_console = True
        self.addHandler(self._stdout_handler)

    def disable_database_output(self):
        """Disable database output for logging."""
        self._save_to_database = False
        self.removeHandler(self._database_handler)

    def enable_database_output(self):
        """Enable database output for logging."""
        self._save_to_database = True
        self.addHandler(self._database_handler)

    def disable_slack_output(self):
        """Disable Slack output for logging."""
        self._send_to_slack = False
        self.removeHandler(self._slack_handler)

    def enable_slack_output(self):
        """Enable Slack output for logging."""
        self._send_to_slack = True
        self.addHandler(self._slack_handler)

    def debug(self, msg: str, console: bool = True, slack: bool = False, store: bool = False, *args, **kwargs):
        """
        Log a DEBUG-level message.
        By default, message will be sent to the console.

        Args:
            msg (str): The log message.
            console (bool): Whether to output the message to the console. Default is True.
            slack (bool): Whether to output the message to the Slack channel. Default is False.
            store (bool): Whether to save the message to the Database. Default is False.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.__msg_impl(super().debug, msg, console, slack, store, *args, **kwargs)

    def info(self, msg: str, console: bool = True, slack: bool = True, store: bool = False, *args, **kwargs):
        """
        Log a INFO-level message.
        By default, message will be sent to the console and to the Slack channel.

        Args:
            msg (str): The log message.
            console (bool): Whether to output the message to the console. Default is True.
            slack (bool): Whether to output the message to the Slack channel. Default is True.
            store (bool): Whether to save the message to the Database. Default is False.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.__msg_impl(super().info, msg, console, slack, store, *args, **kwargs)

    def warning(self, msg: str, console: bool = True, slack: bool = True, store: bool = False, *args, **kwargs):
        """
        Log a WARNING-level message.
        By default, message will be sent to the console and to the Slack channel.

        Args:
            msg (str): The log message.
            console (bool): Whether to output the message to the console. Default is True.
            slack (bool): Whether to output the message to the Slack channel. Default is True.
            store (bool): Whether to save the message to the Database. Default is False.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.__msg_impl(super().warning, msg, console, slack, store, *args, **kwargs)

    def error(self, msg: str, console: bool = True, slack: bool = True, store: bool = True, *args, **kwargs):
        """
        Log a ERROR-level message.
        By default, message will be sent to the console, to the Slack channel and to the Database.

        Args:
            msg (str): The log message.
            console (bool): Whether to output the message to the console. Default is True.
            slack (bool): Whether to output the message to the Slack channel. Default is True.
            store (bool): Whether to save the message to the Database. Default is True.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.__msg_impl(super().error, msg, console, slack, store, *args, **kwargs)

    def critical(self, msg: str, console: bool = True, slack: bool = True, store: bool = True, *args, **kwargs):
        """
        Log a CRITICAL-level message.
        By default, message will be sent to the console, to the Slack channel and to the Database.

        Args:
            msg (str): The log message.
            console (bool): Whether to output the message to the console. Default is True.
            slack (bool): Whether to output the message to the Slack channel. Default is True.
            store (bool): Whether to save the message to the Database. Default is True.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.__msg_impl(super().critical, msg, console, slack, store, *args, **kwargs)

    def __msg_impl(self, func: Callable, msg: str, console: bool, slack: bool, store: bool, *args, **kwargs):
        """
        Helper method for logging DEBUG through CRITICAL messages
        by calling the appropriate `func()` from the base class.

        Args:
            func (Callable): The logging function to call.
            msg (str): The log message.
            console (bool): Whether to output the message to the console.
            slack (bool): Whether to output the message to the Slack channel.
            store (bool): Whether to save the message to the Database.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        # Checking flags
        if self._print_to_console and not console:
            self.removeHandler(self._stdout_handler)
        if self._save_to_database and not store:
            self.removeHandler(self._database_handler)
        if self._send_to_slack and not slack:
            self.removeHandler(self._slack_handler)

        # Log
        func(msg, *args, **kwargs)

        # Enable if needed
        if self._print_to_console and not console:
            self.addHandler(self._stdout_handler)
        if self._save_to_database and not store:
            self.addHandler(self._database_handler)
        if self._send_to_slack and not slack:
            self.addHandler(self._slack_handler)
