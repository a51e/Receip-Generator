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



def is_adidas_link(link):
    adidas_pattern = re.compile(r'^https?://(www\.)?adidas\.com/.+')

    return bool(adidas_pattern.match(link))


class adidasmodal(ui.Modal, title="Adidas Receipt"):
    link = discord.ui.TextInput(label="Link", placeholder="https://adidas.com/....", required=True)
    pname = discord.ui.TextInput(label="Product Name", placeholder="Adidas Roadstar", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="190.00", required=True)
    tax = discord.ui.TextInput(label="Tax Costs", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)



    async def on_submit(self, interaction: discord.Interaction):
        global Price, currency, name, street , city, zipp, country, tax, link, pname
        from addons.nextsteps import NextstepAdidas
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
            tax = float(self.tax.value)
            link = self.link.value
            pname = self.pname.value


            from addons.nextsteps import NextstepAcne  # Ensure this import is handled if needed at the top or correctly here

            embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receipt.")
            await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed, view=NextstepAdidas(owner_id))
        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)




class adidasmodal2(ui.Modal, title="Adidas Receipt"):
    pcode = discord.ui.TextInput(label="Product Code", placeholder="JQ5111", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="M", required=True)




    async def on_submit(self, interaction: discord.Interaction):
        global Price, currency, name, street , city, zipp, country, tax, link
        owner_id = interaction.user.id 

        try:
                
            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(embed=embed, view=None)

            



            with open("receipt/adidas.html", "r", encoding="utf-8") as file:
                html_content = file.read()



            pcode = self.pcode.value
            size = self.size.value
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
                print(f"[{Colors.green}START Scraping{lg}] Adidas-> {interaction.user.id} ({interaction.user})" + lg)


                color = soup.find('div', class_='color-label___2hXaD')
                if color:
                    colorr = color.text.strip()
                    print(f"    [{Colors.cyan}Scraping{lg}] Color: {colorr}" + lg)


                image_url = soup.find('meta', {'property': 'og:image'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] Adidas -> {interaction.user.id}" + lg)
                print()






                    


            fulltotal =  tax + Price
            fulltotal = round(fulltotal, 2)

            def generate_order_number():
                return str(random.randint(1000000000, 9999999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

            # Bestellnummer generieren
            order_number = generate_order_number()


            html_content = html_content.replace("{ordernumber}", order_number)
            html_content = html_content.replace("{pname}", pname)
            html_content = html_content.replace("{price}", str(Price))
            html_content = html_content.replace("{tax}", str(tax))
            html_content = html_content.replace("{total}", str(fulltotal))
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{color}", colorr)
            html_content = html_content.replace("{size}", size)
            html_content = html_content.replace("{articelno}", pcode)
            html_content = html_content.replace("{imageurl}", image_url)
            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{city}", city)
            html_content = html_content.replace("{zip}", zipp)
            html_content = html_content.replace("{country}", country)

            

            with open("receipt/updatedrecipies/updatedadidas.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            from emails.choise import choiseView
            sender_email = "adidas CONFIRMED <noreply@adidas.org>"
            subject = f"Order: CONFIRMED"

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, pname, image_url, link)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
