import os
import discord
import json
import asyncio
from discord.ext import commands
from datetime import datetime
from utils.utils import Utils
from utils.adminpanel import PanelView



class adminpanelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @discord.app_commands.command(name='edit', description='Admin Command')
    @discord.app_commands.describe(user="User get edited/checked")
    async def adminpanel(self, interaction: discord.Interaction, user: discord.Member):
        owner_id = interaction.user.id

        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Whitelisted",
                    description="_You are not allowed to use the bot, please contact the respective owner._",
                    color=discord.Colour.red()
                )
            )
        
        
        embed = discord.Embed(
            title=f"Admin Panel | User Connected: {user}",
            description="Select an option below to use the Panel"
            )
        
        view = PanelView(owner_id, user=user.id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        


        



async def setup(bot):
    await bot.add_cog(adminpanelCog(bot))





