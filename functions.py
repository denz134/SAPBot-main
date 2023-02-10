# in order to maintain organization in the rest of the files, i've dumped all the long functions and variables into this one, please don't judge me D:

import os
import discord
import requests
import random
import rstr
from dotenv import load_dotenv

load_dotenv()


guild_ids = [940119443109969990]
group_id = 11228220

subreddit = "memes"

roles = {
    1 : {
        "name":"Development Team",
        "roleId" : 66117905,
        "rank": 230
    },
    2: {
        "name": "Chief Inspector",
        "roleId" : 66117622,
        "rank": 229
    },
    3:{
        "name": "Inspector",
        "roleId" : 66117648,
        "rank": 228
    },
    4:{
        "name": "Senior Sergeant First Class",
        "roleId" : 66117667,
        "rank": 226
    },
    5:{
        "name": "Senior Sergeant",
        "roleId" : 66117718,
        "rank": 18
    },
    6:{
        "name": "Sergeant",
        "roleId" : 66117723,
        "rank": 17
    },
    7:{
        "name": "Brevent Sergeant",
        "roleId" : 66117733,
        "rank": 16
    },
    8:{
        "name": "Senior Constable First Class",
        "roleId" : 66117816,
        "rank": 11
    },
    9:{
        "name": "Senior Constable",
        "roleId" : 66117881,
        "rank": 8
    },
    10:{
        "name": "Constable",
        "roleId" : 66117904,
        "rank": 6,

    },
    11:{
        "name": "Probationary Constable",
        "roleId" : 66117887,
        "rank": 5
    },
    12:{
        "name": "Police Cadet",
        "roleId" : 66117183,
        "rank": 4
    },
    13:{
        "name": "Suspended",
        "roleId" : 67549098,
        "rank": 2
    },
    14:{
        "name": "Junior Cadet",
        "roleId" : 67549117,
        "rank": 1
    }
}

def get_jokeEmbed(jokeType):
    if jokeType:
        if jokeType.lower() == "pun":
            url = "https://v2.jokeapi.dev/joke/Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        elif jokeType.lower() == "programming":
            url = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        elif jokeType.lower() == "misc":
            url = "https://v2.jokeapi.dev/joke/Miscellaneous?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        elif jokeType.lower() == "dark":
            url = "https://v2.jokeapi.dev/joke/Dark?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        elif jokeType.lower() == "spooky":
            url = "https://v2.jokeapi.dev/joke/Spooky?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        elif jokeType.lower() == "christmas":
            url = "https://v2.jokeapi.dev/joke/Christmas?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        else:
            url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    else:
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    
    jokeData = requests.get(url).json()
    if jokeData['error'] == True:
        return "Error"
    
    jokeEmbed = None
    if jokeData['type'] == "single":
        jokeEmbed = discord.Embed(title="Here's a joke for ya!", description=jokeData['joke'], color=0x00ff00)
    elif jokeData['type'] == "twopart":
        jokeEmbed = discord.Embed(title="Here's a joke for ya!", description=f"{jokeData['setup']}\n||{jokeData['delivery']}||", color=0x00ff00)
    return jokeEmbed

def getMemeEmbed():
    url = f"https://meme-api.herokuapp.com/gimme/{subreddit}"
    request = requests.get(url)
    response = request.json()
    memeTitle = response["title"]
    memeAuthor = response["author"]
    memeImage = response["url"]
    memeUrl = response["postLink"]
    memeAuthorUrl = "https://reddit.com/u/{}".format(memeAuthor)
    memeEmbed = discord.Embed(title=memeTitle, description=f"[r/{subreddit}](https://reddit.com/{subreddit})", url=memeUrl, color=0x00ff00)
    memeEmbed.set_footer(text=f"u/{memeAuthor}")
    memeEmbed.set_image(url=memeImage)
    return memeEmbed

def set_role(userId, roleId):
    cookie = os.environ.get("ROBLOXTOKEN")
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    url = f"https://groups.roblox.com/v1/groups/{group_id}/users/{userId}"
    data = {
        "roleId" : int(roleId)
    }
    fetchToken = session.patch(url, json=data)
    xcrfToken = fetchToken.json()
    if "X-CSRF-Token" in fetchToken.headers:  # check if token is in response headers
        session.headers["X-CSRF-Token"] = fetchToken.headers["X-CSRF-Token"]
    request = session.patch(url, json=data)
    response = request.json()


def get_roles():
    cookie = os.environ.get("ROBLOXTOKEN")
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    url = f"https://groups.roblox.com/v1/groups/{group_id}/roles"
    request = session.get(url)
    response = request.json()

def get_role(userId):
    cookie = os.environ.get("ROBLOXTOKEN")
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    groups_url = f"https://groups.roblox.com/v1/users/{userId}/groups/roles"
    request = session.get(groups_url)
    user_groups = request.json()['data']
    for groupInfo in user_groups:
        groupObj = groupInfo['group']
        if groupObj['id'] == group_id:
            roleObj = groupInfo['role']
            return roleObj

def get_role_id_from_name(name):
    for index in roles:
        role = roles[index]
        if role["name"].lower() == name.lower():
            return role["roleId"], role["name"]
        
def get_user_id_from_name(name):
    url = "https://api.roblox.com/users/get-by-username?username={}".format(str(name))
    request = requests.get(url)
    response = request.json()
    if "SUCCESS" in response:
        print("error")
        return "NO_SUCH_USER", None
    else:
        user_id = response["Id"]
        name = response["Username"]
        return user_id, name

def get_username_from_id(userid):
    url = "https://api.roblox.com/users/{}".format(str(userid))
    request = requests.get(url)
    response = request.json()
    if "SUCCESS" in response:
        return "NO_SUCH_USER"
    else:
        name = response["Username"]
        return name

def get_roblox_avatar(user_id):
    url = "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={}&size=48x48&format=Png&isCircular=false".format(str(user_id))
    request = requests.get(url)
    response = request.json()
    imageUrl = response["data"][0]["imageUrl"]
    return imageUrl

def promote(user_id):
    user_role = get_role(user_id)
    for index in roles:
        if roles[index]['roleId'] == user_role['id']:
            newIndex = index - 1
            if newIndex in roles:
                nextRole = roles[newIndex]
                nextRoleId = nextRole['roleId']
                set_role(user_id, nextRoleId)                            
                return "SUCCESS", nextRole
            else:
                return "MAX", None
        else:
            "NOT_IN_GROUP", None

def demote(user_id):
    user_role = get_role(user_id)
    for index in roles:
        if roles[index]['roleId'] == user_role['id']:
            newIndex = index + 1
            if newIndex in roles:
                nextRole = roles[newIndex]
                nextRoleId = nextRole['roleId']
                set_role(user_id, nextRoleId)                            
                return "SUCCESS", nextRole
            else:
                return "LOW", None
        else:
            "NOT_IN_GROUP", None

def get_trello_link(endpoint):
    url = "https://api.trello.com/1{}?key={}&token={}".format(endpoint, os.getenv("TRELLO_KEY"), os.getenv("TRELLO_TOKEN"))   
    return url

def get_desc_string(username, user_id, profileLink, reason, evidenceUrl, banLength):
    profileLink = "https://www.roblox.com/users/{}/profile".format(str(user_id))
    descString = f"---\n>  **Username: '{username}'** \n\n> **UserId: '{user_id}'** \n\n> **Profile Link: '{profileLink}'** \n\n> **Reason: '{reason}'** \n\n> **Evidence: '{evidenceUrl}'** \n\n> **Ban Length: '{banLength}'** "
    return descString

def create_ban_card(user_id, reason, evidenceUrl, banLength):
    prevExists = get_ban_card(user_id)
    if prevExists != "NO_RECORDS":
        return "ALREADY_BANNED"
    createCardUrl = get_trello_link("/cards")
    username = get_username_from_id(user_id)
    if username == "NO_SUCH_USER":
        return "INVALID_USERID"
    profileLink = "https://www.roblox.com/users/{}/profile".format(str(user_id))
    descString = get_desc_string(username, user_id, profileLink, reason, evidenceUrl, banLength)
    descString = descString.replace(">", " ")
    descString = descString.replace("'", " ")
    descString = descString.replace("\n\n", "\n")
    query = {
        "idList": "62039def75a5f1360a46017f",
        "idCardSource": "62039def75a5f1360a460309",
        "keepFromSource": "all",
        "name": f"{username}:{user_id}",
        "desc": descString
    }
    headers = {
        "Accept": "application/json"
    }
    request = requests.post(createCardUrl, params=query, headers=headers)
    response = request.json()
    return response

def get_ban_card(user_id):
    url = get_trello_link("/lists/62039def75a5f1360a46017f/cards")
    request = requests.get(url)
    ban_cards = request.json()
    for ban_card in ban_cards:
        if str(user_id) in str(ban_card["name"]):
            banCardArgs = ban_card["name"].split(":")
            banCardUserId = banCardArgs[1]
            if str(banCardUserId) == str(user_id):
                return ban_card
    return "NO_RECORDS"

def delete_ban_card(user_id):
    card = get_ban_card(user_id)
    if card == "NO_RECORDS":
        return "NOT_BANNED"
    cardId = card["id"]
    url = get_trello_link("/cards/{}".format(cardId))
    request = requests.delete(url)
    response = request.text
    return response

def update_ban_reason(user_id, reason):
    banCard = get_ban_card(user_id)
    username = get_username_from_id(user_id)
    if username == "NO_SUCH_USER":
        return "INVALID_USERID"
    if banCard == "NO_RECORDS":
        return "NO_RECORDS"    
    descString = banCard["desc"]
    args = descString.split("\'")
    username = args[1]
    profileLink = args[5]
    evidenceUrl = args[9]
    banLength = args[11]
    newDescString = get_desc_string(username, user_id, profileLink, reason, evidenceUrl, banLength)
    card_id = banCard["id"]
    createCardUrl = get_trello_link(f"/cards/{card_id}")
    query = {
        "idList": "62039def75a5f1360a46017f",
        "idCardSource": banCard["id"],
        "keepFromSource": "all",
        "name": f"{user_id}",
        "desc": newDescString
    }
    headers = {
        "Accept": "application/json"
    }
    request = requests.put(createCardUrl, params=query, headers=headers)
    response = request.text
    return response
