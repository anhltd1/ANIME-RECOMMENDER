"""Custom application exception with traceback context in the message.

Use when re-wrapping a low-level ``Exception`` with a stable, readable string that still
points to the original failure site (file and line) via ``sys.exc_info()`` while handling
the exception.
"""

from __future__ import annotations

import sys


class CustomException(Exception):
    """
    Exception whose string form combines a custom *message* with optional *error_details*
    plus filename and line number from the current exception traceback (if any).
    """

    def __init__(self, message: str, error_details: Exception | None = None):
        # Build the full text once; ``Exception`` stores it via ``super().__init__``.
        self.error_message = self.get_detail_error_message(
            message=message, error_details=error_details
        )
        super().__init__(self.error_message)

    @staticmethod
    def get_detail_error_message(message: str, error_details: Exception | None) -> str:
        # ``sys.exc_info()`` is only reliable while handling an exception; callers should
        # construct ``CustomException`` from inside an ``except`` block when possible.
        _, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "unknown"
            line_number = "unknown"

        details = repr(error_details) if error_details is not None else "none"
        return (
            f"{message} | Error: {details} | "
            f"Filename: {file_name} | Line Number: {line_number}"
        )

    def __str__(self) -> str:
        return self.error_message
