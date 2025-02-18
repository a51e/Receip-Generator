import random
import sqlite3
import discord
import json
from datetime import datetime, timedelta
from discord import ui


class paypalView(discord.ui.View):
    def __init__(self, email, amount):
        super().__init__(timeout=None)

        self.email = email
        self.amount = amount
        self.notes = [
            "Taxi", "Food", "Uber", "Groceries", "From Mom",
            "Gift", "Utilities", "Dinner", "Drinks",
            "Movie", "Concert", "Book", "Fitness", "Health",
            "Donation", "Course",
            "Travel", "Hotel", "Flight", "Car Rental", "Shopping",
            "Sports", "Equipment", "Festival", "Parking", "Pet Supplies",
            "Party Supplies", "Art Supplies", "Gardening", "Household",
            "Beauty Products", "Personal Care", "Electronics", "Software",
            "Games", "Music", "Apparel"
        ]




    @discord.ui.button(label="Yes")
    async def handle_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        note = random.choice(self.notes)
        embed = discord.Embed(title="PayPal Payment")
        embed.add_field(name=f"Email:", value=f"```{self.email}```", inline=False)
        embed.add_field(name=f"Amount:", value=f"```{self.amount}```", inline=False)
        embed.add_field(name=f"Note:", value=f"```{note}```", inline=False)
        embed.add_field(name=f"Disclamer:", value=f"Please send the amount using **Friends & Family** and the written **Note** provided.")
        await interaction.response.edit_message(embed=embed, view=None)



    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def handle_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="PayPal Payment canceled.", embed=None, view=None)