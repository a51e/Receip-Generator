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





def is_dyson_link(link):
    dyson_link_pattern = re.compile(r'^https?://(www\.)?dyson\.[a-z]{2,3}(/.*)?$')
    return bool(dyson_link_pattern.match(link))


class dyson(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="Dyson link", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="1693", required=True)

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
            currency = self.currency.value
            price = self.price.value
            

            if not is_dyson_link(link):
                embed = discord.Embed(title="Error - Invalid Dyson link", description="Please provide a valid Dyson link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/dyson.html", "r", encoding="utf-8") as file:
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



                product_name = "None"
                image_src = "None"

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] DYSON -> {interaction.user.id} ({interaction.user})" + lg)



                    product_name_element = soup.find('h1', class_='h3 product-hero__line1')
                    if product_name_element:
                        product_name = product_name_element.text.strip()
                    else:
                        product_name_element = soup.find('h1', class_='h4 product-hero__line1')
                        if product_name_element:
                            product_name = product_name_element.text.strip()
                        else:
                            product_name_element = soup.find('h1', class_='h5 product-hero__line1')
                            if product_name_element:
                                product_name = product_name_element.text.strip()
                            else:
                                product_name_element = soup.find('h1', class_='h2 product-hero__line1')
                                if product_name_element:
                                    product_name = product_name_element.text.strip()
                                else:
                                    product_name_element = soup.find('h2', class_='h3 product-hero__line1')
                                    if product_name_element:
                                        product_name = product_name_element.text.strip()
                                    else:
                                        product_name_element = soup.find('h2', class_='h4 product-hero__line1')
                                        if product_name_element:
                                            product_name = product_name_element.text.strip()
                                        else:
                                            product_name_element = soup.find('h2', class_='h5 product-hero__line1')
                                            if product_name_element:
                                                product_name = product_name_element.text.strip()
                                            else:
                                                product_name_element = soup.find('h2', class_='h2 product-hero__line1')
                                                if product_name_element:
                                                    product_name = product_name_element.text.strip()



                    # Bild-URL extrahieren
                    image_html = soup.find('div', {'class': 'responsive-image js-responsive-image-container'})
                    if image_html:
                        img_tag = image_html.find('img')
                        if img_tag and 'data-src' in img_tag.attrs:
                            image_src = img_tag['data-src']
                        else:
                            image_src = "Image URL not found"
                    else:
                        image_src = "Image container not found"


                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_src}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] DYSON -> {interaction.user.id}" + lg)
                    print()





                cityzip = f"{city} {zipp}"




                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{price}", price)
                html_content = html_content.replace("{imageurl}", image_src)





                with open("receipt/updatedrecipies/updateddyson.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Dyson <b2bservice@dyson.com>"
                subject = f"Your Dyson order confirmation 5089915074"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_src, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

