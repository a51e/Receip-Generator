import os
import discord
import json
from discord import ui
from datetime import datetime, timedelta
import sqlite3


conn = sqlite3.connect('data.db')
cursor = conn.cursor()

config = json.load(open("config.json", encoding="utf-8"))


        
class adminDrop(discord.ui.Select):
    def __init__(self, owner_id, user):
        self.owner_id = owner_id
        self.user = user

        options = [
            discord.SelectOption(label='1 Month', description='Standard', emoji='🚀', value="1mstandard"),
            discord.SelectOption(label='Lifetime', description='Standard', emoji='🚀', value="lftstandard"),
        ]


        super().__init__(placeholder='Select an option to proceed...', min_values=1, max_values=1, options=options)


    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True)
            return
        value = self.values[0] 
        
        user = self.user
        guild = interaction.guild  # Getting the guild from the interaction
        user = guild.get_member(user)

        role_mapping = {
            'lftstandard': (1500, 'LifetimeKey'),
            '1mstandard': (32, '1Month'),
            'lftpremium': (1500, 'LifetimeKey'),
            '1mpremium': (32, '1Month')
        }

        buyer_role_id = int(config.get("Client_ID"))
        buyer_role = discord.utils.get(interaction.guild.roles, id=buyer_role_id)
        print(buyer_role_id, buyer_role)

        paper_role_name = 'Paper Access'  # Change this to the name of the role you want to give
        paper_role = discord.utils.get(interaction.guild.roles, name=paper_role_name)

        emu_role_name = 'Emu Access'  # Change this to the name of the role you want to give
        emu_role = discord.utils.get(interaction.guild.roles, name=emu_role_name)


        
        if value == '1mstandard':

            expiry_days, key_prefix = role_mapping[value]

            embed = discord.Embed(title="Thanks for choosing us!", description=f"Successfully added `1 Month` access to {user.mention} subscription.")
            embed.add_field(name="", value="**»** Go to <#1334294256864596078> and read the setup guide.\n**»** Please make a vouch in this format `+rep <10/10> <experience>` \n<#1333587524697854006>")
            embed.set_footer(text="Email can be changed once a week!.", icon_url="https://cdn.discordapp.com/emojis/1278802261748879390.webp?size=96&quality=lossless")
            await user.add_roles(buyer_role)


            expiry_days, key_prefix = role_mapping[value]
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            expiry_str = expiry_date.strftime('%d/%m/%Y %H:%M:%S')

            cursor.execute('''
            INSERT INTO licenses (owner_id, key, expiry, emailtf, credentialstf)
            VALUES (?, ?, ?, 'False', 'False')
            ON CONFLICT(owner_id) DO UPDATE SET
            key=excluded.key, expiry=excluded.expiry
            ''', (str(user.id), f"{key_prefix}-{user.id}", expiry_str))

            conn.commit()



            await interaction.response.send_message(embed=embed)

        elif value == 'lftstandard':

            expiry_days, key_prefix = role_mapping[value]

            embed = discord.Embed(title="Thanks for choosing us!", description=f"Successfully added `Lifetime` access to {user.mention} subscription.")
            embed.add_field(name="", value="**»** Go to <#1334294256864596078> and read the setup guide.\n**»** Please make a vouch in this format `+rep <10/10> <experience>` \n<#1333587524697854006>")
            embed.set_footer(text="Email can be changed once a week!.", icon_url="https://cdn.discordapp.com/emojis/1278802261748879390.webp?size=96&quality=lossless")
            await user.add_roles(buyer_role)


            expiry_days, key_prefix = role_mapping[value]
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            expiry_str = expiry_date.strftime('%d/%m/%Y %H:%M:%S')

            cursor.execute('''
            INSERT INTO licenses (owner_id, key, expiry, emailtf, credentialstf)
            VALUES (?, ?, ?, 'False', 'False')
            ON CONFLICT(owner_id) DO UPDATE SET
            key=excluded.key, expiry=excluded.expiry
            ''', (str(user.id), f"{key_prefix}-{user.id}", expiry_str))

            conn.commit()


            await interaction.response.send_message(embed=embed)

        







class PanelView(discord.ui.View):
    def __init__(self, owner_id, user):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user = user



    @discord.ui.button(label="Information", emoji="<:informationn:1329647518874730527>")
    async def handle_checktime(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            user = self.user
            guild = interaction.guild  # Getting the guild from the interaction
            user = guild.get_member(user)

            embed = discord.Embed(title="")
            user_found = False

            # SQL-Abfrage zur Überprüfung der Lizenzinformationen
            cursor.execute('''
            SELECT owner_id, key, expiry, email FROM licenses WHERE owner_id = ?
            ''', (str(user.id),))
            license_info = cursor.fetchone()

            if license_info:
                owner_id, key, expiry_str, email = license_info
                expiry_date = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
                current_date = datetime.now()

                remaining_days = (expiry_date - current_date).days

                embed.add_field(name="", value=f"User: <@{owner_id}>\nExpiry: {expiry_str} ``{remaining_days} Days``\nEmail: `{email}`", inline=False)
                user_found = True

            if not user_found:
                embed.add_field(name="Error", value="User not found or does not exist.", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)


    @discord.ui.button(label="Add Access", emoji="<:Tools:1329647517276700722>")
    async def handle_addaccess(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            owner = self.owner_id
            user = self.user
            view = discord.ui.View()
            view.add_item(adminDrop(owner, user))  # Add the dropdown as an item
            await interaction.response.send_message(content="", view=view, ephemeral=True) 

        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)


    @discord.ui.button(label="Remove Access", emoji="<:Trash:1329647515963883671>")
    async def handle_removeaccess(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            user = self.user
            guild = interaction.guild  # Getting the guild from the interaction
            user = guild.get_member(user)

            # Entferne Lizenzdaten aus der SQLite-Datenbank
            cursor.execute('DELETE FROM licenses WHERE owner_id = ?', (str(user.id),))
            conn.commit()

            # Entferne zugehörige Rollen
            buyer_role_name = 'Client'
            buyer_role = discord.utils.get(interaction.guild.roles, name=buyer_role_name)

            paper_role_name = 'Paper Access'
            paper_role = discord.utils.get(interaction.guild.roles, name=paper_role_name)

            emu_role_name = 'Emu Access'
            emu_role = discord.utils.get(interaction.guild.roles, name=emu_role_name)

            roles_to_remove = [role for role in [buyer_role, paper_role, emu_role] if role in user.roles]
            if roles_to_remove:
                await user.remove_roles(*roles_to_remove)

            # Send a response message
            await interaction.response.send_message(embed=discord.Embed(
                title="Removed access from user",
                description=f"The access for {user.mention} has been removed successfully.",
                color=discord.Color.green()
            ), ephemeral=True)

        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)


    @discord.ui.button(label="Remove Email", emoji="<:Trash:1329647515963883671>")
    async def handle_removeemail(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            user = self.user
            guild = interaction.guild  # Getting the guild from the interaction
            user = guild.get_member(user)

            # Aktualisiere die Datenbank, um die E-Mail-Informationen zu entfernen
            cursor.execute('''
            UPDATE licenses
            SET email = NULL, last_email_update = NULL, emailtf = 'False'
            WHERE owner_id = ?
            ''', (str(user.id),))
            conn.commit()

            # Send a response message
            await interaction.response.send_message(embed=discord.Embed(
                title="Removed email from user",
                description=f"The email for {user.mention} has been removed successfully.",
                color=discord.Color.green()
            ), ephemeral=True)

        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)

    