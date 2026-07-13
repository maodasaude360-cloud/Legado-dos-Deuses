import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.database import criar_tabelas

# =========================
# CONFIGURAÇÕES
# =========================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN não encontrado no arquivo .env")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# EVENTOS
# =========================

@bot.event
async def on_ready():

    print("\n" + "=" * 50)
    print(f"🏛️ {bot.user} conectado com sucesso!")
    print(f"🆔 ID: {bot.user.id}")
    print("=" * 50)

    try:
        synced = await bot.tree.sync()

        print(f"\n✅ {len(synced)} Slash Commands sincronizados.\n")

        for command in synced:
            print(f"• /{command.name}")

    except Exception as e:
        print("Erro ao sincronizar:")
        print(e)

# =========================
# COGS
# =========================

async def load_cogs():

    print("\n📦 Carregando módulos...\n")

    for file in os.listdir("./cogs"):

        if file.endswith(".py"):

            try:

                await bot.load_extension(
                    f"cogs.{file[:-3]}"
                )

                print(f"✅ {file}")

            except Exception as e:

                print(f"❌ {file}")
                print(e)

# =========================
# INICIALIZAÇÃO
# =========================

async def main():

    print("🚀 Iniciando Legado dos Deuses...")

    criar_tabelas()

    print("🗄️ Banco inicializado!")

    async with bot:

        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())