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



def is_zara_link(link):
    zara_pattern = re.compile(r'^https?://(www\.)?zara\.com(/.+)?')


    return bool(zara_pattern.match(link))


class zaramodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="zara.com link", required=True)
    Price = discord.ui.TextInput(label="Price without currency", placeholder="49.50", required=True)
    currency = discord.ui.TextInput(label="Currency Code (EUR, USD)", placeholder="EUR", required=True, min_length=1, max_length=3)
    deliverydate = discord.ui.TextInput(label="Orderdate", placeholder="FREITAG, 18. OKTOBER", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        global Link , Price, currency, deliverydate
        from addons.nextsteps import Nextstepzara
        owner_id = interaction.user.id 


        Link = self.Link.value
        deliverydate = self.deliverydate.value
        Price = float(self.Price.value)
        currency = self.currency.value
        

        if not is_zara_link(Link):
            embed = discord.Embed(title="Error - Invalid Zara link", description="Please provide a valid Zara link.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        
        embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receip.")
        await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=Nextstepzara(owner_id))





class zaramodal2(ui.Modal, title="Zara Receipt"):
    Street = discord.ui.TextInput(label="Street", placeholder="Musterstraße 12", required=True)
    zipcity = discord.ui.TextInput(label="Zip Code with City", placeholder="Berlin 10115", required=True)
    state = discord.ui.TextInput(label="State", placeholder="NORDRHEIN-WESTFALEN", required=True)
    country = discord.ui.TextInput(label="Country", placeholder="DEUTSCHLAND", required=True)
    sizee = discord.ui.TextInput(label="Size", placeholder="M")


    async def on_submit(self, interaction: discord.Interaction):
        global Link , Price, currency, deliverydate
        owner_id = interaction.user.id 

        try:

            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(content=None,embed=embed, view=None)

            



            with open("receipt/zara.html", "r", encoding="utf-8") as file:
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
                print(f"[{Colors.green}START Scraping{lg}] ZARA -> {interaction.user.id} ({interaction.user})" + lg)

                color_name = "None"
                product_name = "None"
                image_url = "None"


                image_url = soup.find('meta', {'property': 'og:image'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)

                product_name = soup.find('meta', {'property': 'og:title'})['content']
                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)


                color_name = "None"
                color_name_element = soup.find('p', class_='product-color-extended-name product-detail-color-selector__selected-color-name')
                if color_name_element:
                    color_name = color_name_element.text.strip()
                else:
                    color_name_element = soup.find('p', class_='product-color-extended-name product-detail-info__color')
                    if color_name_element:
                        color_name = color_name_element.text.strip()

                if color_name:
                    color_name = re.sub(r'^Farbe:\s*', '', color_name)
                    print(f"    [{Colors.cyan}Scraping{lg}] Color: {color_name}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] ZARA -> {interaction.user.id}" + lg)
                print()





                    

                
            street = str(self.Street.value)
            zipcity = str(self.zipcity.value)
            state = str(self.state.value)
            country = str(self.country.value)
            sizee = str(self.sizee.value)
            
            tax = float("5.49")

            total = Price + tax
            total = round(total, 2)




            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{zipcity}", zipcity)
            html_content = html_content.replace("{state}", state)
            html_content = html_content.replace("{country}", country)
            html_content = html_content.replace("{imageurl}", image_url)
            html_content = html_content.replace("{pname}", product_name)
            html_content = html_content.replace("{coloridcode}", color_name)
            html_content = html_content.replace("{price}", str(Price))
            html_content = html_content.replace("{total}", str(total))
            html_content = html_content.replace("{size}", sizee)


            html_content = html_content.replace("{currencycode}", currency)
            html_content = html_content.replace("{deliverydate}", deliverydate)






            

            with open("receipt/updatedrecipies/updatedzara.html", "w", encoding="utf-8") as file:
                file.write(html_content)


            sender_email = "Zara <noreply@zara.com>"
            subject = f"Vielen Dank für Ihren Einkauf"
            from emails.choise import choiseView
            owner_id = interaction.user.id

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, Link)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)
