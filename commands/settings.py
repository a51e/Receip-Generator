import discord
from discord.ext import commands
from utils.utils import Utils
from addons.botsettings import botsettingsView




class settingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='settings', description='Admin Command')
    async def settings(self, interaction: discord.Interaction):
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
            title=f"Admin Settings",
            description="Select an option below to use the Panel"
            )
        
        bot = self.bot
        
        view = botsettingsView(owner_id, bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)



async def setup(bot):
    await bot.add_cog(settingsCog(bot))
