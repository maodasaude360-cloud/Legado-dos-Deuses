import time
import discord

from discord.ext import commands

from database.database import (
    criar_usuario,
    obter_usuario,
    adicionar_xp,
    atualizar_level,
    adicionar_mensagem
)

# ==========================
# CONFIGURAÇÕES
# ==========================

XP_POR_MENSAGEM = 10
COOLDOWN = 60

cooldowns = {}


def xp_necessario(level):
    """
    XP necessário para alcançar o próximo nível.
    """

    return level * 100


# ==========================
# COG
# ==========================

class Levels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignora bots
        if message.author.bot:
            return

        user_id = message.author.id

        # Garante usuário no banco
        criar_usuario(user_id)

        # Conta mensagens SEMPRE
        adicionar_mensagem(user_id)

        agora = time.time()

        # Cooldown de XP
        if user_id in cooldowns:

            if agora - cooldowns[user_id] < COOLDOWN:
                return

        cooldowns[user_id] = agora

        # Adiciona XP
        adicionar_xp(
            user_id,
            XP_POR_MENSAGEM
        )

        # Atualiza dados
        usuario = obter_usuario(user_id)

        xp = usuario["xp"]
        level = usuario["level"]

        level_antigo = level

        # Verifica múltiplos níveis
        while xp >= xp_necessario(level):

            level += 1

        # Atualiza apenas se subiu
        if level > level_antigo:

            atualizar_level(
                user_id,
                level
            )

            embed = discord.Embed(
                title="🏛️ Ascensão Divina",
                description=(
                    f"{message.author.mention}\n\n"
                    f"Alcançou o nível **{level}**.\n\n"
                    f"Os deuses observam seus feitos."
                ),
                color=discord.Color.gold()
            )

            embed.set_thumbnail(
                url=message.author.display_avatar.url
            )

            embed.add_field(
                name="⭐ XP Atual",
                value=str(xp),
                inline=True
            )

            embed.add_field(
                name="🏆 Nível",
                value=str(level),
                inline=True
            )

            embed.set_footer(
                text="Legado dos Deuses"
            )

            await message.channel.send(
                embed=embed
            )


# ==========================
# SETUP
# ==========================

async def setup(bot):

    await bot.add_cog(
        Levels(bot)
    )

    print(
        "⭐ Levels carregado!"
    )