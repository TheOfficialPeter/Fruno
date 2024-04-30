import discord
from discord.ext import commands
import aiohttp
import requests
from PIL import Image
from io import BytesIO

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        print("FetchCommand Cog initialized.")

    async def fetch_image(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    def create_progress_bar(self, value):
        """
        Create a beautiful ASCII progress bar.
        """
        bar_length = 20
        filled_length = int(bar_length * value)
        bar = '█' * filled_length + '▒' * (bar_length - filled_length)
        return f"[{value:.2f}/1] {bar}"

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

            # Defer the response to let Discord know the bot is processing
            await self.ctx.defer()

            # Make the HTTP GET request using aiohttp
            url = f"https://fruno-1-h7317751.deta.app/fetch?name={name}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"Received response: {data}")

                        # Extract the relevant information from the JSON response
                        data = data.get("data")
                        game_name = data.get('name');
                        tier = data.get('tier');
                        score = data.get('score');
                        game_id = data.get('objectId');
                        header_image = data.get('image');

                        # Fetch the header image and calculate the average color
                        image_data = await self.fetch_image(header_image)
                        image = Image.open(BytesIO(image_data))
                        average_color = self.get_average_color(image)

                        # Create an embed to display the information
                        embed = discord.Embed(title="Game Information", color=average_color)
                        embed.add_field(name="Name", value=game_name, inline=False)
                        embed.add_field(name="Tier", value=tier, inline=False)
                        embed.add_field(name="Score", value=self.create_progress_bar(score), inline=False)
                        embed.add_field(name="Game ID", value=game_id, inline=False)
                        if header_image:
                            embed.set_image(url=header_image)

                        # Send the response using the saved ctx object
                        await self.ctx.send(embed=embed)

                        # Delete the loading message
                        await self.ctx.interaction.delete_original_response()
                    else:
                        await self.ctx.send(f"Error fetching information for {name}.")
                        await self.ctx.interaction.delete_original_response()
        else:
            print(f"User {self.ctx.author} does not have the 'Verified' role.")
            await self.ctx.send("You do not have the required role to use this command.")
            await self.ctx.interaction.delete_original_response()

    def get_average_color(self, image):
        """
        Calculate the average color of an image.
        """
        pixels = image.getdata()
        r, g, b = 0, 0, 0
        for pixel in pixels:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        num_pixels = len(pixels)
        return discord.Color.from_rgb(r // num_pixels, g // num_pixels, b // num_pixels)
