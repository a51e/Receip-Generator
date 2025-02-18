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




class grailedmodal(ui.Modal, title="discord.gg/maison"):
    brand = discord.ui.TextInput(label="Brand", placeholder="Nudie Jeans", required=True)
    productname = discord.ui.TextInput(label="Product Name", placeholder="Distressed Vintage Nudie Jeans Light Washed Denim Pants", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (Disord Image)", placeholder="https://cdn.discordapp.com/attachments/...", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="M", required=False)



    async def on_submit(self, interaction: discord.Interaction):
        global name, street, city, zipp, country, brand, productname, imageurl, size
        from addons.nextsteps import NextstepGrailed
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            brand = self.brand.value
            productname = self.productname.value
            imageurl = self.imageurl.value
            size = self.size.value


            
            embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receip.")
            await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=NextstepGrailed(owner_id))

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)






class grailedmodal2(ui.Modal, title="Grailed Receipt"):
    price = discord.ui.TextInput(label="Price without currency", placeholder="72.00", required=True)
    tax = discord.ui.TextInput(label="Tax", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)




    async def on_submit(self, interaction: discord.Interaction):
        global name, street, city, zipp, country, brand, productname, imageurl, size
        owner_id = interaction.user.id 

        try:

            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(embed=embed, view=None)

            



            with open("receipt/grailed.html", "r", encoding="utf-8") as file:
                html_content = file.read()



            price = float(self.price.value)
            tax = float(self.tax.value)
            currency = self.currency.value




                    


            fulltotal = tax + price
            fulltotal = round(fulltotal, 2)


            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{city}", city)
            html_content = html_content.replace("{zip}", zipp)
            html_content = html_content.replace("{country}", country)
            html_content = html_content.replace("{total}", str(fulltotal))
            html_content = html_content.replace("{brand}", brand)
            html_content = html_content.replace("{product}", productname)
            html_content = html_content.replace("{imageurl}", imageurl)
            html_content = html_content.replace("{size}", size)
            html_content = html_content.replace("{price}", str(price))
            html_content = html_content.replace("{tax}", str(tax))
            html_content = html_content.replace("{currency}", currency)













            

            with open("receipt/updatedrecipies/updatedgrailed.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            from emails.choise import choiseView
            sender_email = "Grailed   <orders@grailed.com>"
            subject = f"Congrats on your purchase!"
            link = "https://grailed.com/"

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, productname, imageurl, link)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
