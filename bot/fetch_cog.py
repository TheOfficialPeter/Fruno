import discord
from discord.ext import commands
import requests
import json

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        print("FetchCommand Cog initialized.")

    @commands.slash_command(name="fetch", description="Fetch some information")
    async def fetch(self, ctx, name: str):
        """
        Fetch some information.
        """
        # Save the ctx object in a variable
        self.ctx = ctx

        # Check if the user has the "Verified" role
        verified_role = discord.utils.get(self.ctx.guild.roles, name="Verified")
        if verified_role in self.ctx.author.roles:
            print(f"User {self.ctx.author} has the 'Verified' role.")
            print(f"Received name input: {name}")

            # Make the HTTP GET request using requests
            url = f"https://fruno-1-h7317751.deta.app/fetch?name={name}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                print(f"Received response: {data}")
                # Defer the response to let Discord know the bot is processing
                await self.ctx.defer()

                # Extract the header_image from the JSON response
                header_image = data.get("proton_data", {}).get("header_image", "")

                # Create an embed to display the JSON object and the header image
                embed = discord.Embed(title=f"Information for {name}", description=f"```json\n{json.dumps(data, indent=2)}\n```")
                if header_image:
                    embed.set_image(url=header_image)

                # Send the response using the saved ctx object
                await self.ctx.respond(embed=embed)
            else:
                await self.ctx.respond(f"Error fetching information for {name}.")
        else:
            print(f"User {self.ctx.author} does not have the 'Verified' role.")
            await self.ctx.respond("You do not have the required role to use this command.")
