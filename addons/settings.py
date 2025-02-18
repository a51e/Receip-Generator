import sqlite3
import discord
import json
from datetime import datetime, timedelta
from discord import ui
from faker import Faker
from addons.emailmodal import emailmodal

fake = Faker()


def clientid(config_path="config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)
        return int(config.get("Client_ID"))  # Standardname, falls nicht vorhanden
clientidd = clientid()

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

class custinfomodal(ui.Modal, title="Set up your Credentials"):
    Name = ui.TextInput(label="Name ", style= discord.TextStyle.short, placeholder="Mike Hunt", required= True)
    street = ui.TextInput(label="Street ", style= discord.TextStyle.short, placeholder="Musterstraße 12", required= True)
    city = ui.TextInput(label="City ", style= discord.TextStyle.short, placeholder="Köln", required= True)
    zipp = ui.TextInput(label="Zip ", style= discord.TextStyle.short, placeholder="10015", required= True)
    country = ui.TextInput(label="Country ", style= discord.TextStyle.short, placeholder="Germany", required= True)


    async def on_submit(self, interaction: discord.Interaction):

        name = self.Name.value
        street = self.street.value
        city = self.city.value
        zipp = self.zipp.value
        country = self.country.value
        owner_id = str(interaction.user.id)


        required_role_ids = [clientidd]
        user_role_ids = [role.id for role in interaction.user.roles]

        if any(role_id in required_role_ids for role_id in user_role_ids):
            # Update or insert the credentials into the database
            cursor.execute("""
                INSERT INTO licenses (owner_id, name, street, city, zipp, country, credentialstf)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(owner_id) 
                DO UPDATE SET name = excluded.name, street = excluded.street, city = excluded.city, zipp = excluded.zipp, country = excluded.country, credentialstf = excluded.credentialstf;
            """, (owner_id, name, street, city, zipp, country, "True"))
            conn.commit()

            cursor.execute("SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            license_data = cursor.fetchone()
            if license_data:
                emailtf, credentialstf = license_data

            description = f"Please make sure you fill in the options below. (Data will save)\n\nEmail = **{emailtf}**\nCredentials = **{credentialstf}**"
            embed = discord.Embed(title="Dashboard", description=description)
            await interaction.response.edit_message(embed=embed)

            embed = discord.Embed(title="Success", description=f"Custom Credentials changed for {interaction.user.mention}.")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            # Error message if user does not have the required role
            embed = discord.Embed(title="Error", description=f"{interaction.user.mention}, you do not have a subscription to set up Credentials.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



class SettingsDrop(discord.ui.Select):
    def __init__(self, owner_id, user_roles):
        self.owner_id = owner_id

        options = [
            discord.SelectOption(label='Custom Info', description='Enter your details manually', emoji='📄'),
            discord.SelectOption(label='Random Info', description='Generate random details', emoji='🌐'),
            discord.SelectOption(label='Email', description='Update your email adress', emoji='📧'),
        ]


        super().__init__(placeholder='Select an option to proceed...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True)
            return
        
        if self.values[0] == 'Custom Info':
            await interaction.response.send_modal(custinfomodal())
        elif self.values[0] == 'Random Info':

            name = fake.name()
            street = fake.street_address()
            city = fake.city()
            zipp = fake.zipcode()
            country = "United States"
            owner_id = str(interaction.user.id)


            required_role_ids = [clientidd]
            user_role_ids = [role.id for role in interaction.user.roles]

            if any(role_id in required_role_ids for role_id in user_role_ids):
                # Update or insert the credentials into the database
                cursor.execute("""
                    INSERT INTO licenses (owner_id, name, street, city, zipp, country, credentialstf)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(owner_id) 
                    DO UPDATE SET name = excluded.name, street = excluded.street, city = excluded.city, zipp = excluded.zipp, country = excluded.country, credentialstf = excluded.credentialstf;
                """, (owner_id, name, street, city, zipp, country, "True"))
                conn.commit()

                cursor.execute("SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
                license_data = cursor.fetchone()

                if license_data:
                    emailtf, credentialstf = license_data

                description = f"Please make sure you fill in the options below. (Data will save)\n\nEmail = **{emailtf}**\nCredentials = **{credentialstf}**"
                embed = discord.Embed(title="Dashboard", description=description)
                await interaction.response.edit_message(embed=embed)


                embed = discord.Embed(title="Success", description=f"Custom Credentials changed for {interaction.user.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                # Error message if user does not have the required role
                embed = discord.Embed(title="Error", description=f"{interaction.user.mention}, you do not have a subscription to set up Credentials.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == 'Email':
            await interaction.response.send_modal(emailmodal())


class SettingsView(discord.ui.View):
    def __init__(self, owner_id, user_roles):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user_roles = user_roles

        # Add dropdown to the view
        self.add_item(SettingsDrop(owner_id, user_roles))




    @discord.ui.button(label="Go Back")
    async def handle_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            owner_id = interaction.user.id 
            user_roles = interaction.user.roles
            embed = discord.Embed(title="Dashboard", description='You have currently no access for DE and US receipts')

            # Fetch the license data from the SQLite database
            cursor.execute("SELECT expiry, key FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            x = cursor.fetchone()

            if x:
                expiry_str, key = x
                extime = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
                now = datetime.now()
                delta = extime - now
                days_left = delta.days
                hours_left = delta.total_seconds() // 3600

                if extime < now:
                    embed.description = 'You have currently no access for DE and US receipts'
                else:
                    if key.startswith("LifetimeKey"):
                        embed.description = 'Please select your Receipt Language to continue generating receipts for.\n You have a **``Lifetime``** subscription.'
                    elif days_left > 0:
                        embed.description = f'Please select your Receipt Language to continue generating receipts for.\nYou have **``{days_left} Days``** left on your subscription.'
                    else:
                        embed.description = f'Please select your Receipt Language to continue generating receipts for.\nYou have **``{int(hours_left)} Hours``** left on your subscription.'

                embed.set_footer(text=f"{interaction.user}'s Panel", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

            from addons.RegionalView import RegionSelectionView
            
            region_view = RegionSelectionView(owner_id, user_roles)
            await interaction.response.edit_message(embed=embed, view=region_view)
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True)
