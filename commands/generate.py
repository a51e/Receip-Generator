import os
import discord
import json
import asyncio
from discord.ext import commands
from datetime import datetime
from addons.RegionalView import RegionSelectionView
import sqlite3


class GenerateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('data.db')  # Establish a connection to the SQLite database
        self.cursor = self.conn.cursor() 

    @discord.app_commands.command(name='generate', description='Generate 1:1 Receipts')
    async def receiptgen(self, interaction: discord.Interaction):
        user_id = interaction.user.id 
        user_roles = interaction.user.roles

    
        embed = discord.Embed(title="Dashboard", description=f'You have currently no access for DE and US receipts')

        # Load the config data to check licenses
        self.cursor.execute("SELECT expiry, key FROM licenses WHERE owner_id = ?", (str(user_id),))
        license = self.cursor.fetchone()

        if license:
            expiry_str, key = license
            expiry_date = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
            now = datetime.now()
            delta = expiry_date - now
            days_left = delta.days
            hours_left = delta.total_seconds() // 3600

            if expiry_date < now:
                embed.description = 'Your subscription has expired.'
            else:
                if key.startswith("LifetimeKey"):
                    embed.description = 'Please select your Receipt Language to continue generating receipts for.\nYou have a **``Lifetime``** subscription.'
                else:
                    if days_left > 0:
                        embed.description = f'Please select your Receipt Language to continue generating receipts for.\nYou have **``{days_left} Days``** left on your subscription.'
                    else:
                        embed.description = f'Please select your Receipt Language to continue generating receipts for.\nYou have **``{int(hours_left)} Hours``** left on your subscription.'

        embed.set_footer(text=f"{interaction.user}'s Panel", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        region_view = RegionSelectionView(user_id, user_roles)
        await interaction.response.send_message(embed=embed, view=region_view)

        # Wait for timeout or interaction
        await asyncio.sleep(160)
        follow_up_embed = discord.Embed(
            title="No Interaction",
            description="The menu timed out automatically due to no interaction.\nYou can type /gen again to generate receipts."
        )
        follow_up_embed.set_footer(
            text=f"{interaction.user}'s Panel", 
            icon_url=interaction.user.avatar
        )
        await interaction.edit_original_response(embed=follow_up_embed, view=None)



async def setup(bot):
    await bot.add_cog(GenerateCog(bot))
