from contextlib import suppress

from aiogram import Dispatcher, md
from aiogram.types import (InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent, Message)
from aiohttp import ClientError
from app.filters import HasText
from app.infrastructure.github import GitHub
from app.text_utils.formatting import (cut_description, repositories_to_text,
                                       repository_to_text)
from app.text_utils.regexes import get_keywoards, get_text
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def search_repositories_cmd(m: Message, github: GitHub):
    query = m.text
    if len(query) > 256:
        await m.answer(
            "Query is too long. Max length is 256 symbols :(",
            parse_mode=None,
            disable_web_page_preview=False,
            disable_notification=False,
        )
        return

    wait_m = await m.answer(
        "Searching repositories...",
        parse_mode=None,
        disable_web_page_preview=True,
        disable_notification=True,
    )

    text, keywords = get_text(query), get_keywoards(query)
    try:
        repositories = await github.search_repositories(text, **keywords)
    except ClientError as e:
        logger.warning(
            "Failed to search repositories",
            error=e, query=query,
            text=text, keywords=keywords,
        )
        await wait_m.edit_text(
            "Failed to search repositories :(",
            parse_mode=None,
            disable_web_page_preview=True,
        )
        return
    else:
        repositories_len = len(repositories)

    if repositories_len == 0:
        logger.info(
            "No repositories found",
            query=query, text=text,
            keywords=keywords,
            repositories=repositories,
        )
        await wait_m.edit_text(
            "No repositories found :(",
            parse_mode=None,
            disable_web_page_preview=True,
        )
        return

    text = repositories_to_text(
        repositories,
        max_description_length=200,
        quoter=md.quote_html,
    )

    await wait_m.delete()
    await m.reply(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=repositories_len > 1,
        disable_notification=False,
    )


async def search_repositories_query(q: InlineQuery, github: GitHub):
    query = q.query
    if len(query) > 256:
        await q.answer(
            results=[
                InlineQueryResultArticle(
                    id="query_too_long",
                    title="Query is too long. Max length is 256 symbols :(",
                    input_message_content=InputTextMessageContent(
                        "Query is too long. Max length is 256 symbols :(",
                        parse_mode=None,
                        disable_web_page_preview=True,
                    ),
                ),
            ],
            cache_time=86400,
            is_personal=False,
        )
        return
    logger.info(
        "Searching repositories",
        query_len=len(query),
        query=query,
    )

    text, keywords = get_text(query), get_keywoards(query)
    try:
        repositories = await github.search_repositories(text, **keywords)
    except ClientError as e:
        logger.warning(
            "Failed to search repositories",
            query=query, text=text,
            keywords=keywords,
            error=e,
        )
        await q.answer(
            results=[
                InlineQueryResultArticle(
                    id="failed_to_search_repositories",
                    title="Failed to search repositories :(",
                    input_message_content=InputTextMessageContent(
                        "Failed to search repositories :(",
                        parse_mode=None,
                        disable_web_page_preview=True,
                    ),
                ),
            ],
            cache_time=300,
            is_personal=False,
        )
        return
    else:
        repositories_len = len(repositories)

    if repositories_len == 0:
        logger.info(
            "No repositories found",
            query=query, text=text,
            keywords=keywords,
            repositories=repositories,
        )
        await q.answer(
            results=[
                InlineQueryResultArticle(
                    id="no_repositories_found",
                    title="No repositories found :(",
                    input_message_content=InputTextMessageContent(
                        "No repositories found :(",
                        parse_mode=None,
                        disable_web_page_preview=True,
                    ),
                ),
            ],
            cache_time=60,
            is_personal=False,
        )
        return

    results = []
    with suppress(StopIteration):
        for index, repository in enumerate(repositories, start=1):
            if description := repository.description:
                repository.description = cut_description(
                    description, max_length=200,
                )

            results.append(
                InlineQueryResultArticle(
                    id=repository.id,
                    title=repository.full_name,
                    input_message_content=InputTextMessageContent(
                        repository_to_text(
                            repository,
                            quoter=md.quote_html,
                        ),
                        parse_mode="HTML",
                        disable_web_page_preview=False,
                    ),
                    description=repository.description,
                    thumb_url=repository.owner.avatar_url,
                )
            )
            if index >= 50:
                break

    await q.answer(
        results,
        cache_time=60,
        is_personal=False,
    )


def register_repositories_handlers(dp: Dispatcher):
    dp.register_message_handler(
        search_repositories_cmd,
        HasText(True),
        chat_type="private",
        state="*",
    )
    dp.register_inline_handler(
        search_repositories_query,
        HasText(True),
        state="*",
    )
