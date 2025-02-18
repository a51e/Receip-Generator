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





def is_fightclub_link(link):
    fightclub_link_pattern = re.compile(r'^https?://(www\.)?flightclub\.com/.*$')
    return bool(fightclub_link_pattern.match(link))


class fightclubmodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://flightclub.com/...", required=True)
    price = discord.ui.TextInput(label="Price without currency", placeholder="120.30", required=True)
    color = discord.ui.TextInput(label="Color", placeholder="Black", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="46", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)





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
            price = self.price.value
            color = self.color.value
            size = self.size.value
            currency = self.currency.value






            

            if not is_fightclub_link(link):
                embed = discord.Embed(title="Error - Invalid Flightclub link", description="Please provide a valid Flightclub link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/fightclub.html", "r", encoding="utf-8") as file:
                    html_content = file.read()


                # Zyte API setup
                url = link

                response = requests.get(
                    url=url,
                    proxies={
                        "http": "http://c75647e5bd0e425db76b57feebf89590:@api.zyte.com:8011/",
                        "https": "http://c75647e5bd0e425db76b57feebf89590:@api.zyte.com:8011/",
                    },
                    verify='zyte-ca.crt' 
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] Flightclub -> {interaction.user.id} ({interaction.user})" + lg)

                    scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
                    for script in scripts:
                        try:
                            data = json.loads(script.string)
                            # Check if the data type is Product
                            if data['@type'].lower() == 'product':
                                product_name = data.get('name', 'No product name found')
                                image_url = data.get('image', 'No image URL found')
                                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
                                break
                        except json.JSONDecodeError as e:
                            print('Error decoding JSON:', e)



                    print(f"[{Colors.green}Scraping DONE{lg}] Flightclub -> {interaction.user.id}" + lg)
                    print()



                def generate_order_number():
                    return str(random.randint(1000000000, 9999999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

                # Bestellnummer generieren
                order_number = generate_order_number()


                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)


                html_content = html_content.replace("{ordernumber}", order_number)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{imageurl}", image_url)

                html_content = html_content.replace("{price}", price)
                html_content = html_content.replace("{color}", color)
                html_content = html_content.replace("{size}", size)
                html_content = html_content.replace("{currency}", currency)





                with open("receipt/updatedrecipies/updatedflightclub.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "Flight Club <orders@flightclub.com>"
                subject = f"Your Flight Club order #{order_number} "

                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)




    