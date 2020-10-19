import discord
import os
import pokebase as pb
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

fclient = FaunaClient(secret=os.getenv("FAUNA"))
class MyClient(discord.Client):

    async def on_ready(self):

        print('Logged on as', self.user)

    async def on_message(self, message):

        if message.author == client.user:
        
          return
        try:
          fclient.query(q.get(q.match(q.index("users_by_name"),str(message.author))))
        except:
          person_data = { "data":{ 
            "name": str(message.author),
            "pokemon": []
          }
          }
          fclient.query(q.create(q.collection('users'), person_data))

    
        if "???add" in message.content:  
          try:
            stuff = message.content.replace("???add","").replace(" ","")
            print(pb.pokemon(stuff).height)
            something = fclient.query(q.get(q.match(q.index("users_by_name"),str(message.author))))

            pokemon = something["data"]["pokemon"]
            reference = something["ref"]

            pokemon.append(stuff)

            data = { 
                "data": {
                    "pokemon": pokemon
                 }
              }
              
            fclient.query(q.update(q.ref(reference), data))

            await message.channel.send("added "+stuff)
            await message.channel.send("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pb.pokemon(str(stuff).replace(" ","")).id)+".png")
          except: 
            await message.channel.send("pokemon doesnt exist")


        if "???pokemon" in message.content:
           something = fclient.query(q.get(q.match(q.index("users_by_name"),str(message.author))))

           for p in something["data"]["pokemon"]:
             if "-" in p:
                pokemonstring,useless,typething = p.partition("-")
                embed = discord.Embed(title=p,description="#"+str(pb.pokemon(pokemonstring).id),color=discord.Color.green())
                embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pb.pokemon(pokemonstring).id)+useless+typething+".png")
                await message.channel.send(embed=embed)
             else:
                 embed = discord.Embed(title=p,description="#"+str(pb.pokemon(p).id),color=discord.Color.green())
                 embed.set_image(url= "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pb.pokemon(p).id)+".png")
                 await message.channel.send(embed=embed)
        if "???help" in message.content:
           embed = discord.Embed(title="commands",description="a list of commands",color=discord.Color.green())
           embed.add_field(name="???add <pokemon>",value="adds pokemon",inline=True)
           embed.add_field(name="???pokemon",value="list of pokemon",inline=False)
           await message.channel.send(embed=embed)

           

client = MyClient()

client.run(os.getenv("TOKEN"))
