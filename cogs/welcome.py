import asyncio
import discord

from discord.ext import commands

from database.database import (
    criar_usuario,
    recebeu_boas_vindas,
    marcar_boas_vindas
)


class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        criar_usuario(
            message.author.id
        )

        if recebeu_boas_vindas(
            message.author.id
        ):
            return

        marcar_boas_vindas(
            message.author.id
        )

        embed = discord.Embed(
            title="⚡ Um novo semideus desperta",
            description=(
                f"Seja bem-vindo ao **Legado dos Deuses**, "
                f"{message.author.mention}.\n\n"
                f"🔮 Utilize **/oraculo** para descobrir sua linhagem divina.\n\n"
                f"⭐ Converse para ganhar XP e subir de nível.\n\n"
                f"🏛️ O Olimpo observa seus passos."
            ),
            color=discord.Color.gold()
        )

        embed.set_thumbnail(
            url=message.author.display_avatar.url
        )

        mensagem = await message.channel.send(
            embed=embed
        )

        await asyncio.sleep(20)

        try:
            await mensagem.delete()
        except:
            pass


async def setup(bot):

    await bot.add_cog(
        Welcome(bot)
    )

    print("👋 Welcome carregado!")