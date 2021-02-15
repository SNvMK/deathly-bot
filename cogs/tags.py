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
                tags = await conn.fetch("SELECT * FROM tags")
                print("fetched")
                for tag in tags:
                    tag_dict = dict(tag)
                    print("dict")
                    if tag["name"] == name:
                        await ctx.send("Тэг уже существует!", hidden=True)
                        print("exists")
                        break

                    else:
                        injection = f"""
                        INSERT INTO tags (
                            author, 
                            name, 
                            response
                        ) VALUES ($1, $2, $3)
                        """
                        print("injection")

                        await conn.execute(injection, ctx.author_id, name, response)
                        print("exec")
                        await ctx.send("Тэг создан", hidden=True)
                        print("send")


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
