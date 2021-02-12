import discord
import discord_slash
import jishaku

from discord.ext import commands

import asyncio
import typing
from os import getenv


TOKEN = getenv("TOKEN")

bot = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.competing, name="cum зоне"),
    status=discord.Status.idle,
    owner_id=487845696100368384
)
bot.remove_command("help")
slash = discord_slash.SlashCommand(
    bot,
    sync_commands=True
)

@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    print(f"Запущен бот {str(bot.user)}")

@slash.slash(guild_ids=[664609892400758784])
async def пинг(ctx):
    """
    Понг!
    """

    await ctx.ack()

    embed = discord.Embed(
        title=f"Понг! Пинг сокета: {round(bot.latency * 1000)} мс",
        color=discord.Color.blurple()
    )
    embed.set_author(
        name=ctx.author,
        icon_url=ctx.author.avatar_url
    )

    await ctx.send(embed=embed)

@slash.slash(
    guild_ids=[664609892400758784],
    connector={
        "текст": "text"
    }
)
async def скажи(ctx, text: str):
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

@slash.slash(
    guild_ids=[664609892400758784],
    connector={
        "заголовок": "title",
        "описание": "description",
        "автор": "author",
        "аватар": "author_icon",
        "иконка": "thumbnail",
        "изображение": "image",
        "футер": "footer",
        "иконка_футера": "footer_icon"
    }
)
async def отправить(ctx,
                    title: str = None,
                    description: str = None,
                    author: str = None,
                    author_icon: str = None,
                    thumbnail: str = None,
                    image: str = None,
                    footer: str = None,
                    footer_icon: str = None
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

if __name__ == "__main__":
    bot.run(TOKEN)
