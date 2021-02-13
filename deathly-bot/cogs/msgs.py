import discord
import discord_slash

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashCommandOptionType as types

import asyncio


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.slash.get_cog_commands()

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(
        name="скажи",
        options=[
            create_option(
                "сообщение",
                "Сообщение, которое надо сказать",
                types.STRING,
                False
            )
        ],
        guild_ids=[664609892400758784]
    )
    async def say(self, ctx, text: str = "я ебал меня сосали"):
        """
        Сказать что-нибудь
        """

        await ctx.ack(eat=True)

        embed = discord.Embed(
            title=discord.Embed.Empty,
            description=f"**{text}**",
            color=0x2F3136
        )

        async with ctx.channel.typing():
            await asyncio.sleep(3.0)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="отправить",
        options=[
            
        ],
        guild_ids=[664609892400758784]
    )
    async def send(self, ctx,
                   title = None,
                   description = None,
                   author = None,
                   author_icon = None,
                   thumbnail = None,
                   image = None,
                   footer = None,
                   footer_icon = None
    ):
        """
        Отправить настраиваемый эмбед
        """
        embed = discord.Embed()

        if title:
            embed.title = title
        else:
            embed.title = embed.Empty
    
        if description:
            embed.description = description
        else:
            embed.description = embed.Empty

        if author and not author_icon:
            embed.set_author(
                name=author
            )
        elif author and author_icon:
            embed.set_author(
                name=author,
                icon_url=f"{author_icon}"
            )
    
        if thumbnail:
            embed.set_thumbnail(
                url=f"{thumbnail}"
            )

        if image:
            embed.set_image(
                url=f"{image}"
            )

        if footer and not footer_icon:
            embed.set_footer(
                text=footer
            )
        elif footer and footer_icon:
            embed.set_footer(
                text=footer,
                icon_url=f"{footer_icon}"
            )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Messages(bot))
