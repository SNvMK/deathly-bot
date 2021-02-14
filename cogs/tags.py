import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext

import aiopg

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
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM tags;")
                    for tag in cur:
                        if tag[2] == name:
                            await ctx.send(f"Тэг {name} уже существует!", hidden=True)
                            break
                        else:
                            injection = """
                            INSERT INTO tags (
                                author, 
                                name, 
                                response
                            ) VALUES (%s, %s, %s);
                            """
                            await cur.execute(injection, (ctx.author_id, name, response))
                            await ctx.send(f"Создан тэг {name}!", hidden=True)
                            break

    @cog_ext.cog_subcommand(
        base="тэги",
        name="найти",
        base_desc="Управление тэгами",
        description="Найти тэг",
        connector={
            "имя": "name"
        },
        guild_ids=[664609892400758784]
    )
    async def search_tag(self, ctx,
                      name: str
    ):
        async with aiopg.create_pool(self.bot.db_url) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM tags;")
                    async for row in cur:
                        if row[1] == name:
                            await ctx.send(row[2])
                            break


def setup(bot):
    bot.add_cog(Tags(bot))
