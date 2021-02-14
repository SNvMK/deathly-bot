import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext

import asyncpg as aiopg

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands()

    @cog_ext.cog_subcommand(
        base="тэги",
        name="добавить",
        base_desc="Управление тэгами",
        description="Добавить тэг",
        connector={
            "имя": "name",
            "ответ": "response"
        },
        guild_ids=[664609892400758784]
    )
    async def add_tag(self, ctx,
                      name: str,
                      response: str
    ):
        ...

    @cog_ext.cog_subcommand(
        base="тэги",
        name="найти",
        base_desc="Управление тэгами",
        description="Найти тэг",
        connector={
            "имя": "name",
            "ответить-на": "reply_to"
        },
        guild_ids=[664609892400758784]
    )
    async def search_tag(self, ctx,
                         name: str,
                         reply_to: int = None
    ):
        ...


def setup(bot):
    bot.add_cog(Tags(bot))
