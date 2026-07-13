import discord

from discord.ext import commands, tasks

from database.database import (
    top_usuarios,
    obter_deus
)

CANAL_RANKING = 1526232568209473607


class Ranking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.atualizar_ranking.start()

    def cog_unload(self):
        self.atualizar_ranking.cancel()

    @tasks.loop(minutes=5)
    async def atualizar_ranking(self):

        canal = self.bot.get_channel(
            CANAL_RANKING
        )

        if not canal:
            return

        ranking = top_usuarios(10)

        medalhas = [
            "🥇",
            "🥈",
            "🥉",
            "𝟰 ",
            "𝟱 ",
            "𝟲 ",
            "𝟳 ",
            "𝟴 ",
            "𝟵 ",
            "𝟭𝟬"
        ]

        descricao = ""

        for posicao, usuario in enumerate(ranking):

            membro = canal.guild.get_member(
                usuario["user_id"]
            )

            if not membro:
                continue

            deus = obter_deus(
                usuario["user_id"]
            )

            deus = deus or "Sem Linhagem"

            descricao += (
                f"{medalhas[posicao]} "
                f"{membro.mention} • "
                f"{deus} • "
                f"Nível {usuario['level']}\n"
            )

        descricao += (
            "\n Legado dos Deuses"
        )

        embed = discord.Embed(
            title="🏛️ Ranking do Olimpo",
            description=descricao,
            color=discord.Color.gold()
        )

        mensagens = [
            msg async for msg in canal.history(
                limit=20
            )
            if msg.author == self.bot.user
        ]

        if mensagens:

            await mensagens[0].edit(
                embed=embed
            )

        else:

            await canal.send(
                embed=embed
            )

    @atualizar_ranking.before_loop
    async def before_ranking(self):
        await self.bot.wait_until_ready()


async def setup(bot):

    await bot.add_cog(
        Ranking(bot)
    )

    print(
        "🏆 Ranking carregado!"
    )