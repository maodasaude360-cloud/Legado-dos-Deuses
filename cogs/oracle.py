import discord
import json
import os

from discord.ext import commands
from discord import app_commands

from database.database import (
    criar_usuario,
    definir_deus,
    obter_deus,
    resetar_deus
)


QUIZ_PATH = "data/quiz.json"

with open(QUIZ_PATH, "r", encoding="utf-8") as f:
    QUIZ_DATA = json.load(f)


CARGOS_DEUSES = {
    "Zeus": 1520910299740241921,
    "Poseidon": 1520912463522955344,
    "Ártemis": 1520914235956138004,
    "Afrodite": 1520913556768428194,
    "Ares": 1520913396919439582,
    "Apolo": 1520913683369164971,
    "Atena": 1520912881695326288,
    "Deméter": 1520913815917563994,
    "Dionísio": 1520914187042295918,
    "Hades": 1520912664124063814,
    "Hermes": 1520914069811368169,
    "Hebe": 1523856292538613821,
    "Hécate": 1523856359131582524,
    "Hefesto": 1520913929587396641,
    "Hipnos": 1523856142143455274,
    "Íris": 1523856090641731725,
    "Nêmesis": 1523856192886145034,
    "Nike": 1523856234917400728,
    "Tique": 1523856326030135306
}


def criar_embed_pergunta(indice):

    pergunta = QUIZ_DATA["questions"][indice]

    embed = discord.Embed(
        title=f"🔮 Pergunta {indice + 1} de {len(QUIZ_DATA['questions'])}",
        description=f"**{pergunta['question']}**",
        color=discord.Color.blurple()
    )

    for letra, dados in pergunta["answers"].items():

        embed.add_field(
            name=letra,
            value=dados["text"],
            inline=False
        )

    embed.set_footer(
        text="Responda com sinceridade. O Oráculo observa."
    )

    return embed
class QuizView(discord.ui.View):

    def __init__(self, user_id, pergunta_atual=0, pontuacoes=None):
        super().__init__(timeout=600)

        self.user_id = user_id
        self.pergunta_atual = pergunta_atual
        self.pontuacoes = pontuacoes or {}

    async def responder(self, interaction, alternativa):

        if interaction.user.id != self.user_id:

            await interaction.response.send_message(
                "⚠️ Apenas quem iniciou o Oráculo pode responder.",
                ephemeral=True
            )
            return

        pergunta = QUIZ_DATA["questions"][self.pergunta_atual]

        pontos = pergunta["answers"][alternativa]["points"]

        for deus, valor in pontos.items():

            self.pontuacoes[deus] = (
                self.pontuacoes.get(deus, 0) + valor
            )

        proxima = self.pergunta_atual + 1

        if proxima >= len(QUIZ_DATA["questions"]):

            vencedor = max(
                self.pontuacoes,
                key=self.pontuacoes.get
            )

            definir_deus(
                interaction.user.id,
                vencedor
            )

            cargo_id = CARGOS_DEUSES.get(vencedor)

            if cargo_id:

                cargo = interaction.guild.get_role(
                    cargo_id
                )

                if cargo:

                    try:
                        await interaction.user.add_roles(
                            cargo,
                            reason="Resultado do Oráculo"
                        )
                    except Exception:
                        pass

            embed = discord.Embed(
                title="🏛️ Julgamento Concluído",
                description=(
                    f"O destino foi revelado.\n\n"
                    f"⚡ Sua linhagem divina é:\n\n"
                    f"## {vencedor}"
                ),
                color=discord.Color.gold()
            )

            embed.add_field(
                name="🔮 Veredito do Oráculo",
                value=(
                    f"As Moiras teceram seu fio "
                    f"e apontaram o caminho de "
                    f"**{vencedor}**."
                ),
                inline=False
            )

            embed.set_footer(
                text="Legado dos Deuses"
            )

            await interaction.response.edit_message(
                embed=embed,
                view=None
            )

            return

        embed = criar_embed_pergunta(
            proxima
        )

        await interaction.response.edit_message(
            embed=embed,
            view=QuizView(
                self.user_id,
                proxima,
                self.pontuacoes
            )
        )

    @discord.ui.button(
        label="A",
        style=discord.ButtonStyle.primary
    )
    async def alternativa_a(
        self,
        interaction,
        button
    ):
        await self.responder(
            interaction,
            "A"
        )

    @discord.ui.button(
        label="B",
        style=discord.ButtonStyle.success
    )
    async def alternativa_b(
        self,
        interaction,
        button
    ):
        await self.responder(
            interaction,
            "B"
        )

    @discord.ui.button(
        label="C",
        style=discord.ButtonStyle.secondary
    )
    async def alternativa_c(
        self,
        interaction,
        button
    ):
        await self.responder(
            interaction,
            "C"
        )

    @discord.ui.button(
        label="D",
        style=discord.ButtonStyle.danger
    )
    async def alternativa_d(
        self,
        interaction,
        button
    ):
        await self.responder(
            interaction,
            "D"
        )
       
class StartOracleView(discord.ui.View):

    def __init__(self, user_id):
        super().__init__(timeout=300)
        self.user_id = user_id

    @discord.ui.button(
        label="✨ Iniciar Julgamento",
        style=discord.ButtonStyle.primary
    )
    async def iniciar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.user_id:

            await interaction.response.send_message(
                "⚠️ Apenas quem iniciou o Oráculo pode usar este botão.",
                ephemeral=True
            )
            return

        embed = criar_embed_pergunta(0)

        await interaction.response.edit_message(
            embed=embed,
            view=QuizView(
                user_id=self.user_id,
                pergunta_atual=0,
                pontuacoes={}
            )
        )


class Oracle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="oraculo",
        description="Descubra sua linhagem divina."
    )
    async def oraculo(
        self,
        interaction: discord.Interaction
    ):

        criar_usuario(interaction.user.id)

        deus = obter_deus(
            interaction.user.id
        )

        if deus:

            embed = discord.Embed(
                title="🔒 Destino Já Revelado",
                description=(
                    f"Sua linhagem divina já foi descoberta.\n\n"
                    f"⚡ Descendente de **{deus}**"
                ),
                color=discord.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🔮 O Oráculo de Delfos",
            description=(
                "Poucos conhecem sua verdadeira origem.\n\n"
                "Responda às perguntas com sinceridade e permita que o Oráculo interprete os sinais do destino.\n\n"
                "Ao final do julgamento, sua Linhagem Divina será revelada."
            ),
            color=discord.Color.gold()
        )

        await interaction.response.send_message(
    embed=embed,
    view=StartOracleView(
        interaction.user.id
    )
)

    @app_commands.command(
        name="resetar_oraculo",
        description="Reseta a linhagem divina de um usuário."
    )
    @app_commands.default_permissions(
        administrator=True
    )
    async def resetar_oraculo(
        self,
        interaction: discord.Interaction,
        membro: discord.Member
    ):

        resetar_deus(membro.id)

        await interaction.response.send_message(
            f"✅ Oráculo de {membro.mention} resetado.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        Oracle(bot)
    )