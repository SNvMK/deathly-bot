import discord
import discord_slash
import jishaku

from discord.ext import commands
from discord import MissingPermissions

from os import getenv, listdir


TOKEN = getenv("TOKEN")

bot = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.competing, name="cum зоне"),
    status=discord.Status.idle,
    owner_id=487845696100368384
)
bot.embed_color = 0x0EA1EB
bot.remove_command("help")
slash = discord_slash.SlashCommand(
    bot,
    sync_commands=True,
    sync_on_cog_edit=True
)


for cog in listdir("./cogs"):
    if cog.endswith(".py"):
        bot.load_extension(f"cogs.{cog[:-3]}")
        print(f"Загружено расширение: {cog[:-3]}...")

@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    print("Загружен модуль дебага...")

    print(f"Бот запущен как {str(bot.user)}")

@bot.event
async def on_slash_command_error(ctx, ex):
    ...


if __name__ == "__main__":
    bot.run(TOKEN)
