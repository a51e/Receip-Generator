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





def is_offwhite_link(link):
    cooblue_link_pattern = re.compile(r'^https?://(www\.)?off---white\.com/.*$')
    return bool(cooblue_link_pattern.match(link))


class offwhitemodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://off---white.com/...", required=True)
    price = discord.ui.TextInput(label="Price without currency", placeholder="275", required=True)
    shipping = discord.ui.TextInput(label="Shipping Costs", placeholder="10.00", required=True)
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
            price = float(self.price.value)
            shipping = float(self.shipping.value)
            currency = self.currency.value




            

            if not is_offwhite_link(link):
                embed = discord.Embed(title="Error - Invalid Off White link", description="Please provide a valid Off White link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/offwhite.html", "r", encoding="utf-8") as file:
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
                    print(f"[{Colors.green}START Scraping{lg}] offwhite -> {interaction.user.id} ({interaction.user})" + lg)

                    product_name = soup.find('meta', {'property': 'og:title'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)

                    img_src = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {img_src}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] offwhite -> {interaction.user.id}" + lg)
                    print()


                fulltotal =  shipping + price
                fulltotal = round(fulltotal, 2)


                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{imageur}", img_src)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{total}", fulltotal)
                html_content = html_content.replace("{price}", str(price))
                html_content = html_content.replace("{shipping}", str(shipping))
                html_content = html_content.replace("{currency}", currency)








                with open("receipt/updatedrecipies/updatedoffwhite.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "Off-White <noreply@off---white.com>"
                subject = f"Thank you for placing your order"

                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, img_src, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



    