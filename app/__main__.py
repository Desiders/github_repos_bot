import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.types import (BotCommand, BotCommandScopeAllGroupChats,
                           BotCommandScopeAllPrivateChats)
from structlog import get_logger
from structlog.stdlib import BoundLogger

from app.config import load_config
from app.handlers import (register_introduction_handlers,
                          register_repositories_handlers)
from app.infrastructure.github import GitHub
from app.logging import logging_configure

logger: BoundLogger = get_logger()


async def main():
    logging_configure()
    logger.info("Logging is configured")

    config = load_config()
    logger.info("Configuration loaded")

    bot = Bot(
        token=config.bot.token,
        parse_mode=None,
        disable_web_page_preview=None,
    )

    dp = Dispatcher(
        bot=bot,
    )

    github = GitHub()

    await set_bot_commands(bot)
    logger.info("Bot commands are set")

    dp.setup_middleware(EnvironmentMiddleware(dict(
        github=github,
    )))
    logger.info("Middlewares are registered")

    register_introduction_handlers(dp)
    register_repositories_handlers(dp)
    logger.info("Handlers are registered")

    try:
        logger.warning("Bot starting!")
        await dp.start_polling(
            allowed_updates=[
                "message_handlers",
            ],
        )
    finally:
        logger.warning("Bot stopped!")

        bot_session = await bot.get_session()
        if bot_session is not None:
            logger.warning("Closing bot session")
            await bot_session.close()
        logger.warning("Bot session closed")

        await github.close()
        logger.warning("GitHub session cloased")

        logger.warning("Bye")


async def set_bot_commands(bot: Bot):
    cmd_help = BotCommand(
        command="help",
        description="Show menu",
    )
    cmd_source = BotCommand(
        command="source",
        description="Show source code",
    )

    public = [cmd_help]
    private = [cmd_help, cmd_source]

    await bot.set_my_commands(public, BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private, BotCommandScopeAllPrivateChats())


asyncio.run(main())
