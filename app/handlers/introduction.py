from aiogram import Dispatcher, md
from aiogram.types import Message
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def start_cmd(m: Message):
    await m.answer(
        "Hello, {first_name}!\n\n"
        "I'm helps you find the repositories!\n\n"
        "{search_pattern}\n"
        "args (main, other see by link):\n"
        "\t- <b>user:&lt;username&gt;</b>\n"
        "\t- <b>language:&lt;language&gt;</b>\n"
        "\t- <b>order:asc|desc</b>\n"
        "\t- <b>sort:stars|forks|updated</b>\n"
        "\t- <b>&lt;text&gt; in:name|description|topics|readme</b>\n"
        "\t- <b>forks|stars|followers|size|topics:lt;condition&gt;</b>\n\n"
        "Examples:\n"
        "1. <code>get_anime_bot user:Desiders</code>\n"
        "2. <code>anime sort:stars order:desc language:Python</code>\n"
        "3. <code>sort:stars order:desc language:Rust</code>\n"
        "4. <code>fast in:description</code>\n"
        "5. <code>popular in:description order:asc sort:stars</code>\n"
        "6. <code>language:Rust "
        "stars:1000..2000 forks:&lt;=100 order:desc sort:forks</code>\n"
        "7. <code>python baby</code>"
        .format(
            first_name=md.quote_html(m.from_user.first_name),
            search_pattern=md.hlink(
                title="Search pattern",
                url=(
                    "https://docs.github.com/en/search-github/"
                    "searching-on-github/searching-for-repositories"
                ),
            ),
        ),
        parse_mode="HTML",
        disable_web_page_preview=False,
        disable_notification=False,
    )


async def source_cmd(m: Message):
    await m.answer(
        text=(
            "Bot has open source code!\n\n"
            "Source: {link}"
        ).format(
            link=(
                "https://github.com/Desiders/"
                "github_repos_bot"
            ),
        ),
    )


def register_introduction_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_cmd,
        commands={"start", "help"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        source_cmd,
        commands={"source"},
        content_types={"text"},
        state="*",
    )
