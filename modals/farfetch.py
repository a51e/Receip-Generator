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





def is_farfetch_link(link):
    farfetch_pattern = re.compile(r'^https?://(www\.)?farfetch\.com/.+')

    return bool(farfetch_pattern.match(link))


class farfetchmodal(ui.Modal, title="discord.gg/maison"):
    Linkff = discord.ui.TextInput(label="Link", placeholder="Farfetch EU link", required=True)
    Priceff = discord.ui.TextInput(label="Price without currency", placeholder="790", required=True)
    currencyff = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    deliverydateff = discord.ui.TextInput(label="Delivery Date in - MM/DD/YY", placeholder="Ex. 7/15/2024", required=True)


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
            firstname1 = name


            if not is_farfetch_link(Linkff):
                embed = discord.Embed(title="Error - Invalid Farfetch link", description="Please provide a valid Farfetch link.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            try:
                embed = discord.Embed(title="Under Process...", description="Processing your email will be sent soon!", color=0x1e1f22)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)

                deliverydate = self.deliverydateff.value


                with open("receipt/farfetch.html", "r", encoding="utf-8") as file:
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


                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] FARFETCH -> {interaction.user.id} ({interaction.user})" + lg)


                    brandname1 = soup.find('div', {'class': 'ltr-8c0sef'})

                    if brandname1:
                        brandname2 = soup.find('div', {'class': 'ltr-9fv542'})
                        brandname234 = None

                        if brandname2:
                            brandname3 = soup.find('h1', {'class': 'ltr-i980jo el610qn0'})

                            if brandname3:
                                brandname234 = brandname3.find('a', {'class': 'ltr-183yg4m-Body-Heading-HeadingBold e1h8dali1'}).text.strip()

                        print(f"    [{Colors.cyan}Scraping{lg}] Brand Name: {brandname234}" + lg)






                    productname1 = soup.find('div', {'class': 'ltr-8c0sef'})

                    if productname1:
                        productname2 = soup.find('div', {'class': 'ltr-9fv542'})
                        productname = None

                        if productname2:
                            productname3 = soup.find('h1', {'class': 'ltr-i980jo el610qn0'})

                            if productname3:
                                productname = productname3.find('p', {'class': 'ltr-13ze6d5-Body efhm1m90'}).text.strip()

                        print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {productname}" + lg)



                    productimage3 = soup.find('div', {'class': 'ltr-ukwwcv'})


                    button_element = productimage3.find('button', {'class': 'ltr-1c58b5g'})

                    if button_element:

                        image_element = button_element.find('img', {'class': 'ltr-1w2up3s'})

                        if image_element:

                            productimage = image_element['src'].strip()

                            print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {productimage}" + lg)


                    print(f"[{Colors.green}Scraping DONE{lg}] FARFETCH -> {interaction.user.id}" + lg)
                    print()





                cityzip = f"{city} {zipp}"



                html_content = html_content.replace("{firstname}", firstname1)
                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{cityzip}", cityzip)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{deliverydate}", deliverydate)

                html_content = html_content.replace("{imageurl}", str(productimage))

                html_content = html_content.replace("{brandname}", brandname234)
                html_content = html_content.replace("{productname}", productname)


                html_content = html_content.replace("{currency}", currencyff) 
                html_content = html_content.replace("{total}", Priceff)
                

                with open("receipt/updatedrecipies/updatedfarfetch.html", "w", encoding="utf-8") as file:
                    file.write(html_content)    


                image = str(productimage)

                sender_email = "FARFETCH <info@farfetch.com>"
                subject = "Your order will be with you soon"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="Choose email provider", description="Email is ready to send choose Spoofed or Normal domain.", color=0x1e1f22)
                view = choiseView(owner_id, html_content, sender_email, subject, productname, image, Linkff)
                await interaction.edit_original_response(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred: {str(e)}")
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="Error", description="No user details found. Please ensure your information is set up.")
            await interaction.response.send_message(embed=embed, ephemeral=True)





