import discord

from discord.ext import commands
from discord import app_commands

from database.database import (
    criar_usuario,
    obter_usuario,
    posicao_ranking
)


def xp_necessario(level):
    return level * 100


def barra_xp(atual, maximo):

    porcentagem = min(
        atual / maximo,
        1
    )

    preenchido = int(
        porcentagem * 10
    )

    vazio = 10 - preenchido

    return (
        "█" * preenchido +
        "░" * vazio
    )


FRASES_DEUSES = {
    "Zeus": "⚡ O trovão responde ao seu chamado.",
    "Poseidon": "🌊 O mar reconhece sua autoridade.",
    "Hades": "💀 Nem a morte ignora sua presença.",
    "Atena": "🦉 A sabedoria guia seus passos.",
    "Ares": "⚔️ A batalha fortalece sua alma.",
    "Afrodite": "💖 O coração é sua maior força.",
    "Apolo": "☀️ A luz revela seu caminho.",
    "Ártemis": "🏹 A liberdade corre em suas veias.",
    "Hermes": "🪽 Nenhum caminho é rápido demais.",
    "Deméter": "🌾 Sua presença traz prosperidade.",
    "Dionísio": "🍷 A vida deve ser celebrada.",
    "Hefesto": "🔨 Grandes obras exigem paciência.",
    "Hécate": "🔮 Os mistérios caminham ao seu lado.",
    "Hebe": "✨ A juventude eterna inspira seu espírito.",
    "Hipnos": "🌙 Os sonhos conhecem seus segredos.",
    "Íris": "🌈 A esperança acompanha seus passos.",
    "Nike": "🏆 A vitória sorri para você.",
    "Nêmesis": "⚖️ Toda ação recebe seu retorno.",
    "Tique": "🎲 O destino dança ao seu redor."
}


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Mostra seu perfil divino."
    )
    async def profile(
        self,
        interaction: discord.Interaction
    ):

        user = interaction.user

        criar_usuario(user.id)

        dados = obter_usuario(user.id)

        ranking = posicao_ranking(user.id)

        xp = dados["xp"]
        level = dados["level"]

        xp_max = xp_necessario(level)

        progresso = barra_xp(
            xp,
            xp_max
        )

        deus = (
            dados["god"]
            if dados["god"]
            else "Desconhecida"
        )

        embed = discord.Embed(
            title="🏛️ Perfil Divino",
            description=(
                f"## {user.display_name}\n"
                f"🔮 Filho de **{deus}**"
            ),
            color=discord.Color.gold()
        )

        embed.set_thumbnail(
            url=user.display_avatar.url
        )

        embed.add_field(
            name="⭐ Evolução",
            value=(
                f"**Nível:** {level}\n"
                f"**XP:** {xp}/{xp_max}\n"
                f"`{progresso}`"
            ),
            inline=False
        )

        embed.add_field(
            name="🏛️ Conquistas",
            value=(
                f"🏅 Honras: **{dados['honors']}**\n"
                f"💬 Mensagens: **{dados['messages']}**\n"
                f"🏆 Ranking: **#{ranking}**"
            ),
            inline=True
        )

        embed.add_field(
            name="🔮 Linhagem",
            value=f"**{deus}**",
            inline=True
        )

        embed.set_footer(
            text=FRASES_DEUSES.get(
                deus,
                "O Olimpo observa seus feitos."
            )
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        Profile(bot)
    )