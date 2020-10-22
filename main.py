import discord
import os
import random
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
        spawn = random.randint(1,1000)
        try:
            fclient.query(
                q.get(q.match(q.index("users_by_name"), str(message.author))))
        except:
            person_data = {"data": {
                "name": str(message.author),
                "coins": 0,
                "pokemon": []
            }
            }
            fclient.query(q.create(q.collection('users'), person_data))
       
        if "???find" in message.content:
            person = message.content.replace(" ", "",1).replace("???find", "")
            try:
                something = fclient.query(q.get(q.match(q.index("users_by_name"), str(person))))
                embed = discord.Embed(title="user's pokemon list", color=discord.Color.green())
                for p in something["data"]["pokemon"]:
                   embed.add_field(name=p, value = "...",inline=True)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(
                    title=person + " does not exist", color=discord.Color.green())
                await message.channel.send(embed=embed)

        if "???pokemon" in message.content:
            something = fclient.query(
                q.get(q.match(q.index("users_by_name"), str(message.author))))
            embed = discord.Embed(title=str(message.author)+"'s pokemon", color=discord.Color.green())
            for p in something["data"]["pokemon"]:
                embed.add_field(name=p, value = "...",inline=True)
            await message.channel.send(embed=embed)
        if "???coins" in message.content:
            something = fclient.query(
                q.get(q.match(q.index("users_by_name"), str(message.author))))
            await message.channel.send("coins: "+str(something["data"]["coins"]))
        if "???select" in message.content:
             something = fclient.query(
                q.get(q.match(q.index("users_by_name"), str(message.author))))
             msg = int(message.content.replace(" ","").replace("???select",""))
             p = something["data"]["pokemon"][msg-1]
             if "-" in p:
                pokemonstring, useless, typething = p.partition("-")
                embed = discord.Embed(title=p, color=discord.Color.green())
                embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(
                        pb.pokemon(pokemonstring).id)+useless+typething+".png")
                embed.add_field(name="id:",value=str(pb.pokemon(pokemonstring).id))
                embed.add_field(name="height:",value=str(pb.pokemon(pokemonstring).height))
                embed.add_field(name="weight:",value=str(pb.pokemon(pokemonstring).weight))
                await message.channel.send(embed=embed)
             else:
                embed = discord.Embed(title=p, color=discord.Color.green())
                embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pb.pokemon(p).id)+".png")
                embed.add_field(name="id:",value=str(pb.pokemon(p).id))
                embed.add_field(name="height:",value=str(pb.pokemon(p).height))
                embed.add_field(name="weight:",value=str(pb.pokemon(p).weight))
                await message.channel.send(embed=embed)

        if spawn == 1000:
            pokeid = random.randint(1,898)
            shiny = random.randint(1,100)
            if shiny == 100:
                begurl = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/"
            else:
                begurl = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
            embed1 = discord.Embed(title="‌‌A wild pokémon has аppeаred!", description="Guess the pokémon аnd type the pokémon's name to cаtch it", color=discord.Color.green())
            embed1.set_image(url=begurl+str(pokeid)+".png")
            await message.channel.send(embed=embed1)
            def check(m):
               return m.channel == message.channel and m.author != client.user
            msg = await client.wait_for('message',check=check)
            if pb.pokemon(pokeid).name in msg.content.lower():
              caughtpoke =  pb.pokemon(pokeid).name
              something = fclient.query(
                    q.get(q.match(q.index("users_by_name"), str(msg.author))))
              pokemon = something["data"]["pokemon"]
              reference = something["ref"]
              pokemon.append(caughtpoke)
              data = {
                    "data": {
                        "pokemon": pokemon
                    }
                }
              fclient.query(q.update(q.ref(reference), data))
              embed = discord.Embed(title=caughtpoke+" was successfully caught", description= "#"+str(pokeid), color=discord.Color.green())
              await message.channel.send(embed=embed)

            else:
              await message.channel.send(pb.pokemon(pokeid).name+" fled")


        if "???sell" in message.content:
            msg = message.content.replace("???sell","").replace(" ","",1)
            msg = msg.split()
            try:
                something = fclient.query(q.get(q.match(q.index("users_by_name"), str(message.author))))
                shop = fclient.query(q.get(q.match(q.index("users_by_name"), "shop")))
                pokemon = something["data"]["pokemon"]
                shopPokemon = shop["data"]["pokemon"]
                reference = something["ref"]
                shopReference = shop["ref"]
                pokemon.remove(msg[0])
                shopPokemon.append({"poke":msg[0],"user":str(message.author),"price":int(msg[1])})
                pokemonData = {
                    "data": {
                        "pokemon": shopPokemon
                    }
                }
                data = {
                    "data": {
                        "pokemon": pokemon
                    }
                }
                fclient.query(q.update(q.ref(reference), data))
                fclient.query(q.update(q.ref(shopReference), pokemonData))
                embed = discord.Embed(title=msg[0], description= "was successfully added to the shop", color=discord.Color.green())
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(msg[0]+" doesnt exist or you dont have it")
        if "???buy" in message.content:
                msg = int(message.content.replace("???buy","").replace(" ","",1))-1
                something = fclient.query(q.get(q.match(q.index("users_by_name"), str(message.author))))
                shop = fclient.query(q.get(q.match(q.index("users_by_name"), "shop")))
                pokemon = something["data"]["pokemon"]
                shopPokemon = shop["data"]["pokemon"]
                reference = something["ref"]
                shopReference = shop["ref"]
                seller = fclient.query(q.get(q.match(q.index("users_by_name"), str(shopPokemon[msg]["user"]))))
                if str(message.author) == str(shopPokemon[msg]["user"]):
                    await message.channel.send("sorry you cannot buy your own pokemon")
                else:
                  sellerCoins = int(seller["data"]["coins"])
                  sellerReference = seller["ref"]
                  buyerCoins = int(something["data"]["coins"])
                  if buyerCoins >= int(shopPokemon[msg]["price"]):
                     buyerCoins -= int(shopPokemon[msg]["price"])
                     sellerCoins += int(shopPokemon[msg]["price"])
                     boughtThing = shopPokemon[msg]["poke"]
                     pokemon.append(boughtThing)
                     del shopPokemon[int(msg)]
                     buyerData = {
                       "data" : {
                           "pokemon": pokemon,
                           "coins": buyerCoins
                       }
                     }
                     sellerData = {
                       "data" : {
                           "coins": sellerCoins
                       }
                     }
                     shopData = {
                       "data" : {
                           "pokemon": shopPokemon
                       }
                     }
                     fclient.query(q.update(q.ref(reference), buyerData))
                     fclient.query(q.update(q.ref(shopReference), shopData))
                     fclient.query(q.update(q.ref(sellerReference), sellerData))
                     await message.channel.send(boughtThing+" was added to your account")
                  else:
                    await message.channel.send("you're lacking coins")
                
        if "???transfer" in message.content:
            msg = message.content.replace("???transfer","").replace(" ","",1)
            try:
                something = fclient.query(q.get(q.match(q.index("users_by_name"), str(message.author))))
                pokemon = something["data"]["pokemon"]
                coins = something["data"]["coins"]
                reference = something["ref"]
                pokemon.remove(msg)
                coins += random.randint(10,20)
                data = {
                    "data": {
                        "pokemon": pokemon,
                        "coins": coins
                    }
                }
                fclient.query(q.update(q.ref(reference), data))
                embed = discord.Embed(title=msg, description= "was successfully transferred and "+str(coins)+" coins were added", color=discord.Color.green())
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(msg+" doesnt exist or you dont have it")
        if "???shop" in message.content:
                something = fclient.query(q.get(q.match(q.index("users_by_name"), "shop")))
                embed = discord.Embed(title="shop", description="pokemon on the market", color=discord.Color.green())
                for p in something["data"]["pokemon"]:
                   embed.add_field(name="pokemon: ", value = p["poke"],inline=True)
                   embed.add_field(name="price: ", value = p["price"],inline=True)
                   embed.add_field(name="user: ", value = p["user"],inline=True)

                await message.channel.send(embed=embed)

        if "???help" in message.content:
            embed = discord.Embed(
                title="commands", description="a list of commands", color=discord.Color.green())
            embed.add_field(name="???pokemon",
                            value="list of pokemon", inline=False)
            embed.add_field(name="???find <user>",
                            value="lists any users pokemon", inline=False)
            embed.add_field(name="???select <pokemon number>",
                            value="lists details about one of your pokemon", inline=False)
            embed.add_field(name="???coins",
                            value="displays coin count", inline=False)        
            embed.add_field(name="???transfer <pokemon>",
                            value="transfers a pokemon for coins", inline=False)  
            embed.add_field(name="???sell <pokemon> <coins>",
                            value="puts pokemon up for sale in the shop", inline=False)  
            embed.add_field(name="???buy <number on list>",
                            value="buys pokemon from the shop", inline=False)   
            embed.add_field(name= "???shop",
                            value="displays pokemon in the shop", inline=False)       
            await message.channel.send(embed=embed)


client = MyClient()

client.run(os.getenv("TOKEN"))
