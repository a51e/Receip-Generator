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





class chronomodal(ui.Modal, title="discord.gg/maison"):
    pname = discord.ui.TextInput(label="Product Name", placeholder="Rolex Datejust", required=True)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="199.99", required=True)
    sellername = discord.ui.TextInput(label="Sellername", placeholder="Albert", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (Discord Image)", placeholder="https://cdn.discordapp.com/attachments/...", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 


        pname = self.pname.value
        price = self.price.value
        sellername = self.sellername.value
        imageurl = self.imageurl.value
        currency = self.currency.value


        
        try:


            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


            with open("receipt/chrono24.html", "r", encoding="utf-8") as file:
                html_content = file.read()


            html_content = html_content.replace("{pname}", pname)
            html_content = html_content.replace("{price}", price)
            html_content = html_content.replace("{sellername}", sellername)
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{imageurl}", imageurl)







            with open("receipt/updatedrecipies/updatedchrono.html", "w", encoding="utf-8") as file:
                file.write(html_content)



            sender_email = "Chrono24 <order@chrono24.com>"
            subject = f"Your watch has been shipped (TC-9856274702)"

            from emails.choise import choiseView
            owner_id = interaction.user.id
            link = "https://chrono24.com"


                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, pname, imageurl, link)
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
