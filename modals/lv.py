import asyncio
import json
import queue
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





class lvmodal(ui.Modal, title="discord.gg/maison"):
    Linklv = discord.ui.TextInput(label="Link", placeholder="Louis Vuitton EU link", required=True)
    Pricelv = discord.ui.TextInput(label="Price without currency", placeholder="1600", required=True)
    currencylv = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    imglink = discord.ui.TextInput(label="Image Link (Discord Img)", placeholder="https://cdn.discordapp.com/attachments/10869879156.....", required=True, min_length=1)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            Linklv = self.Linklv.value
            currencylv = self.currencylv.value
            Pricelv = self.Pricelv.value
            imglink = self.imglink.value

            
            try:

                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)

                with open("receipt/lv.html", "r", encoding="utf-8") as file:
                    html_content = file.read()
                

                url = Linklv

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
                    print(f"[{Colors.green}START Scraping{lg}] LOUIS VUITTON -> {interaction.user.id} ({interaction.user})" + lg)



                    pname = soup.find('div', {'class': 'lv-product__head'})
                    product_name = None  

                    if pname:
                        product_name = pname.find('h1', {'class': 'lv-product__name heading-s'}).text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)


                    reference = soup.find('div', {'class': 'lv-footer-breadcrumb lv-gutters'})
                    referencename = None  
                    if reference:
                        referencename = reference.find('li', {'class': 'lv-footer-breadcrumb__item'}).text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Reference: {referencename}" + lg)

                    
                    print(f"[{Colors.green}Scraping DONE{lg}] LOUIS VUITTON -> {interaction.user.id}" + lg)
                    print()

                    

                firstname = name
                cityzip = f"{city} {zipp}"


                html_content = html_content.replace("{fname}", firstname)
                html_content = html_content.replace("{fullname}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", cityzip)
                html_content = html_content.replace("{country}", country)

                html_content = html_content.replace("{pname}", str(product_name))
                html_content = html_content.replace("{pimage}", str(imglink))
                html_content = html_content.replace("{reference}", str(referencename))


                html_content = html_content.replace("{currency}", currencylv) 
                html_content = html_content.replace("{total}", str(Pricelv))
                

                with open("receipt/updatedrecipies/updatedlv.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Louis Vuitton <customer.service@louisvuitton.com>"
                subject = "Your Louis Vuitton Order Has been Shipped"

                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, imglink, Linklv)
                await interaction.edit_original_response(embed=embed, view=view)
                    
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



    