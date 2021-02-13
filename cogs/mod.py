import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @commands.has_permissions(manage_messages=True)
    @cog_ext.cog_slash(
        name="очистить",
        connector={
            "количетсво": "ampount"
        },
        guild_ids=[664609892400758784]
    )
    async def purge(self, ctx, amount: int):
        """
        Очистить сообщения
        """

        await ctx.ack(eat=True)

        purge = await ctx.channel.purge(limit=amount)

        await ctx.send(f"Сообщений очищено: [{len(purge)}](https://snvmk.tk/)", delete_after=3.0)


def setup(bot):
    bot.add_cog(Moderation(bot))
