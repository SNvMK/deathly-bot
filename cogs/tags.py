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
        async with aiopg.create_pool(self.bot.db_url) as pool:
            async with pool.acquire() as conn:
                injection = f"""
                INSERT INTO tags (
                    author, 
                    name, 
                    response
                ) VALUES ($1, $2, $3)
                """

                await conn.execute(injection, ctx.author_id, name, response)
                await ctx.send("Тэг создан", hidden=True)


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
        async with aiopg.create_pool(self.bot.db_url) as pool:
            async with pool.acquire() as conn:
                tags = await conn.fetch("SELECT * FROM tags")

                for tag in tags:
                    tag_dict = dict(tag)

                    if tag_dict["name"] == name:
                        if reply_to:
                            msg = discord.utils.get(ctx.channel.history(limit=100).flatten(), id=reply_to)
                            await msg.reply(tag_dict["response"])
                            break
                        else:
                            await ctx.send(tag_dict["response"])
                            break


def setup(bot):
    bot.add_cog(Tags(bot))
