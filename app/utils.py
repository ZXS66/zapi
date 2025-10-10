def isNoneOrEmptyStr(txt: str | None) -> bool:
    """Check if the given string is None or empty.

    Args:
        txt (str | None): The string to check.

    Returns:
        bool: True if the string is None or empty, False otherwise.
    """
    return txt is None or txt == ""
