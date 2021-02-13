import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.slash.get_cog_commands()

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
            description=f"Пинг сокета: {round(bot.latency * 1000)} мс",
            color=discord.Color.blurple()
        )
        embed.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
