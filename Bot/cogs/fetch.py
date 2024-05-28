from discord.ext import commands

class Cog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, name: str):
        await ctx.respond('Hello from Cog1!')

def setup(bot):
    bot.add_cog(Cog1(bot))
