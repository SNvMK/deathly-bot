import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext

import asyncio


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(
        name="пинг",
        guild_ids=[664609892400758784]
    )
    async def ping(self, ctx):
        """
        Понг!
        """

        await ctx.ack()

        embed = discord.Embed(
            title=f"Понг!",
            description=f"Пинг сокета: {round(self.bot.latency * 1000)} мс",
            color=self.bot.embed_color
        )
        embed.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)

    async def spam(self, ctx, text, interval):
        await ctx.ack(eat=True)
        while True:
            await ctx.send(text)
            await asyncio.sleep(interval)
    
    @cog_ext.cog_slash(
        name="спам",
        guild_ids=[664609892400758784]
    )
    async def spam_cmd(self, ctx,
                       текст: str = "ATTACK",
                       интервал: int = 3
    ):
        self.bot.loop.create_task(self.spam(ctx, текст, интервал), name="SPAM")

    @cog_ext.cog_slash(
        name="стоп-спам",
        guild_ids=[664609892400758784]
    )
    async def stop_spam(self, ctx):
        for task in asyncio.all_tasks(loop=self.bot.loop):
            if task.get_name() == "SPAM":
                task.cancel()


def setup(bot):
    bot.add_cog(Misc(bot))
