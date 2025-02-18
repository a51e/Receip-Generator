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





def is_dior_link(link):
    dior_link_pattern = re.compile(r'^https?://(www\.)?dior\.com/.*$')
    return bool(dior_link_pattern.match(link))


class diormodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://dior.com/...", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="XS", required=True)
    shipping = discord.ui.TextInput(label="Shipping", placeholder="10.00", required=True)
    tax = discord.ui.TextInput(label="Tax", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)




    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country, email FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country, email = user_details

            link = self.Link.value
            shipping = float(self.shipping.value)
            tax = float(self.tax.value)
            currency = self.currency.value
            size = self.size.value






            

            if not is_dior_link(link):
                embed = discord.Embed(title="Error - Invalid Dior link", description="Please provide a valid Dior link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/dior.html", "r", encoding="utf-8") as file:
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
                    print(f"[{Colors.green}START Scraping{lg}] Dior -> {interaction.user.id} ({interaction.user})" + lg)


                    product_name = soup.find('meta', {'property': 'og:title'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)

                    img_src = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {img_src}" + lg)


                    match = re.search(r'var dataLayerWithUemail = (\[.*?\]);', response.text)
                    if match:
                        # Parsing the JSON data
                        json_data = json.loads(match.group(1))
                        view_item_data = next((item for item in json_data if item.get('event') == 'view_item'), None)
                        if view_item_data:
                            value = view_item_data['ecommerce']['value']
                            item_variant = view_item_data['ecommerce']['items'][0]['item_variant']


                            print(f"    [{Colors.cyan}Scraping{lg}] Price: {value}" + lg)
                            print(f"    [{Colors.cyan}Scraping{lg}] Color: {item_variant}" + lg)
                        else:
                            print("View item event not found.")


                    print(f"[{Colors.green}Scraping DONE{lg}] Dior -> {interaction.user.id}" + lg)
                    print()



                def generate_order_number():
                    return str(random.randint(100000000, 999999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

                # Bestellnummer generieren
                order_number = generate_order_number()

                fulltotal = shipping + tax + float(value)
                fulltotal = round(fulltotal, 2)

                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{ordernumber}", order_number)


                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{imageurl}", img_src)
                html_content = html_content.replace("{total}", str(fulltotal))
                html_content = html_content.replace("{email}", email)
                html_content = html_content.replace("{price}", str(value))
                html_content = html_content.replace("{size}", size)
                html_content = html_content.replace("{shipping}", str(shipping))
                html_content = html_content.replace("{tax}", str(tax))
                html_content = html_content.replace("{currency}", currency)












                with open("receipt/updatedrecipies/updateddior.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "Dior <noreply@dior.org>"
                subject = f"Your order confirmation"

                from emails.choise import choiseView
                owner_id = interaction.user.id
                img = "None"

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, img, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



       