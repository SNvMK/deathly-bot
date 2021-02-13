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
        connector={"количетсво": "amount"},
        guild_ids=[664609892400758784]
    )
    async def purge(self, ctx, amount: int = 10):
        """
        Очистить сообщения
        """

        await ctx.ack(eat=True)

        purge = await ctx.channel.purge(limit=amount)

        await ctx.send(f"Сообщений очищено: [{len(purge)}](https://snvmk.tk/)", delete_after=3.0)

    @commands.has_permissions(kick_members=True)
    @cog_ext.cog_slash(
        name="кик",
        connector={
            "юзер": "user",
            "причина": "reason"
        },
        guild_ids=[664609892400758784]
    )
    async def kick(self, ctx, 
                   user: discord.Member, 
                   reason: str = "сосал хуи"
    ):
        """
        Кикнуть участника
        """

        await ctx.ack(eat=True)

        await user.kick(reason=reason)

        embed = discord.Embed(
            title="Кикнут участник",
            description=f"Был кикнут {str(user)}, потому что *{reason}*",
            color=self.bot.embed_color
        )

        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @cog_ext.cog_slash(
        name="бан",
        connector={
            "юзер": "user",
            "причина": "reason"
        },
        guild_ids=[664609892400758784]
    )
    async def ban(self, ctx, 
                  user: discord.Member, 
                  reason: str = "сосал хуи"
    ):
        """
        Забанить участника
        """

        await ctx.ack(eat=True)

        await user.ban(reason=reason)

        embed = discord.Embed(
            title="Забанен участник",
            description=f"Был забанен {str(user)}, потому что *{reason}*",
            color=self.bot.embed_color
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
