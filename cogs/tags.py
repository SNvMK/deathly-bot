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
                tags = conn.fetch("SELECT * FROM tags")

                for tag in tags:
                    tag_dict = dict(tag)

                    if name in list(tag_dict.values()):
                        await ctx.send("Тэг уже существует", hidden=True)
                        break
                    else:
                        injection = f"""
                        INSERT INTO tags (
                            author, 
                            name, 
                            response
                        ) VALUES ($1, $2, $3)
                        """

                        await conn.execute(injection, ctx.author_id, name, response)
                        await ctx.send("Тэг создан", hidden=True)
                        break


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
                            msg = await ctx.channel.fetch_message(reply_to)
                            await msg.reply(tag_dict["response"])
                            break
                        else:
                            await ctx.send(tag_dict["response"])
                            break
                    else:
                        await ctx.send("Тэг не существует", hidden=True)
                        break

    @cog_ext.cog_subcommand(
        base="тэги",
        name="удалить",
        base_desc="Управление тэгами",
        description="Удалить тэг",
        connector={
            "имя": "name"
        },
        guild_ids=[664609892400758784]
    )
    async def delete_tag(self, ctx,
                         name: str
    ):
        async with aiopg.create_pool(self.bot.db_url) as pool:
            async with pool.acquire() as conn:
                tags = await conn.fetch("SELECT * FROM tags")

                for tag in tags:
                    tag_dict = dict(tag)

                    if tag_dict["name"] == name:
                        if tag["author"] == ctx.author_id:
                            await conn.execute(f"DELETE FROM tags WHERE name = {name}")
                            await ctx.send("Тэг удалён", hidden=True)
                            break
                        else:
                            await ctx.send("Вы не автор этого тэга", hidden=True)
                            break
                    else:
                        await ctx.send("Тэг не существует", hidden=True)
                        break

    @cog_ext.cog_subcommand(
        base="тэги",
        name="инфо",
        base_desc="Управление тэгами",
        description="Инфо о тэге",
        connector={
            "имя": "name"
        },
        guild_ids=[664609892400758784]
    )
    async def tag_info(self, ctx,
                       name: str
    ):
        async with aiopg.create_pool(self.bot.db_url) as pool:
            async with pool.acquire() as conn:
                tags = await conn.fetch("SELECT * FROM tags")

                for tag in tags:
                    tag_dict = dict(tag)

                    if tag_dict["name"] == name:
                        embed = discord.Embed(
                            title=f"Тэг `{name}`",
                            description=f"Автор: {ctx.guild.fetch_member(tag_dict['author']).mention}"
                        )
                        await ctx.send(embed=embed)
                        break
                    else:
                        await ctx.send("Тэг не существует", hidden=True)
                        break


def setup(bot):
    bot.add_cog(Tags(bot))
