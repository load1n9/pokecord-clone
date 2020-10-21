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
        try:
            fclient.query(
                q.get(q.match(q.index("users_by_name"), str(message.author))))
        except:
            person_data = {"data": {
                "name": str(message.author),
                "pokemon": []
            }
            }
            fclient.query(q.create(q.collection('users'), person_data))
            
        if "???find" in message.content:
            person = message.content.replace(" ", "",1).replace("???find", "")
            try:
                something = fclient.query(q.get(q.match(q.index("users_by_name"), str(person))))
                for p in something["data"]["pokemon"]:
                    if "-" in p:
                        pokemonstring, useless, typething = p.partition("-")
                        embed = discord.Embed(
                            title=p, description="#"+str(pb.pokemon(pokemonstring).id), color=discord.Color.green())
                        embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(
                            pb.pokemon(pokemonstring).id)+useless+typething+".png")
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title=p, description="#"+str(pb.pokemon(p).id), color=discord.Color.green())
                        embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pb.pokemon(p).id)+".png")
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
                embed.add_field(name=p, value = pb.pokemon(p).id,inline=True)
            await message.channel.send(embed=embed)
        if "???catch" in message.content:
            pokeid = random.randint(1,898)
            embed1 = discord.Embed(title="‌‌A wild pokémon has аppeаred!", description="Guess the pokémon аnd type the pokémon's name to cаtch it", color=discord.Color.green())
            embed1.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+str(pokeid)+".png")
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



        if "???help" in message.content:
            embed = discord.Embed(
                title="commands", description="a list of commands", color=discord.Color.green())
            embed.add_field(name="???catch",
                            value="finds pokemon nearby", inline=True)
            embed.add_field(name="???pokemon",
                            value="list of pokemon", inline=False)
            embed.add_field(name="???find <user>",
                            value="lists any users pokemon", inline=False)
            await message.channel.send(embed=embed)


client = MyClient()

client.run(os.getenv("TOKEN"))
