import asyncio
from base64 import b64decode
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





def is_amazon_link(link):
    amazon_link_pattern = re.compile(r'^https?://(www\.)?amazon\.com/.*$')
    return bool(amazon_link_pattern.match(link))


class amazonmodal(ui.Modal, title="discord.gg/maison"):
    pname = discord.ui.TextInput(label="Product Name", placeholder="Jeans", required=True)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="160.54", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    arriving = discord.ui.TextInput(label="Arriving (DD/MM/YYYY)", placeholder="06/06/2024", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (Discord Image))", placeholder="https://cdn.discordapp.com/attachments/...", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 


        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            currency = self.currency.value
            price = self.price.value
            arriving = self.arriving.value
            imageurl = self.imageurl.value
            pname = self.pname.value

            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/amazon.html", "r", encoding="utf-8") as file:
                    html_content = file.read()


                
                print()
                print(f"[{Colors.green}START Scraping{lg}] Amazon -> {interaction.user.id} ({interaction.user})" + lg)
                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {pname}" + lg)
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {imageurl}" + lg)
                print(f"[{Colors.green}Scraping DONE{lg}] Amazon -> {interaction.user.id}" + lg)
                print()



                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{total}", price)
                html_content = html_content.replace("{arriving}", arriving)
                html_content = html_content.replace("{imageurl}", imageurl)
                html_content = html_content.replace("{pname}", pname)









                with open("receipt/updatedrecipies/updatedamazon.html", "w", encoding="utf-8") as file:
                    file.write(html_content)

                from emails.choise import choiseView
                sender_email = "<no-reply@amazon.com>"
                subject = f"Your Amazon.com order."
                link = "https://amazon.com/"

                    
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





        
       