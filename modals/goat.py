import asyncio
from base64 import b64decode
import json
import random
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





def is_goat_link(link):
    goat_link_pattern = re.compile(r'^https?://(www\.)?goat\.com/.*$')
    return bool(goat_link_pattern.match(link))


class goat(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="Goat link", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    colorr = discord.ui.TextInput(label="Color", placeholder="Black", required=True)
    sizee = discord.ui.TextInput(label="Size (If no size leave blank)", placeholder="US M", required=False)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="1693", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            link = self.Link.value
            currency = self.currency.value
            colorr = self.colorr.value
            sizee = self.sizee.value if self.sizee.value else ""
            

            if not is_goat_link(link):
                embed = discord.Embed(title="Error - Invalid Goat link", description="Please provide a valid Goat link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/goat.html", "r", encoding="utf-8") as file:
                    html_content = file.read()


                # Zyte API setup
                url = link  # Link should be defined or passed into the class

                # Zyte API request
                api_response = requests.post(
                    "https://api.zyte.com/v1/extract",
                    auth=("c75647e5bd0e425db76b57feebf89590", ""),
                    json={
                        "url": url,
                        "browserHtml": True,
                        "product": True,
                        "productOptions": {"extractFrom": "browserHtml"},
                    },
                )

                # Decode HTML data and parse it
                browser_html = api_response.json().get("browserHtml")
                soup = BeautifulSoup(browser_html, 'html.parser')
                print()
                print(f"[{Colors.green}START Scraping{lg}] GOAT -> {interaction.user.id} ({interaction.user})" + lg)


                og_image_url = "Image URL not found"

                product_name = "Product Name not found"

                # Check for additional product information in API response
                product_data = api_response.json().get("product")
                if product_data:
                    product_name = product_data.get("name", product_name)  # Override if name found
                    og_image_url = product_data.get("mainImage", {}).get("url", og_image_url)  # Override if mainImage URL found


                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {og_image_url}" + lg)



                print(f"[{Colors.green}Scraping DONE{lg}] GOAT -> {interaction.user.id}" + lg)
                print()



                price = self.price.value



                html_content = html_content.replace("{imageurl}", og_image_url)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{sizee}", sizee)
                html_content = html_content.replace("{color}", colorr)
                html_content = html_content.replace("{price}", price)
                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{currency}", currency)





                with open("receipt/updatedrecipies/updatedgoat.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "GOAT <info@goat.com>"
                subject = f"Your GOAT order #511637332"

                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, og_image_url, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



        
