from discord.ext import commands

class Cog2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def goodbye(self, ctx):
        await ctx.send('Goodbye from Cog2!')

def setup(bot):
    bot.add_cog(Cog2(bot))
