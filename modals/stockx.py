import asyncio
import json
import re
import warnings
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





def is_stockx_link(link):
    stockx_link_pattern = re.compile(r'^https?://stockx.com/.+$')
    return bool(stockx_link_pattern.match(link))


class stockxmodal(ui.Modal, title="discord.gg/maison"):
    Link = discord.ui.TextInput(label="Link", placeholder="StockX link", required=True)
    conditionn = discord.ui.TextInput(label="Condition (New, Used)", placeholder="New", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    status = discord.ui.TextInput(label="Order Status", placeholder="Ex. Delivered, Ordered, Verified", required=True)
    sizee = discord.ui.TextInput(label="Size (If no size leave blank)", placeholder="US M 13", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        global condition1 , currency1, status, link, sizee
        from addons.nextsteps import NextstepStockX
        owner_id = interaction.user.id 

        link = self.Link.value
        condition = self.conditionn.value
        currency = self.currency.value
        status = self.status.value
        sizee = self.sizee.value if self.sizee.value else ""
        
        
        condition1 = f"{condition}"
        currency1 = f"{currency}"

        if not is_stockx_link(link):
            embed = discord.Embed(title="Error - Invalid StockX link", description="Please provide a valid StockX link.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return


        
        embed = discord.Embed(title="You are almost done...", description="Complete the next modal to receive the receip.")
        await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=NextstepStockX(owner_id))







class stockxmodal2(ui.Modal, title="StockX Receipt"):
    styleidd = discord.ui.TextInput(label="Style ID", placeholder="AMOULW1029-001", required=False)
    pprice = discord.ui.TextInput(label="Price without Currency", placeholder="1693", required=True)
    pfee = discord.ui.TextInput(label="StockX Fee without Currency", placeholder="12.94", required=True)
    shipping = discord.ui.TextInput(label="Shipping Fees without Currency", placeholder="12.94", required=True)
    Delivereddate = discord.ui.TextInput(label="Delivery Date", placeholder="22 January 2024", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        global condition1 , currency1, status, link, sizee

        try:

            pprice = float(self.pprice.value)
            pfee1 = self.pfee.value
            shipping1 = self.shipping.value
            dd = self.Delivereddate.value
            style_id = self.styleidd.value

            embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
            await interaction.response.edit_message(content=None, embed=embed, view=None)

            if not (re.match(r'^\d+(\.\d{1,2})?$', pfee1) and re.match(r'^\d+(\.\d{1,2})?$', shipping1)):
                embed = discord.Embed(title="Error StockX - Invalid fee/shipping format", description="Please use a valid format (e.g., 12.94) for StockX Fee and Shipping Fees.")
                await interaction.edit_original_response(embed=embed)
                return
            
            pfee = float(self.pfee.value)
            shipping = float(self.shipping.value)

            date_pattern = re.compile(r'^\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}$', re.IGNORECASE)

            if not date_pattern.match(dd):
                embed = discord.Embed(title="Error StockX - Invalid date format", description="Please use the format 'Day Month Year'\nEx. `24 January 2024`")
                await interaction.edit_original_response(embed=embed)
                return
            
            total = pprice + pfee + shipping


            total = round(total, 2)

            with open("receipt/stockx.html", "r", encoding="utf-8") as file:
                html_content = file.read()


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
                print(f"[{Colors.green}START Scraping{lg}] STOCKX -> {interaction.user.id} ({interaction.user})" + lg)

                image_url = ""
                

                image_elements = soup.find_all('img')
                image_urls = [img.get('src') for img in image_elements if img.get('src')]
                for image_url in image_urls:
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)
                    break 


                product_name_element = soup.find('h1', {'class': 'chakra-heading css-1qzfqqa'})
                if product_name_element:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    product_name = ''.join(product_name_element.find_all(text=True, recursive=False)).strip()
                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)



                print(f"    [{Colors.cyan}Scraping{lg}] Style ID: {style_id}" + lg)


                print(f"[{Colors.green}Scraping DONE{lg}] STOCKX -> {interaction.user.id}" + lg)
                print()






            pprice1 = f"{pprice}"
            pfee1 = f"{pfee}"
            shipping1 = f"{shipping}"

            html_content = html_content.replace("{placeholder1}", condition1)
            html_content = html_content.replace("{placeholder2}", currency1)
            html_content = html_content.replace("{placeholder3}", pprice1)
            html_content = html_content.replace("{placeholder4}", pfee1)
            html_content = html_content.replace("{placeholder5}", shipping1)
            html_content = html_content.replace("{placeholder6}", dd)
            html_content = html_content.replace("{placeholder7}", status) 
            html_content = html_content.replace("{link_value_stockx}", link)
            html_content = html_content.replace("{brimage}", image_url) 
            html_content = html_content.replace("{pname}", product_name)
            html_content = html_content.replace("{styleid}", style_id)
            html_content = html_content.replace("{sizee}", sizee)

            html_content = html_content.replace("{totalp}", str(total))
            

            with open("receipt/updatedrecipies/updatedstockx.html", "w", encoding="utf-8") as file:
                file.write(html_content)



            sender_email = "StockX <noreply@stockx.org>"
            subject = f"🎉Order {status}: {product_name}"
            from emails.choise import choiseView
            owner_id = interaction.user.id

                
            embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
            view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, link)
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
            await interaction.edit_original_response(embed=embed)