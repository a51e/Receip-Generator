import discord
import json
from discord.ext import commands
from utils.utils import Utils


config = json.load(open("config.json", encoding="utf-8"))




class whitelistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='unwhitelist', description='Unwhitelist a user with ease.')
    @discord.app_commands.describe(value="Member to unwhitelist")
    async def unwhitelist(self, interaction: discord.Interaction, value: discord.Member):
        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Whitelisted",
                    description="_You are not allowed to use the bot, please contact the respective owner._",
                    color=discord.Colour.red()
                )
            )
        
        if str(value.id) == config["owner_id"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"Already Owner!",
                    description=f"You are currently the owner! You cannot unwhitelist yourself.",
                    color=discord.Colour.red()
                )
            )

        
        if await Utils.remove_from_whitelist(value.id):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Successfully Unwhitelisted",
                    description=f"Successfully Unwhitelisted {value.mention}",
                    color=0xFF10A4
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="User Not Whitelisted!",
                    description=f"{value.mention} is currently not whitelisted.",
                    color=0xFF10A4
                )
            )


    @discord.app_commands.command(name='whitelist', description='Whitelist a user with ease.')
    @discord.app_commands.describe(value="Member to whitelist")
    async def whitelist(self, interaction: discord.Interaction, value: discord.Member):
        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Whitelisted",
                    description="_You are not allowed to use the bot, please contact the respective owner._",
                    color=discord.Colour.red()
                )
            )
        
        if str(value.id) == config["owner_id"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"Already Owner!",
                    description=f"You are currently the owner! You cannot unwhitelist yourself.",
                    color=discord.Colour.red()
                )
            )

        
        if await Utils.remove_from_whitelist(value.id):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Successfully Unwhitelisted",
                    description=f"Successfully Unwhitelisted {value.mention}",
                    color=0xFF10A4
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="User Not Whitelisted!",
                    description=f"{value.mention} is currently not whitelisted.",
                    color=0xFF10A4
                )
            )



async def setup(bot):
    await bot.add_cog(whitelistCog(bot))
