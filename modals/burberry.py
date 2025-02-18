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


r = Colors.red
lg = Colors.light_gray



def is_burberry_link(link):
    burberry_pattern = re.compile(r'^https?://(www\.)?us\.burberry\.com/.+')

    return bool(burberry_pattern.match(link))


class burberrymodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://us.burberry.com/...", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="990.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    sizee = discord.ui.TextInput(label="Size", placeholder="XS", required=False)
    sku = discord.ui.TextInput(label="Articel Number", placeholder="81026761", required=False)




    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            Link = self.Link.value
            Price = self.Price.value
            currency = str(self.currency.value)
            sizee = self.sizee.value
            sku = self.sku.value



            

            if not is_burberry_link(Link):
                embed = discord.Embed(title="Error - Invalid burberry link", description="Please provide a valid burberry link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            
            try:

                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)

                



                with open("receipt/burberry.html", "r", encoding="utf-8") as file:
                    html_content = file.read()


                url = Link

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
                    print(f"[{Colors.green}START Scraping{lg}] burberry-> {interaction.user.id} ({interaction.user})" + lg)



                    productname = soup.find('h1', {'class': 'product-info-panel__title css-183zbdt e19cbv3t0'}).text.strip()
                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {productname}" + lg)

                    color2 = soup.find('div', {'class': 'product-swatches-panel__description'})
                    if color2:
                        color = color2.find('span', {'class': 'css-1t42rsd e19cbv3t0'}).text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {color}" + lg)


                    image_url = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] burberry -> {interaction.user.id}" + lg)
                    print()


                        



                def generate_order_number():
                    return str(random.randint(10000000, 99999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

                # Bestellnummer generieren
                order_number = generate_order_number()
                



                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)

                html_content = html_content.replace("{ordernumber}", order_number)
                html_content = html_content.replace("{pname}", productname)
                html_content = html_content.replace("{imageurl}", image_url)
                html_content = html_content.replace("{color}", color)
                html_content = html_content.replace("{articalnum}", sku)
                html_content = html_content.replace("{price}", Price)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{size}", sizee)




                

                with open("receipt/updatedrecipies/updateburberry.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "customerservice <noreply@orders.mail.burberry.com>"
                subject = f"Thank you for your order"
                from emails.choise import choiseView

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, productname, image_url, Link)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)



        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


        