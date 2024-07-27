from discord.ext import commands
from Enums.enums import Role
from Logic.Fetch.fetchGameInfo import fetch_game_info
from UI.Embeds.gameInfoEmbed import generate_embed

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, name: str):
        await ctx.interaction.response.defer()

        if Role.BUYER.value in [role.name for role in ctx.author.roles] and name != "":
            success, message, embedData = fetch_game_info(name)

            if not success:
                await ctx.followup.send(message)

            success, message, embed, buttonRows = generate_embed(ctx, embedData)

            if not success:
                await ctx.followup.send(message)

            await ctx.followup.send(embed=embed, view=buttonRows)
        else:
            await ctx.interaction.respond("You do not have the required 'Buyer' role.")

def setup(bot):
    bot.add_cog(FetchCommand(bot))
