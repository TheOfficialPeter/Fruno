from discord.ext import commands
from discord import Embed, Colour

class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="info")
    async def info(self, ctx):
        
        embed = Embed(
            title="Info about the Fruno Bot",
            description="The best game assistance bot on discord.",
            color=Colour.green(),
        )

        embed.add_field(name="--- /// Background\n", value="This bot was made to help gamers find information about games quickly without any hassle. The main idea came when I was switching to Linux and realized that its a hassle looking for games to play since some work and some don't and checking on multiple websites each time was a little frustrating so I thought of a way to make the process faster, but with other features too.")

        embed.add_field(name="--- /// Pricing?\n", value="Currently **Free to use** for selected servers for basic actions,  more paid features will be added. Like the AI game recommendation feature, Game installation guide, Deal and Promotions Webhook notifier.", inline=False)
        embed.add_field(name="--- /// How can I use it in my server?\n", value="Shoot me a dm so we can discuss integration into your server", inline=False)
        embed.add_field(name="--- /// Uptime?", value="Depends on my hosting provider. Expected to be 99.9%. We do have maintenance times", inline=False)
    
        embed.set_footer(text="Made b TheOfficialPeter") # footers can have icons too
        embed.set_author(name="Fruno")

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(InfoCommand(bot))
