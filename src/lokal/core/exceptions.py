"""Custom exceptions for lokal project generator."""


class LokalException(Exception):
    """Base exception for lokal."""

    pass


class TemplateError(LokalException):
    """Template-related error."""

    pass


class TemplateNotFound(TemplateError):
    """Template not found."""

    pass


class InvalidTemplate(TemplateError):
    """Invalid template structure."""

    pass


class ConfigError(LokalException):
    """Configuration error."""

    pass


class HookExecutionError(LokalException):
    """Hook execution failed."""

    pass


class RemoteTemplateError(LokalException):
    """Remote template error."""

    pass
