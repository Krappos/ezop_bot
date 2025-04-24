import discord
from discord.ext import commands
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()


my_token = os.getenv("DISCORD_TOKEN")

generator = pipeline('text-generation', model='gpt2')


DISCORD_TOKEN = my_token
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} je pripravený a pripojený.")

@bot.command()
async def ezop(ctx):
    
    try:
        messages = [message async for message in ctx.channel.history(limit=2)]  
        if len(messages) < 2:
            await ctx.send("Nenašiel som žiadnu správu pred zavolaním príkazu.")
            return
        
        last_message = messages[1].content 
        if not last_message:
            await ctx.send("Posledná správa bola prázdna. Nemôžem z nej vytvoriť príbeh.")
            return

        output = generator(
            last_message,
            max_length=100,       
            num_return_sequences=1,  
            temperature=0.7,     
            top_p=0.9,             
            top_k=50,             
            pad_token_id=50256,   
            truncation=True      
        )

       
        story = output[0]['generated_text']
        await ctx.send(f"Tu je tvoj príbeh, inšpirovaný poslednou správou:\n\n{story}")
        
    except Exception as e:
        print(f"Chyba pri spracovaní správ: {e}")
        await ctx.send("Pri spracovaní správ nastala chyba.")

bot.run(DISCORD_TOKEN)
    