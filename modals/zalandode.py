import asyncio
import json
import locale
import random
import re
import webbrowser
import discord
from discord.ui import Select
from discord import SelectOption, ui, app_commands

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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from datetime import datetime, timedelta



from bs4 import BeautifulSoup

from pystyle import Colors


r = Colors.red
lg = Colors.light_gray



def is_zalando_link(link):
    zalando_pattern = re.compile(r'^https?://(www\.)?zalando\.de(/.+)?')


    return bool(zalando_pattern.match(link))


class zalandodemodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="zalando.de link", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790,00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    orderdate2 = discord.ui.TextInput(label="Orderdate", placeholder="Mo., 09.12.2024", required=True)
    sizee = discord.ui.TextInput(label="Size", placeholder="XL", required=True)


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
            orderdate2 = self.orderdate2.value
            Price = self.Price.value
            currency = str(self.currency.value)
            

            if not is_zalando_link(Link):
                embed = discord.Embed(title="Error - Invalid Zalando link", description="Please provide a valid Zalando link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            
            try:

                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)

                



                with open("receipt/zalandode.html", "r", encoding="utf-8") as file:
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
                    print(f"[{Colors.green}START Scraping{lg}] ZALANDO DE -> {interaction.user.id} ({interaction.user})" + lg)

                    brand_name = None
                    product_name = None
                    image_url = None


                    brand_name_element = soup.find('div', class_='XKeLfu lm1Id5')
                    if brand_name_element:
                        brand_name = brand_name_element.text.strip()
                    else:
                        brand_name_element = soup.find('span', class_='OBkCPz Z82GLX m3OCL3 HlZ_Tf _5Yd-hZ')
                        if brand_name_element:
                            brand_name = brand_name_element.text.strip()


                    product_name_element = soup.find('span', class_='EKabf7 R_QwOV')
                    if product_name_element:
                        product_name = product_name_element.text.strip()


                    image_url = soup.find('meta', {'property': 'og:image'})['content']
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Brand Name: {brand_name}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)

                    print(f"[{Colors.green}Scraping DONE{lg}] ZALANDO DE -> {interaction.user.id}" + lg)
                    print()


                        

                    

                zipcity = f"{city} {zipp}"
                sizee = str(self.sizee.value)
                
                locale.setlocale(locale.LC_TIME, 'de_DE.utf8')

                order_date_str = orderdate2.split(",")[1].strip()
                order_date = datetime.strptime(order_date_str, "%d.%m.%Y")
                delivery_date = order_date + timedelta(days=1)  # 1 Tag später
                tddelivery_date = order_date + timedelta(days=3)  # 3 Tage später

                formatted_delivery_date = delivery_date.strftime("%a., %d.%m.%Y")  # Di., 10.12.2024
                formatted_tddelivery_date = tddelivery_date.strftime("%a., %d.%m.%Y")  # Do., 12.12.2024


                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{link}", Link)
                html_content = html_content.replace("{orderdate}", orderdate2)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{zipcity}", zipcity)
                html_content = html_content.replace("{imageurl}", image_url)
                html_content = html_content.replace("{Brand}", brand_name)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{sizee}", sizee)
                html_content = html_content.replace("{price}", Price)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{deliverydate}", formatted_delivery_date)
                html_content = html_content.replace("{tddeliverydate}", formatted_tddelivery_date)


                

                with open("receipt/updatedrecipies/updatedzalandode.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Zalando Team <noreply@zalando.com>"
                subject = f"Danke für deine Bestellung"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, Link)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

