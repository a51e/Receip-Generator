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



def is_acne_link(link):
    acne_pattern = re.compile(r'^https?://(www\.)?acnestudios\.com/.+')

    return bool(acne_pattern.match(link))


class acnemodal(ui.Modal, title="discord.gg/maison"):
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790.00", required=True)
    shipping = discord.ui.TextInput(label="Shipping Costs", placeholder="10.00", required=True)
    tax = discord.ui.TextInput(label="Tax Costs", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    orderdate = discord.ui.TextInput(label="Orderdate (DD/MM/YY)", placeholder="9/10/2024", required=True)



    async def on_submit(self, interaction: discord.Interaction):
        global Price, currency, name, orderdate, street , city, zipp, country, tax, shipping
        from addons.nextsteps import NextstepAcne
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
            orderdate = self.orderdate.value
            tax = float(self.tax.value)
            shipping = float(self.shipping.value)

            from addons.nextsteps import NextstepAcne  # Ensure this import is handled if needed at the top or correctly here

            embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receipt.")
            await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed, view=NextstepAcne(owner_id))
        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



class acnemodal2(ui.Modal, title="Acnestudios Receipt"):
    pname = discord.ui.TextInput(label="Product Name", placeholder="Hooded zipper sweater", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="M", required=True)



    async def on_submit(self, interaction: discord.Interaction):
        global Price, currency, name, orderdate, street , city, zipp, country, tax, shipping
        owner_id = interaction.user.id 

        try:

            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(embed=embed, view=None)

            



            with open("receipt/acnestudios.html", "r", encoding="utf-8") as file:
                html_content = file.read()



            product_name = self.pname.value
            size = self.size.value


            print()
            print(f"[{Colors.green}START Scraping{lg}] acnestudios -> {interaction.user.id} ({interaction.user})" + lg)
            print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
            print(f"[{Colors.green}Scraping DONE{lg}] acnestudios -> {interaction.user.id} ({interaction.user})" + lg)
            print()






                    


            fulltotal = shipping + tax + Price
            fulltotal = round(fulltotal, 2)

            def generate_order_number():
                return str(random.randint(1000000000, 9999999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

            # Bestellnummer generieren
            order_number = generate_order_number()


            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{ordernumber}", order_number)
            html_content = html_content.replace("{orderdate}", orderdate)
            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{city}", city)
            html_content = html_content.replace("{zip}", zipp)
            html_content = html_content.replace("{country}", country)
            html_content = html_content.replace("{shipping}", str(shipping))
            html_content = html_content.replace("{tax}", str(tax))
            html_content = html_content.replace("{price}", str(Price))
            html_content = html_content.replace("{total}", str(fulltotal))
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{size}", size)
            html_content = html_content.replace("{pname}", product_name)
            

            with open("receipt/updatedrecipies/updatedacnestudios.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            from emails.choise import choiseView
            sender_email = "Acnestudios.com  <clientservices@acnestudios.com>"
            subject = f"New order {order_number}"
            link = "https://acnestudios.com/"
            image_url = "None"

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, link)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
