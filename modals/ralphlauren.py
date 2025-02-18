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





def is_rl_link(link):
    rl_pattern = re.compile(r'^https?://(www\.)?ralphlauren\.co\.uk(/.*)?$')

    return bool(rl_pattern.match(link))


class ralphlaurenmodal(ui.Modal, title="discord.gg/maison"):
    Linkff = discord.ui.TextInput(label="Link", placeholder="ralphlauren.co.uk/en link", required=True)
    Priceff = discord.ui.TextInput(label="Price without currency", placeholder="Ex. 790", required=True)
    currencyff = discord.ui.TextInput(label="Currency ($, £‚ €)", placeholder="€", required=True, min_length=1, max_length=2)
    delivery = discord.ui.TextInput(label="Delivery Date", placeholder="Ex. 24/04/2024", required=True)
    Size = discord.ui.TextInput(label="Size", placeholder="Ex. UK 36", required=True)


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
            delivery = self.delivery.value


            if not is_rl_link(Linkff):
                embed = discord.Embed(title="Error - Invalid Ralph Lauren link", description="Please provide a valid Ralph Lauren link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            

            try:
                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)



                with open("receipt/ralphlauren.html", "r", encoding="utf-8") as file:
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
                color = None
                styleid = None
                image_url = None


                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] RALPH LAUREN -> {interaction.user.id} ({interaction.user})" + lg)



                    pname = soup.find('div', {'class': 'product-favorite-cont'})
                    if pname:
                        product_name = pname.find('h1', {'class': 'product-name'}).text.strip()
                        print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)



                    colour = soup.find('div', {'class': 'attribute-top-links'})
                    if colour:
                        color_element = colour.find('span', {'class': 'js-selected-value-wrapper selected-value select-attribute selected-color'})
                        if color_element:
                            color = color_element.text.strip()
                            print(f"    [{Colors.cyan}Scraping{lg}] Color: {color}" + lg)


                    style = soup.find('div', {'class': 'bullet-list'})
                    if style:
                        styleid_element = style.find('span', {'class': 'screen-reader-digits'})
                        if styleid_element:
                            styleid = styleid_element.text.strip()
                            print(f"    [{Colors.cyan}Scraping{lg}] Style ID: {styleid}" + lg)


                    source_element = soup.find('source')
                    if source_element and 'srcset' in source_element.attrs:
                        image_url = source_element['srcset'].split(',')[0].split()[0]
                        print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
                    if not image_url:
                        img_element = soup.find('img')
                        if img_element and 'data-img' in img_element.attrs:
                            image_url = img_element['data-img']
                            print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] RALPH LAUREN -> {interaction.user.id}" + lg)
                    print()



                cityzip = f"{city} {zipp}"

                size = self.Size.value


                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{land}", country)
                html_content = html_content.replace("{ddate}", delivery)
                html_content = html_content.replace("{price}", Priceff) 
                html_content = html_content.replace("{currency}", currencyff) 
                html_content = html_content.replace("{plink}", str(image_url))
                html_content = html_content.replace("{productname}", str(product_name))
                html_content = html_content.replace("{color}", str(color))
                html_content = html_content.replace("{size}", size)
                html_content = html_content.replace("{link}", str(Linkff))
                html_content = html_content.replace("{styleid}", str(styleid))
                html_content = html_content.replace("{currency}", str(currencyff)) 
                

                with open("receipt/updatedrecipies/updatedralphlauren.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "Ralph Lauren Customer Assistance <noreply@ralphlauren.co.uk>"
                subject = "Your Ralph Lauren Order 5692986853"
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



    



    