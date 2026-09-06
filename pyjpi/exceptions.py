"""Exceptions raised by pyJPI."""


class JPIError(Exception):
    """Base exception for pyJPI errors."""


class JPIConnectionError(JPIError):
    """Raised when communication with a JPI device fails."""


class JPIResponseError(JPIError):
    """Raised when a JPI device returns an invalid response."""
