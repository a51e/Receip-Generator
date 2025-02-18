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





def is_chrome_link(link):
    chrome_link_pattern = re.compile(r'^https?://(www\.)?chromehearts\.[a-z]{2,3}(/.*)?$')
    return bool(chrome_link_pattern.match(link))


class chromemodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://chrommehearts.com/", required=True)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="300.00", required=True)
    tax = discord.ui.TextInput(label="Tax", placeholder="10.00", required=True)
    shipping = discord.ui.TextInput(label="Shipping", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 
        global link, name, currency, price, tax, shipping, message

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
            price = float(self.price.value)
            tax = float(self.tax.value)
            shipping = float(self.shipping.value)

            

            if not is_chrome_link(link):
                embed = discord.Embed(title="Error - Invalid Chromehearts link", description="Please provide a valid Chromehearts link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False
            
            from addons.nextsteps import NextstepChrome
            embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receip.")
            await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=NextstepChrome(owner_id))

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



    


        
        

class chromemodal2(ui.Modal, title="Chromhearts Receipt"):
    size = discord.ui.TextInput(label="Size", placeholder="XL", required=True)
    orderdate = discord.ui.TextInput(label="Order Date (DD/MM/YYYY)", placeholder="06/06/2024", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        global link, name, currency, price, tax, shipping
        try:
            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(content=f"{interaction.user.mention}", embed=embed, view=None)



            with open("receipt/chromehearts.html", "r", encoding="utf-8") as file:
                html_content = file.read()


            # Zyte API setup
            url = link  # Link should be defined or passed into the class


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
                print(f"[{Colors.green}START Scraping{lg}] Chromehearts -> {interaction.user.id} ({interaction.user})" + lg)


                product_name = soup.find('meta', {'property': 'og:title'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] Chromehearts -> {interaction.user.id}" + lg)
                print()




            size = self.size.value
            orderdate = self.orderdate.value




            fulltotal = shipping + tax + price
            fulltotal = round(fulltotal, 2)


            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{price}", str(price))
            html_content = html_content.replace("{tax}", str(tax))
            html_content = html_content.replace("{shipping}", str(shipping))
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{total}", str(fulltotal))
            html_content = html_content.replace("{pname}", product_name)
            html_content = html_content.replace("{size}", size)
            html_content = html_content.replace("{orderdate}", orderdate)




            with open("receipt/updatedrecipies/updatedchrome.html", "w", encoding="utf-8") as file:
                file.write(html_content)


            sender_email = "<orders@chromehearts.com>"
            subject = f"Chrome Hearts Receipt"
            from emails.choise import choiseView
            owner_id = interaction.user.id
            image_src = "None"


            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_src, link)
            await interaction.edit_original_response(embed=embed, view=view)


        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)






