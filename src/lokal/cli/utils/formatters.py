"""Output formatters."""

try:
    from colorama import Fore, Style
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        GREEN = RED = CYAN = YELLOW = ""
    class Style:
        RESET_ALL = ""


def format_success(message: str) -> str:
    """Format success message."""
    if HAS_COLORAMA:
        return f"{Fore.GREEN}{message}{Style.RESET_ALL}"
    return message


def format_error(message: str) -> str:
    """Format error message."""
    if HAS_COLORAMA:
        return f"{Fore.RED}{message}{Style.RESET_ALL}"
    return message


def format_info(message: str) -> str:
    """Format info message."""
    if HAS_COLORAMA:
        return f"{Fore.CYAN}{message}{Style.RESET_ALL}"
    return message


def format_warning(message: str) -> str:
    """Format warning message."""
    if HAS_COLORAMA:
        return f"{Fore.YELLOW}{message}{Style.RESET_ALL}"
    return message
