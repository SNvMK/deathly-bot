import os

os.system("pip uninstall -y discord-py-slash-command")
os.system("pip install git+git://github.com/eunwoo1104/discord-py-slash-command.git")

import discord
import discord_slash
import jishaku

from discord.ext import commands
from discord.ext.commands import MissingPermissions, NotOwner

import aiopg
from os import getenv, listdir


TOKEN = getenv("TOKEN")
DATABASE_URL = getenv("DATABASE_URL")

bot = commands.AutoShardedBot(
    "/",
    intents=discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.competing, name="cum зоне"),
    status=discord.Status.idle,
    owner_id=487845696100368384
)
bot.embed_color = 0x0EA1EB
bot.db_url = DATABASE_URL
bot.remove_command("help")
slash = discord_slash.SlashCommand(
    bot,
    sync_commands=True,
    sync_on_cog_reload=True
)


for cog in listdir("./cogs"):
    if cog.endswith(".py"):
        bot.load_extension(f"cogs.{cog[:-3]}")
        print(f"Загружено расширение: {cog[:-3]}...")

permissions = {
    "manage_messages": "управление сообщениями",
    "administrator": "администратор",
    "kick_members": "кикать участников",
    "ban_members": "банить участников"
}

@bot.event
async def on_ready():
    async with aiopg.create_pool(bot.db_url) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                injection = """
                CREATE TABLE tags (
                    author NUMBER, 
                    name TEXT, 
                    response TEXT
                );
                """
                await cur.execute(injection)
    bot.load_extension("jishaku")
    print("Загружен модуль дебага...")

    print(f"Бот запущен как {str(bot.user)}")

@bot.event
async def on_slash_command_error(ctx, ex):
    if isinstance(ex, MissingPermissions):
        await ctx.send(f"Вы не имеете права *{permissions[ex.missing_perms[0]]}* для использования команды `{ctx.name}`", hidden=True)
    elif isinstance(ex, NotOwner):
        await ctx.send(f"Команду {ctx.name} может использовать только владелец", hidden=True)
    elif isinstance(ex, discord.HTTPException):
        await ctx.send("Короче серверам дискорда пизда)")


if __name__ == "__main__":
    bot.run(TOKEN)
