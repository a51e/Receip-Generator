import discord
from modals.acnestudios import acnemodal2
from modals.adidas import adidasmodal2
from modals.apple import  applemodal2
from modals.bape import bapemodal2
from modals.brokenplanet import brokenmodal2
from modals.canadagoose import canadagoose2
from modals.cartier import cartiermodal2
from modals.chromehearts import chromemodal2
from modals.flannels import flannelsmodal2
from modals.gallerydept import gallerydeptmodal2
from modals.grailed import grailedmodal2
from modals.loropiana import loromodal2
from modals.maisonmargiela import maisonmodal2
from modals.pandora import pandoramodal2
from modals.sephora import sephoramodal2
from modals.stockx import stockxmodal2
from modals.zara import zaramodal2
from modals.tnf import tnfmodal2



class NextstepStockX(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Step")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(stockxmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 



class Nextstepbape(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(bapemodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 

class NextstepApple(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(applemodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class Nextsteptnf(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(tnfmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 

class Nextstepcg(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(canadagoose2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class Nextstepsephora(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(sephoramodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class Nextstepzara(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(zaramodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepAcne(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(acnemodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepAdidas(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(adidasmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class Nextstepbroken(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(brokenmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class Nextstepcartier(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(cartiermodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepChrome(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(chromemodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepFlannels(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(flannelsmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepGallerydept(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(gallerydeptmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 


class NextstepLoro(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(loromodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 

class NextstepMaison(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(maisonmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 

class NextstepPandora(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(pandoramodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 

class NextstepGrailed(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    
    @discord.ui.button(label="Next Modal")
    async def nextmodal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id: 
            await interaction.response.send_modal(grailedmodal2())
        else:
            await interaction.response.send_message(content="That is not your panel", ephemeral=True) 
