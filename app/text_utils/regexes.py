import re

KEYWOARDS_REGEX = re.compile(r"(\S*) *: *(\S*)")


def get_keywoards(query: str) -> dict[str, str]:
    """
    Get the keywoards from a query

    :query: The query to parse.

    :examples:
    >>> get_keywords("keyword: value")
    {'keyword': 'value'}
    >>> get_keywords("keyword:value")
    {'keyword': 'value'}
    >>> get_keywords("keyword :value")
    {'keyword': 'value'}
    >>> get_keywords("keyword : value")
    {'keyword': 'value'}
    >>> get_keywords("keyword1:value1 keyword2:value2")
    {'keyword1': 'value1', 'keyword2': 'value2'}
    """
    return {
        keyword: value
        for keyword, value in KEYWOARDS_REGEX.findall(query)
        if keyword and value
    }


def get_text(query: str) -> str:
    """
    Get the text from a query.

    :query: The query to parse.

    :examples:
    >>> get_text("keyword: value")
    ""
    >>> get_text("text keyword:value")
    "text"
    >>> get_text("text1 keyword:value text2")
    "text1 text2"
    """
    return KEYWOARDS_REGEX.sub("", query).strip()
