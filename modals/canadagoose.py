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





def is_canadagoose_link(link):
    canadagoose_link_pattern = re.compile(r'^https?://(www\.)?canadagoose\.com/.*$')
    return bool(canadagoose_link_pattern.match(link))


class canadagoose(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="Canada Goose link", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    invoicedate = discord.ui.TextInput(label="Invoice Date", placeholder="Ex. 22/01/2024", required=True)
    sizee = discord.ui.TextInput(label="Size (If no size leave blank)", placeholder="US M", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        global name , currency, invoicedate, link, sizee, street, city, zipp, country
        from addons.nextsteps import Nextstepcg
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
            invoicedate = self.invoicedate.value
            sizee = self.sizee.value if self.sizee.value else ""
            

            if not is_canadagoose_link(link):
                embed = discord.Embed(title="Error - Invalid Canada Goose link", description="Please provide a valid Canada Goose link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receip.")
            await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=Nextstepcg(owner_id))

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


       






class canadagoose2(ui.Modal, title="Canada Goose Receipt"):
    
    price = discord.ui.TextInput(label="Price without Currency", placeholder="1693", required=True)
    color = discord.ui.TextInput(label="Color", placeholder="BLACK", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        global name , currency, invoicedate, link, sizee

        try:


            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(content=f"{interaction.user.mention}", embed=embed, view=None)


            with open("receipt/canadagoose.html", "r", encoding="utf-8") as file:
                html_content = file.read()


            # Zyte API setup
            url = link  # Link should be defined or passed into the class

            # Zyte API request
            api_response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=("80931067d89d459e9ce06652123794d9", ""),
                json={
                    "url": url,
                    "httpResponseBody": True,
                },
            )

            # Decode and parse Zyte API HTML response
            http_response_body = b64decode(api_response.json().get("httpResponseBody", "")).decode('utf-8')
            soup = BeautifulSoup(http_response_body, 'html.parser')

            # Extract gtmDataCG object from HTML
            pattern = r'gtmDataCG\s*=\s*(\{.*?\});'
            match = re.search(pattern, http_response_body, re.DOTALL)
            print()
            print(f"[{Colors.green}START Scraping{lg}] CANADA GOOSE -> {interaction.user.id} ({interaction.user})" + lg)

            if match:
                gtm_data = match.group(1)
                gtm_data = gtm_data.replace("window.location.href", '"URL"').replace("document.referrer", '"referrer"')
                gtm_data_json = json.loads(gtm_data)

                product_name = gtm_data_json["ecommerce"]["detail"]["products"][0]["name"]
                #product_id = gtm_data_json["ecommerce"]["detail"]["products"][0]["id"]
                price = gtm_data_json["ecommerce"]["detail"]["products"][0]["price"]

                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)


            # Find main image URL
            link_tag = soup.find('link', {'rel': 'preload', 'as': 'image'})
            if link_tag:
                main_image_url = link_tag['href']
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {main_image_url}" + lg)


            print(f"[{Colors.green}Scraping DONE{lg}] CANADA GOOSE -> {interaction.user.id}" + lg)
            print()



            price = self.price.value
            color = self.color.value
            cityzip = f"{city} {zipp}"



            html_content = html_content.replace("{invoicedate}", invoicedate)
            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{cityzip}", cityzip)
            html_content = html_content.replace("{country}", country)
            html_content = html_content.replace("{pname}", product_name)
            html_content = html_content.replace("{color}", color)
            html_content = html_content.replace("{size}", sizee)
            html_content = html_content.replace("{imageurl}", main_image_url)
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{price}", price)




            with open("receipt/updatedrecipies/updatedcanadagoose.html", "w", encoding="utf-8") as file:
                file.write(html_content)



            sender_email = "Canada Goose <noreply@canadagoose.com>"
            subject = f"Your Canada Goose invoice."
            from emails.choise import choiseView
            owner_id = interaction.user.id

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, main_image_url, link)
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)