import requests
from bs4 import BeautifulSoup
import sys

def getResults(search):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    url = f"https://www.planetminecraft.com/projects/?platform=1&keywords={search}"
    print(url)
    result = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(result.content, "html.parser")
    srces = soup.find_all("div", class_="r-preview")
    imgsrces = []
    linksrces = []
    descriptions = []
    downloads = []
    for src in srces:
        imgsrces.append(src.find("img")["src"])
        linksrces.append("https://www.planetminecraft.com"+src.find("a")["href"])
        newurl = "https://www.planetminecraft.com"+src.find("a")["href"]
        newresult = requests.get(newurl, headers=user_agent)
        if BeautifulSoup(newresult.content, "html.parser").find(id="r-text-block") == None:
            descriptions.append(None)
        else:
            descriptions.append(BeautifulSoup(newresult.content, "html.parser").find(id="r-text-block").text.encode('cp1252', errors='ignore').decode('cp1252', errors='ignore').replace("-", ""))
        bap = None
        if BeautifulSoup(newresult.content, "html.parser").find("a", {"title": "Download this file for Minecraft."}) != None:
            bap = "https://www.planetminecraft.com"+BeautifulSoup(newresult.content, "html.parser").find("a", {"title": "Download this file for Minecraft."})["href"]
        if BeautifulSoup(newresult.content, "html.parser").find("a", class_="third-party-download") != None:
            bap = "https://www.planetminecraft.com"+BeautifulSoup(newresult.content, "html.parser").find("a", class_="third-party-download")["href"]

        downloads.append(bap)
    
    response = {}
    for i in range(len(imgsrces)):
        response[f"Map {i + 1}"] = {
            "img": imgsrces[i],
            "link": linksrces[i],
            "description": descriptions[i],
            "download": downloads[i]
        }
    
    return response

def getDownloadableResults(search):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    url = f"https://www.planetminecraft.com/projects/?platform=1&share=world_link&keywords={search}"
    result = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(result.content, "html.parser")
    srces = soup.find_all("div", class_="r-preview")
    imgsrces = []
    linksrces = []
    descriptions = []
    downloads = []
    for src in srces:
        imgsrces.append(src.find("img")["src"])
        linksrces.append("https://www.planetminecraft.com"+src.find("a")["href"])
        newurl = "https://www.planetminecraft.com"+src.find("a")["href"]
        newresult = requests.get(newurl, headers=user_agent)
        if BeautifulSoup(newresult.content, "html.parser").find(id="r-text-block") == None:
            descriptions.append(None)
        else:
            descriptions.append(BeautifulSoup(newresult.content, "html.parser").find(id="r-text-block").text.encode('cp1252', errors='ignore').decode('cp1252', errors='ignore').replace("-", ""))
        bap = None
        if BeautifulSoup(newresult.content, "html.parser").find("a", {"title": "Download this file for Minecraft."}) != None:
            bap = "https://www.planetminecraft.com"+BeautifulSoup(newresult.content, "html.parser").find("a", {"title": "Download this file for Minecraft."})["href"]
        if BeautifulSoup(newresult.content, "html.parser").find("a", class_="third-party-download") != None:
            bap = "https://www.planetminecraft.com"+BeautifulSoup(newresult.content, "html.parser").find("a", class_="third-party-download")["href"]

        downloads.append(bap)
    
    response = {}
    for i in range(len(imgsrces)):
        response[f"Map {i + 1}"] = {
            "img": imgsrces[i],
            "link": linksrces[i],
            "description": descriptions[i],
            "download": downloads[i]
        }
    
    return response

args = sys.argv.copy()
for arg in args:
    if "main.py" or "Main.py" in arg:
        args.remove(arg)
search = '+'.join(map(str, args))
if "-d" in args:
    print(getDownloadableResults(search))
else:
    print(getResults(search))