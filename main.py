import os
import requests
import random
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import asyncio
import aiohttp

# The token is private, so this stops nasty people hijacking our stuff fom our public repo
#load_dotenv()
#TOKEN = os.getenv("DISCORD_TOKEN")

bot_description = """
[Bot description]

Commands:
!cdc -- shows various links to CDC resources

!stats -- shows the global COVID-19 statistics and links to a page listing the up-to-date stats.

!USAstats -- shows the COVID-19 cases in the USA

!risk <age> <zip code> <are you hispanic (y/n)> <gender> <feet (height)> <inches (height)> <weight (lbs)>

Visit [website link] for more information!
"""

client = commands.Bot(command_prefix="!", description=bot_description)

@client.command()
async def cdc(ctx):
  await ctx.send("""
    Links to CDC information:
      Main site: https://www.cdc.gov
      Things to know: https://www.cdc.gov/coronavirus/2019-ncov/your-health/need-to-know.html
     Guidance documents: https://www.cdc.gov/coronavirus/2019-ncov/communication/guidance-list.html?Sort=Date%3A%3Adesc
  
    Visit https://www.cdc.gov/coronavirus/2019-nCoV/index.html for more information!
    """)

@client.command()
async def stats(ctx):
  await ctx.send("""
  
   There are currently 94.4 Million COVID-19 cases across the globe and 2.02 Million deaths. For up to date statistics, follow the link:

   https://www.worldometers.info/coronavirus/

  """)

@client.command()
async def USAstats(ctx):
  await ctx.send("""
  

  """)  

@client.command()
async def risk(ctx, age, zip_code, is_hispanic: int, gender, h_feet, h_inches, weight):
  if gender.lower() == "male":
    gender = 0.431782416425538 # Idek why it's this number but that's what the webiste wants
  elif gender.lower() == "female":
    gender = 0
  else:
    await ctx.send("That gender cannot be used, sorry (only male and female are allowed -- NOT OUR DECISION DON'T SUE US PLS)")
    return

  if int(age) < 18:
    await ctx.send("You must be over 18 to use this, sorry")
    return

  payload = {
    "age": age, 
    "zipcode": zip_code, 
    "hispanic": is_hispanic, 
    "gender": gender, 
    "feet": h_feet, 
    "inches": h_inches, 
    "weight": weight
  }

  async with aiohttp.ClientSession() as session:
    async with session.get("https://covid19risktools.com:8443/riskcalculator", params=payload) as response:
      text = await response.read()

  soup = BeautifulSoup(text.decode('utf-8'), "lxml")
  
  main_content = soup.find("section", class_="risk-assessment-section sectionpadding60").find("div", class_="container")
  rows_div = main_content.find("div", class_="row")
  col_12_div = rows_div.find_all("div", recursive=False)[1]

  risks_p_text = main_content.find_all("p", recursive=False)[0].text
  risks_no_newlines = risks_p_text.replace("\n", " ").replace("\r", " ")
  risks_formatted = " ".join(risks_no_newlines.split())

  deaths_p_text = col_12_div.find_all("p")[0].text
  deaths_no_newlines = deaths_p_text.replace("\n", " ").replace("\r", " ")
  deaths_formatted = " ".join(deaths_no_newlines.split())
  
  ci_p_text = col_12_div.find_all("p")[1].text
  ci_no_newlines = ci_p_text.replace("\n", " ").replace("\r", " ")
  ci_formatted = " ".join(ci_no_newlines.split())

  output_text = f"""
  **COVID-19 Risk Assesment**
  {risks_formatted}

  {deaths_formatted}

  _{ci_formatted}_

  The above information is from **COVID-19 Risk Tools**.
  Visit https://covid19risktools.com:8443/riskcalculator for more information.
  """
  
  await ctx.send(output_text)

client.run("ODAwMDI3NTYwNTQwNzY2MjM5.YAMJug.Yo3T3zm2VMqIQs1UfEVMbLNYgqE")
