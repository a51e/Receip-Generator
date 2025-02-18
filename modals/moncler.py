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
from uuid import uuid4  # gen random guid


from urllib.parse import urlparse, parse_qs
import datetime

import requests



import sys
import time
import platform
import os
import hashlib
from time import sleep
import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



from bs4 import BeautifulSoup
from pystyle import Colors

r = Colors.red
lg = Colors.light_gray


def is_moncler_link(link):
    moncler_link_pattern = re.compile(r'^https?://www\.moncler\.com/.+$')
    return bool(moncler_link_pattern.match(link))


class monclermodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="Moncler link", required=True)
    Size = discord.ui.TextInput(label="Size (1, 2, 3)", placeholder="Ex. 1", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    orderdate = discord.ui.TextInput(label="Order Date", placeholder="Ex. 23 January 2024", required=True)

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
            size = self.Size.value
            price = self.Price.value
            orderdate = self.orderdate.value
            currency = self.currency.value

            if not is_moncler_link(link):
                embed = discord.Embed(title="Error - Invalid Moncler link", description="Please provide a valid Moncler link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            try:
                owner_id = interaction.user.id 

                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                cityzip = f"{city} {zipp}"

                

                orderdate = orderdate.strip()
                
                # Attempt to parse the date
                ddate_datetime = datetime.datetime.strptime(orderdate, "%d %B %Y")
                new_ddate_datetime = ddate_datetime + datetime.timedelta(days=7)
                estdeliveryy = new_ddate_datetime.strftime("%d %B %Y")


                with open("receipt/moncler.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

                url = link

                api_response = requests.post(
                    "https://api.zyte.com/v1/extract",
                    auth=("c75647e5bd0e425db76b57feebf89590", ""),
                    json={
                        "url": url,
                        "browserHtml": True,
                        "product": True,
                        "productOptions": {"extractFrom": "browserHtml"},
                    },
                )



                browser_html = api_response.json()["browserHtml"]
                soup = BeautifulSoup(browser_html, 'html.parser')
                print()
                print(f"[{Colors.green}START Scraping{lg}] MONCLER -> {interaction.user.id} ({interaction.user})" + lg)



                json_ld_script = soup.find('script', type='application/ld+json', attrs={'data-react-helmet': 'true'})
                if json_ld_script:
                    product_data = json.loads(json_ld_script.string)
                    


                    product_name = product_data.get('name', 'Product Name not found') 
                    image_url = product_data.get('image', ['Image URL not found'])[0] 

                    color = 'Black'
                    if 'hasVariant' in product_data:
                        for variant in product_data['hasVariant']:
                            if 'color' in variant:
                                color = variant['color']
                                break 


                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Color: {color}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] MONCLER -> {interaction.user.id}" + lg)
                print()



                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{sizee}", size)
                html_content = html_content.replace("{orderdate}", orderdate)
                html_content = html_content.replace("{estdelivery}", estdeliveryy)

                html_content = html_content.replace("{color}", str(color))
                html_content = html_content.replace("{imageurl}", str(image_url))

                html_content = html_content.replace("{pname}", str(product_name))       
                html_content = html_content.replace("{currency}", currency) 
                html_content = html_content.replace("{price}", price)


                with open("receipt/updatedrecipies/updatedmoncler.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Moncler Online Store <orders@moncler.com>"
                subject = f"Thank you for your order"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



