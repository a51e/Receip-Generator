import random
import discord
from discord.ext import commands

from addons.paypalbuttons import paypalView






class paypalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='paypal', description='Displays the PayPal address for a payment')
    @discord.app_commands.choices(amount=[
        discord.app_commands.Choice(name="14.99€ - Month", value="14.99€"),
        discord.app_commands.Choice(name="29.99€ - Lifetime", value="29.99€"),
        discord.app_commands.Choice(name="Custom Input", value="custominput")
    ])
    @discord.app_commands.choices(email=[
        discord.app_commands.Choice(name="maybemaison@gmail.com", value="maybemaison@gmail.com"),
    ])
    async def paypal(self, interaction: discord.Interaction, amount: str, email: str, custom: str = None):

        
        if amount == "custominput":
            if custom is None:
                await interaction.response.send_message(content="Please provide a custom input.", ephemeral=True)
                return
            amount = custom

        
        embed = discord.Embed(title="PayPal Payment", description="Are you able to send via **Friends & Family**?")
        view = paypalView(email, amount)
        await interaction.response.send_message(content="<@&1112752230815252570>", embed=embed, view=view)



async def setup(bot):
    await bot.add_cog(paypalCog(bot))
