import discord

class AnalyticsSelectMenu(discord.ui.View):
    def __init__(self, options):
        self.options = options

        @discord.ui.select( # the decorator that lets you specify the properties of the select menu
            placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = 1, # the maximum number of values that can be selected by the users
            options = [discord.SelectOption(label=option.title, description=option.description) for option in self.options] # the list of options from which users can choose, a required field
        )
        async def select_callback(self, select, interaction): # the function called when the user is done selecting options
            await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")