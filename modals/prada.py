import asyncio
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





def is_prada_link(link):
    prada_pattern = re.compile(r'^https?://www.prada.com/.+$')

    return bool(prada_pattern.match(link))


class Pradamodal(ui.Modal, title="discord.gg/maison"):
    Linkff = discord.ui.TextInput(label="Link", placeholder="Prada.com Link", required=True)
    Priceff = discord.ui.TextInput(label="Price without currency", placeholder="Ex. 790", required=True)
    currencyff = discord.ui.TextInput(label="Currency ($, £‚ €)", placeholder="€", required=True, min_length=1, max_length=2)
    color = discord.ui.TextInput(label="Color", placeholder="Black", required=True)
    Size = discord.ui.TextInput(label="Size", placeholder="If no size do (One Size)", required=True)



    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            Linkff = self.Linkff.value
            currencyff = self.currencyff.value
            Priceff = self.Priceff.value
            color = self.color.value



            if not is_prada_link(Linkff):
                embed = discord.Embed(title="Error - Invalid Prada link", description="Please provide a valid Prada link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            
            try:
                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)



                with open("receipt/prada.html", "r", encoding="utf-8") as file:
                    html_content = file.read()



                url = Linkff

                response = requests.get(
                    url=url,
                    proxies={
                        "http": "http://c75647e5bd0e425db76b57feebf89590:@api.zyte.com:8011/",
                        "https": "http://c75647e5bd0e425db76b57feebf89590:@api.zyte.com:8011/",
                    },
                    verify='zyte-ca.crt' 
                )



                product_name = None
                image_url = None

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] PRADA -> {interaction.user.id} ({interaction.user})" + lg)


                    product_name_element = soup.find('h1', class_='text-title-big')
                    if product_name_element:
                        product_name = product_name_element.text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)


                    img_tag = soup.find('picture', class_='').find('img')
                    if img_tag:
                        srcset_attribute = img_tag.get('srcset')
                        if srcset_attribute:
                            srcset_urls = srcset_attribute.split(',')
                            image_url = srcset_urls[0].strip().split(' ')[0]
                            print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
 

                    
                    ul_tag = soup.find('ul', class_='ml-sp-26 list-disc text-paragraph-medium lg:text-h3 font-normal')
                    if ul_tag:
                        product_code_li = ul_tag.find('li')
                        if product_code_li:
                            product_text = product_code_li.text.strip()
                            # Splitten des Textes am Doppelpunkt und Entfernen von zusätzlichem Leerzeichen
                            parts = product_text.split(':')
                            if len(parts) > 1:  # Sicherstellen, dass ein Doppelpunkt vorhanden ist
                                productcode = parts[1].strip()  # Extrahieren und Trimmen des Textes nach dem Doppelpunkt
                                print(f"    [Scraping] Product code: {productcode}")

                    print(f"[{Colors.green}Scraping DONE{lg}] PRADA -> {interaction.user.id}" + lg)
                    print()


                size = self.Size.value
    



                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{size}", size)
                html_content = html_content.replace("{currency}", str(currencyff))
                html_content = html_content.replace("{price}", str(Priceff))
                html_content = html_content.replace("{imageurl}", str(image_url))
                html_content = html_content.replace("{productname}", str(product_name))
                html_content = html_content.replace("{color}", str(color))
                html_content = html_content.replace("{productcode}", str(productcode))
                

                with open("receipt/updatedrecipies/updatedprada.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Prada <client.service@prada.com>"
                subject = "Prada - Order acknowledgement - GBPR5247077561738"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, Linkff)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)   
            
        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

