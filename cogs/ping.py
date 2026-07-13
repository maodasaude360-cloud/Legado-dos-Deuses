import discord

from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Verifica a latência do bot."
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏛️ Legado dos Deuses",
            description=f"⚡ Latência: **{latency}ms**",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Ping(bot))