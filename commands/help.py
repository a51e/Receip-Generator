import discord
from discord.ext import commands






class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='help', description='Admin')
    async def paypal(self, interaction: discord.Interaction):

        embed = discord.Embed(title="Help Menu Admin Commands",
            description="\n***All Whitelisted commands***\n \n➜**/panel** | See/Edits a user\n➜**/whitelist** | Whitelists user to use Admin Commands\n➜**/unwhitelist** | Unwhitelists user to use Admin Commands\n➜**/settings** | Change Bots configuration (Bot Name, Interface Name, Avatar, Activity, Customer Role)")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1086603158140227624/1089351424296632500/acio.gif")
        await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(helpCog(bot))
