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




def is_balenciaga_link(link):
    balenciaga_pattern = re.compile(r'^https?://(www\.)?balenciaga\.com/.+')

    return bool(balenciaga_pattern.match(link))


class balenciagamodal(ui.Modal, title="discord.gg/maison"):
    Linkbalenciaga = discord.ui.TextInput(label="Link", placeholder="Balenciaga.com link", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="790", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details


            Link = self.Linkbalenciaga.value
            currency = self.currency.value
            Price = self.Price.value
            cityzip = f"{city} {zipp}"

            if not is_balenciaga_link(Link):
                embed = discord.Embed(title="Error - Invalid Balenciaga link", description="Please provide a valid Balenciaga link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            
            try:
                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)


                with open("receipt/balenciaga.html", "r", encoding="utf-8") as file:
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
                    print(f"[{Colors.green}START Scraping{lg}] BALENCIAGA -> {interaction.user.id} ({interaction.user})" + lg)




                    productname = None
                    image_src = None
                    color = None






                    image_html = soup.find('div', {'class': 'c-productcarousel'})

                    if image_html:
                        image_html1 = image_html.find('button', {'class': 'c-productcarousel__button'})

                        if image_html1:
                            image_element = image_html1.find('img', {'data-src': True})
                            
                            if image_element:
                                image_src = image_element['data-src']

                                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_src}" + lg)





                    color_values = []


                    color_wrapper = soup.find('div', {'class': 'c-swatches__scroller'})
                    if color_wrapper:
                        color_element = color_wrapper.find('span', {'class': 'color-value c-swatches__itemimage selected'})
                        
                        if color_element:
                            color_value = color_element['data-display-value']
                            color_values.append(color_value)


                            print(f"    [{Colors.cyan}Scraping{lg}] Color: {color_values[0]}" + lg)

                    print(f"[{Colors.green}Scraping DONE{lg}] BALENCIAGA -> {interaction.user.id}" + lg)
                    print()




                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{country}", country)

                html_content = html_content.replace("{pimage}", str(image_src))

                html_content = html_content.replace("{pname}", str(productname))
                html_content = html_content.replace("{color}", str(color_values[0]))


                html_content = html_content.replace("{currency}", currency) 
                html_content = html_content.replace("{total}", Price)
                

                with open("receipt/updatedrecipies/updatedbalenciaga.html", "w", encoding="utf-8") as file:
                    file.write(html_content)

                image = str(image_src)


                sender_email = "Balenciaga <noreply@balenciaga.org>"
                subject = "Your Balenciaga Order Registration"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, productname, image, Link)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)



        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


        