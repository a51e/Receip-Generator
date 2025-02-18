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





def is_ck_link(link):
    ck_link_pattern = re.compile(r'^https?://(www\.)?culturekings\.com/.*$')
    return bool(ck_link_pattern.match(link))


class ckmodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="https://culturekings.com/...", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="S", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 



        link = self.Link.value
        size = self.size.value



        

        if not is_ck_link(link):
            embed = discord.Embed(title="Error - Invalid Culturekings link", description="Please provide a valid Culturekings link.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return


        
        try:


            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


            with open("receipt/culturekings.html", "r", encoding="utf-8") as file:
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
                print(f"[{Colors.green}START Scraping{lg}] Culturekings -> {interaction.user.id} ({interaction.user})" + lg)

                product_name = soup.find('meta', {'property': 'og:title'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)

                img_src = soup.find('meta', {'property': 'og:image'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {img_src}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] Culturekings -> {interaction.user.id}" + lg)
                print()



            def generate_order_number():
                return str(random.randint(1000000000, 9999999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

            # Bestellnummer generieren
            order_number = generate_order_number()




            html_content = html_content.replace("{deliverydate}", size)
            html_content = html_content.replace("{ordernumber}", order_number)
            html_content = html_content.replace("{pname}", product_name)
            html_content = html_content.replace("{imageurl}", img_src)





            with open("receipt/updatedrecipies/updatedcoolblue.html", "w", encoding="utf-8") as file:
                file.write(html_content)



            sender_email = "CultureKings <noreply@culutrekings.com>"
            subject = f"Your order from CultureKings has been confirmed."

            from emails.choise import choiseView
            owner_id = interaction.user.id

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, img_src, link)
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
