from typing import Any, Callable

from app.infrastructure.github.schemas import Repository


def cut_description(description: str, max_length: int) -> str:
    """
    Cut the description to a maximum length

    :description: The description to cut.
    :max_length: The maximum length of the description.

    :examples:
    >>> cut_description("Hello world!", 10)
    "Hello world..."
    >>> cut_description("Hello world! This is a long description.", 10)
    "Hello world..."
    >>> cut_description("Bye! This is a long description.", 10)
    "Bye..."
    >>> cut_description("Bye! Hi! This is a long description.", 10)
    "Bye! Hi..."
    """
    if len(description) > max_length:
        description = description[:max_length + 1]
        string = description[::-1]
        for symbol in (".", "!", "?"):
            try:
                index = string.index(symbol)
            except ValueError:
                continue
            else:
                return description[:-index - 1] + "..."
    return description


def repository_to_text(
    repository: Repository,
    quoter: Callable[[Any], str],
) -> str:
    """
    Convert a repository to a text.

    :repository: The repository to convert.
    """
    owner = repository.owner
    owner_html_url = owner.html_url
    owner_login = owner.login
    licence = repository.license
    licence_url = licence.url if licence else None
    licence_name = licence.name if licence else None

    return (
        "<a href='{html_url}'>{name}</a>\n"
        "Language: <b>{language}</b>\n"
        "Owner: <a href='{owner_html_url}'>{owner_login}</a>\n"
        "Stars: <b>{stargazers_count}</b>\n"
        "Forks: <b>{forks_count}</b>\n"
        "License: <a href='{licence_url}'><i>{licence_name}</i></a>\n"
        "Description: <i>{description}</i>\n\n"
    ).format(
        html_url=quoter(repository.html_url),
        name=quoter(repository.name),
        language=quoter(repository.language),
        owner_html_url=quoter(owner_html_url),
        owner_login=quoter(owner_login),
        stargazers_count=quoter(repository.stargazers_count),
        forks_count=quoter(repository.forks_count),
        licence_url=quoter(licence_url),
        licence_name=quoter(licence_name),
        description=quoter(repository.description),
    )


def repositories_to_text(
    repositories: list[Repository],
    max_description_length: int,
    quoter: Callable[[Any], str],
) -> str:
    """
    Convert repositories to a text.

    :repositories: The repositories to convert.
    :max_description_length: The maximum length of the description.
    :quoter: The function to quote the text.
    """
    text = ""
    for repository in repositories:
        if description := repository.description:
            repository.description = cut_description(
                description, max_description_length,
            )
        repository_text = repository_to_text(repository, quoter)

        if len(text) + len(repository_text) > 4096:
            break
        else:
            text += repository_text
    return text
