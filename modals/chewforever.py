import asyncio
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

from emails.normal import SendNormal


r = Colors.red
lg = Colors.light_gray



def is_Chewforever_link(link):
    Chewforever_pattern = re.compile(r'^https?://(www\.)?chewforever\.com/.+')

    return bool(Chewforever_pattern.match(link))


class Chewforevermodal(ui.Modal, title="discord.gg/maison"):
    link = discord.ui.TextInput(label="Link", placeholder="https://chewforever.com/", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790.00", required=True)
    shipping = discord.ui.TextInput(label="Shipping Costs", placeholder="10.00", required=True)
    tax = discord.ui.TextInput(label="Tax Costs", placeholder="10.00", required=True)
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

            currency = self.currency.value
            Price = float(self.Price.value)
            link = self.link.value
            tax = float(self.tax.value)
            shipping = float(self.shipping.value)

            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)
            try:
                with open("receipt/chewforever.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

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
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] Chewforever -> {interaction.user.id} ({interaction.user})" + lg)

                    productname = soup.find('meta', {'property': 'og:title'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {productname}" + lg)


                    image_url = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)

                    print(f"[{Colors.green}Scraping DONE{lg}] Chewforever -> {interaction.user.id} ({interaction.user})" + lg)
                    print()

                            


                    fulltotal = shipping + tax + Price
                    fulltotal = round(fulltotal, 2)

                    def generate_order_number():
                        return str(random.randint(10000, 99999))  # Generiert eine Zahl zwischen 10000000 und 99999999

                    # Bestellnummer generieren
                    order_number = generate_order_number()


                    html_content = html_content.replace("{name}", name)
                    html_content = html_content.replace("{street}", street)
                    html_content = html_content.replace("{city}", city)
                    html_content = html_content.replace("{zip}", zipp)
                    html_content = html_content.replace("{country}", country)

                    html_content = html_content.replace("{price}", str(Price))
                    html_content = html_content.replace("{tax}", str(tax))
                    html_content = html_content.replace("{shipping}", str(shipping))
                    html_content = html_content.replace("{currency}", currency)
                    html_content = html_content.replace("{total}", str(fulltotal))
                    html_content = html_content.replace("{ordernumber}", order_number)
                    html_content = html_content.replace("{pname}", productname)
                    html_content = html_content.replace("{imageurl}", image_url)










                    

                    with open("receipt/updatedrecipies/updatedChewforever.html", "w", encoding="utf-8") as file:
                        file.write(html_content)



                    sender_email = "Chew Forever <noreply@chewforever.com>"
                    subject = f"Order #{order_number} confirmed"
                    from emails.choise import choiseView
                    owner_id = interaction.user.id

                        
                    embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                    view = choiseView(owner_id, html_content, sender_email, subject, productname, image_url, link)
                    await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)



                
        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


        