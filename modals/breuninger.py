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



def is_breuninger_link(link):
    breuninger_pattern = re.compile(r'^https?://(www\.)?breuninger\.com/.+')

    return bool(breuninger_pattern.match(link))


class breuningermodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="breuninger.com link", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790,00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    colorr = discord.ui.TextInput(label="Color", placeholder="SCHWARZ", required=False)
    sizee = discord.ui.TextInput(label="Size", placeholder="XS / 100ml", required=False)



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
            

            if not is_breuninger_link(Link):
                embed = discord.Embed(title="Error - Invalid Breuninger link", description="Please provide a valid Breuninger link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            
            try:

                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)

                



                with open("receipt/breuninger.html", "r", encoding="utf-8") as file:
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
                    print(f"[{Colors.green}START Scraping{lg}] BREUNINGER-> {interaction.user.id} ({interaction.user})" + lg)


                    meta_tag = soup.find('meta', {'property': 'og:product:brand'})
                    if meta_tag and 'content' in meta_tag.attrs:
                        product_brand = meta_tag['content']
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Brand: {product_brand}" + lg)

                
                    productdesc = soup.find('span', class_='bewerten-zusammenfassung__name')
                    if productdesc:
                        product_desc = productdesc.text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Brand: {product_desc}" + lg)


                    image_url = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] BREUNINGER -> {interaction.user.id}" + lg)
                    print()



                    
                zipcity = f"{city} {zipp}"
                sizee = str(self.sizee.value)
                colorr = str(self.colorr.value)


                def generate_order_number():
                    return str(random.randint(10000000, 99999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

                # Bestellnummer generieren
                order_number = generate_order_number()
                



                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{zipcity}", zipcity)
                html_content = html_content.replace("{brandname}", product_brand)
                html_content = html_content.replace("{branddesc}", product_desc)
                html_content = html_content.replace("{sizee}", sizee)
                html_content = html_content.replace("{colorr}", colorr)
                html_content = html_content.replace("{imageurl}", image_url)
                html_content = html_content.replace("{price}", Price)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{rndordernumber}", order_number)

                

                with open("receipt/updatedrecipies/updatebreuninger.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "Breuninger Online-Shop <noreply@breuninger.org>"
                subject = f"Ihre Rechnung zur Bestellung {order_number}"
                from emails.choise import choiseView

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_desc, image_url, Link)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)



        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        