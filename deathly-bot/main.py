import discord
import discord_slash
import jishaku

from discord.ext import commands

from os import getenv


TOKEN = getenv("TOKEN")

bot = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.competing, name="cum зоне"),
    status=discord.Status.idle,
    owner_id=487845696100368384
)


slash = discord_slash.SlashCommand(
    bot,
    sync_commands=True
)

@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    print(f"Запущен бот {str(bot.user)}")

@slash.slash(guild_ids=[guild.id for guild in bot.guilds])
async def пинг(ctx):
    """
    Понг!
    """

    embed = discord.Embed(
        title=f"Понг! Пинг сокета: {round(bot.latency) * 1000} мс",
        color=discord.Color.blurple()
    )
    embed.set_author(
        name=ctx.author,
        icon_url=ctx.author.avatar_url
    )

    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)
