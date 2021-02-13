import discord
import discord_slash
import jishaku

from discord.ext import commands

from os import getenv, listdir


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
    sync_commands=True,
    delete_from_unused_guilds=True,
    sync_on_cog_edit=True
)

@bot.event
async def on_ready():
    for cog in listdir("./cogs"):
        if cog.endswith(".py"):
            bot.load_extension(f"cogs.{cog[:-3]}")
            print(f"Загружено расширение: {cog[:-3]}...")
    
    bot.load_extension("jishaku")
    print("Загружен модуль дебага...")

    print(f"Бот запущен как {str(bot.user)}")


if __name__ == "__main__":
    bot.run(TOKEN)
