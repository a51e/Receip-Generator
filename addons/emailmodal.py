import discord
import json
from datetime import datetime, timedelta
from discord import ui
import sqlite3

def clientid(config_path="config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)
        return int(config.get("Client_ID"))  # Standardname, falls nicht vorhanden


conn = sqlite3.connect('data.db')  # Connect to your SQLite database
cursor = conn.cursor()


class emailmodal(ui.Modal, title="Set up your Email"):
    email = ui.TextInput(label=" Email Adress ", style= discord.TextStyle.short, placeholder="Ex. youremail@gmail.com", required= True)


    async def on_submit(self, interaction: discord.Interaction):
        clientidd = clientid()
        entered_email = self.email.value.lower() 


        required_role_ids = [clientidd]
        user_role_ids = [role.id for role in interaction.user.roles]

        if any(role_id in required_role_ids for role_id in user_role_ids):
            cursor.execute("SELECT email, last_email_update FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            license_entry = cursor.fetchone()

            if license_entry:
                current_email, last_updated = license_entry
                if last_updated:
                    last_update_date = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() - last_update_date < timedelta(days=7):
                        embed = discord.Embed(title="Error", description="You can only change your email once a week.")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                # Update the email and the last_email_update timestamp
                cursor.execute("UPDATE licenses SET email = ?, last_email_update = ?, emailtf = 'True' WHERE owner_id = ?", (entered_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(interaction.user.id)))
                conn.commit()

                cursor.execute("SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
                license_data = cursor.fetchone()
                if license_data:
                    emailtf, credentialstf = license_data

                description = f"Please make sure you fill in the options below. (Data will save)\n\nEmail = **{emailtf}**\nCredentials = **{credentialstf}**"
                embed = discord.Embed(title="Dashboard", description=description)
                await interaction.response.edit_message(embed=embed)

                embed = discord.Embed(title="Success", description=f"The Email {entered_email} changed for {interaction.user.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description=f"{interaction.user.mention}, you do not have a subscription to set up an email.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Error message if user does not have the required role
            embed = discord.Embed(title="Error", description=f"{interaction.user.mention}, you do not have the necessary permissions to set up an email.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

