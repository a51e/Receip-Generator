import asyncio
import json
import re
import webbrowser
import discord
from discord.ui import Select
from discord import SelectOption, ui, app_commands
from datetime import datetime

import hashlib
import sys

import os
import json as jsond  # json
import time  # sleep before exit
import binascii  # hex encoding
from uuid import uuid4

import requests  # gen random guid





import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



from bs4 import BeautifulSoup

from pystyle import Colors


r = Colors.red
lg = Colors.light_gray



class spidermodal(ui.Modal, title="discord.gg/maison"):
    Priceff = discord.ui.TextInput(label="Price without currency", placeholder="790.00", required=True)
    currencyff = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    pname = discord.ui.TextInput(label="Product Name", placeholder="Sp5der Angel Number Hoodie", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (discord image)", placeholder="https://cdn.discordapp.com/attachments/10869879156.....", required=True)
    Size = discord.ui.TextInput(label="Size", placeholder="XL", required=True)



    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            currencyff = self.currencyff.value
            Priceff = self.Priceff.value
            pname = self.pname.value
            imageurl = self.imageurl.value
            cityzip = f"{city} {zipp}"
            size = self.Size.value

            try:
                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)



                with open("receipt/spider.html", "r", encoding="utf-8") as file:
                    html_content = file.read()





                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{currency}", str(currencyff)) 
                html_content = html_content.replace("{price}", str(Priceff)) 
                html_content = html_content.replace("{imageurl}", str(imageurl))
                html_content = html_content.replace("{pname}", pname)
                html_content = html_content.replace("{size}", size)

                

                with open("receipt/updatedrecipies/updatedspider.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "sp5der <noreply@spiderclothing.us>"
                subject = "Order #SP148782 confirmed"
                from emails.choise import choiseView
                owner_id = interaction.user.id
                link = "https://spiderclothing.us/"

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, pname, imageurl, link)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)
        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


