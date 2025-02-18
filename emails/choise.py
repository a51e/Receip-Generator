import asyncio
import os
import re
import smtplib
import discord
import json
from discord import ui
from datetime import datetime, timedelta
from emails.normal import SendNormal
from emails.spoofed import SendSpoofed
import sqlite3

# Datenbankverbindung herstellen
conn = sqlite3.connect('data.db')
cursor = conn.cursor()



class choiseView(discord.ui.View):
    def __init__(self, owner_id, html_content, sender_email, subject, product_name, image_url, url):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.html_content = html_content
        self.sender_email = sender_email
        self.subject = subject
        self.product_name = product_name
        self.image_url = image_url
        self.url = url


    @discord.ui.button(label="Spoofed Email", style=discord.ButtonStyle.danger)
    async def handle_spoofed(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:

            cursor.execute("SELECT email FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            result = cursor.fetchone()

            print(result)
            if result:
                receiver_email = result[0]

                if receiver_email: 
                    
                    embed = discord.Embed(title="Sending...", description="")
                    await interaction.response.edit_message(embed=embed, view=None)

                    try:
                        email_sender = SendSpoofed(self.sender_email, receiver_email, self.subject, self.html_content)
                        email_sender.send_email()

                        embed = discord.Embed(title=f"Confirmation", description=f"{interaction.user.mention} Spoofed email sent successfully!", url=self.url)
                        embed.add_field(name="", value=f"» Product: **{self.product_name}**\n")
                        if self.image_url == "None":
                            pass
                        else:
                            embed.set_thumbnail(url=f"{self.image_url}")
                        await interaction.edit_original_response(embed=embed, view=None)
                        await interaction.followup.send(content="Tip: **Spoofed Domain** will not always work, please try **Default Domain** if you didn't receive an email!\nIf your email doesn't show up in **Inbox** check **Spam** and remove it to load images.", ephemeral=True)

                    except smtplib.SMTPRecipientsRefused as e:
                        print(f"Failed to send email: {e}")
                        # Optionally, notify the user in Discord about the error
                        embed = discord.Embed(title="Error", description="Failed to send email due to SMTP recipient refusal.")
                        await interaction.edit_original_response(embed=embed, view=None)

                else:
                    embed = discord.Embed(title="Error", description=f"{interaction.user.mention} Email address not found in the configuration.\n Make sure you added your email.")
                    await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(title="Error", description=f"{interaction.user.mention} User ID not found in the configuration.\n Make sure you added your email.")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)

    

    @discord.ui.button(label="Normal Email", style=discord.ButtonStyle.danger)
    async def handle_normal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:

            cursor.execute("SELECT email FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            result = cursor.fetchone()

            print(result)
            if result:
                receiver_email = result[0]
                
                if receiver_email:

                    embed = discord.Embed(title="Sending...", description="")
                    await interaction.response.edit_message(embed=embed, view=None)

                                                               
                    new_email = "noreply@maisonreceipts.cc"
                    formatted_sender_email = re.sub(r"<[^>]+>", f"<{new_email}>", self.sender_email)

                    try:
                        email_sender = SendNormal(formatted_sender_email, receiver_email, self.subject, self.html_content)
                        email_sender.send_email()

                        embed = discord.Embed(title=f"Confirmation", description=f"{interaction.user.mention} Normal email sent successfully!", url=self.url)
                        embed.add_field(name="", value=f"» Product: **{self.product_name}**\n")
                        if self.image_url == "None":
                            pass
                        else:
                            embed.set_thumbnail(url=f"{self.image_url}")
                        await interaction.edit_original_response(embed=embed, view=None)

                    except smtplib.SMTPRecipientsRefused as e:
                        print(f"Failed to send email: {e}")
                        # Optionally, notify the user in Discord about the error
                        embed = discord.Embed(title="Error", description="Failed to send email due to SMTP recipient refusal.")
                        await interaction.edit_original_response(embed=embed, view=None)

                else:
                    embed = discord.Embed(title="Error", description=f"{interaction.user.mention} Email address not found in the configuration.\n Make sure you added your email.")
                    await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(title="Error", description=f"{interaction.user.mention} User ID not found in the configuration.\n Make sure you added your email.")
                await interaction.response.edit_message(embed=embed, view=None)
                
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)
