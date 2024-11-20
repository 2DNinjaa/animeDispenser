from datetime import datetime

import json
import pip._vendor.requests 
import secrets
import webbrowser
import random
 
global curr_token
CLIENT_ID = 'client id'
CLIENT_SECRET = 'secret token'
testtoken="test"

# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier():
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url():
    global code_verifier
    code_challenge=get_new_code_verifier()
    code_verifier=code_challenge

    url = "https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id="+CLIENT_ID+"&state=KrustyKrabPizza&redirect_uri=https://coredigitalhome.com/&code_challenge="+code_challenge


    webbrowser.open_new_tab(url)

# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code, code_verifier):
    global curr_token
    global testtoken

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': authorisation_code,
        "redirect_uri":"https://coredigitalhome.com/",
        'code_verifier': code_verifier,
    }
    
    response = pip._vendor.requests.post(url, data)
    #response.raise_for_status()  # Check whether the requests contains errors
    # print(response.json())
    token = response.json()
    testtoken=token
    curr_token=token
    response.close()
    print('Token generated successfully!')


    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')
    testtoken=token

# 4. Test the API by requesting your profile information
def print_user_info():
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = pip._vendor.requests.get(url, headers = {
        'Authorization': f'Bearer {testtoken["access_token"]}'
        })
    
    response.raise_for_status()
    user = response.json()

    response.close()
    try:
        user["error"]
        return 0
    except:

        print(f"\n>>> Greetings {user['name']}! <<<")
        return 1

def rankings(token):
    'returns a random anime via the rankings of animes'
    mod=random.randint(0,8)
    opt=["all","airing","upcoming","tv","ova","movie","special","bypopularity","favorite"]
    mod=opt[mod]
    mod="upcoming"
    mod2=random.randint(1,50)
    # link="https://api.myanimelist.net/v2/anime/ranking?ranking_type="+mod+"&limit="+str(mod2)

    link="https://api.myanimelist.net/v2/anime/ranking?ranking_type="+mod+"&limit="+str(250)

    r = pip._vendor.requests.get(link, headers = {
            'Authorization': f'Bearer {token}'
            })
    r=r.json()
    mod3=random.randint(1,mod2)
    anime=r["data"][mod3]["node"]["title"]
    print(len(r["data"]))
    print(anime)
    #print("finished getting rankings")                      
    

def season():

    todayDate = str(datetime.now())
    ind=todayDate.index(" ")
    todayDate=todayDate[:ind]
    month=todayDate[5:7]
    year=todayDate[:4]
    animeSeason="none"
    if int(month)<4:
        animeSeason='winter'
    elif int(month)>3 and int(month)<7:
        animeSeason='spring'
    elif int(month)>6 and int(month)<10:
        animeSeason='summer'
    else:
        animeSeason="fall"


    idList=[]
    link="https://api.myanimelist.net/v2/anime/season/%s/%s?limit=10" % (year,animeSeason)
    r = pip._vendor.requests.get(link, headers = {
            'Authorization': f'Bearer {testtoken["access_token"]}'
        })
    try:
        r.json()["error"]
        refresh_token()
        r = pip._vendor.requests.get(link, headers = {
        'Authorization': f'Bearer {testtoken["access_token"]}'
        })
    except:
        print("ok")
    
    for i in r.json()["data"]:
        idList.append(i["node"]["id"])
    with open("seasonSmall.json", "w") as outfile:
        json.dump(r.json()["data"], outfile)
    return idList
    # print(len(r.json()["data"])) 

def refresh_token():
    global testtoken
    # with open("token.json", "r", encoding="utf-8") as fp:
    #     info = json.load(fp)

    rToken=testtoken["refresh_token"]#probably wrong to do this
    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': "refresh_token",
        'refresh_token': rToken,
    }
    
    response = pip._vendor.requests.post(url, data)
    #response.raise_for_status()  # Check whether the requests contains errors
    #print(response.json())
    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')
    testtoken=token

def gen_codes():
    code_verifier = get_new_code_verifier()
    print_new_authorisation_url()
    

    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    generate_new_token(authorisation_code, code_verifier)


def details(idList): # 'id': 49387, 'title': 'Vinland Saga Season 2'
    'get the details of a certain anime'
    #        link="https://api.myanimelist.net/v2/anime/"+str(i)+"?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw,created_at,updated_at,media_type,status,genres,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,studios"

    showInfo={}
    for i in idList:
        link="https://api.myanimelist.net/v2/anime/"+str(i)+"?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw,created_at,updated_at,status,genres,num_episodes,start_season,broadcast"
        r = pip._vendor.requests.get(link, headers = {
            'Authorization': f'Bearer {testtoken["access_token"]}'
        })
        day=datetime.fromisoformat(r.json()["updated_at"])
        weekday=day.strftime("%A")
        time=24-int(day.strftime("%H"))

        
        print(r.json()["title"]+"("+r.json()["alternative_titles"]["en"]+")" + " releases on "+ weekday+" at "+str(time) )
        showInfo[i]=r.json()
    with open("showInfoSmall.json", "w") as outfile:
        json.dump(showInfo, outfile)

if __name__ == '__main__':
    with open("token.json", "r", encoding="utf-8") as fp:
        testtoken = json.load(fp)

    try:
        print_user_info()
    except:
        gen_codes()







    # rankings(token['access_token'])
    # print()
    # print(token['access_token'])
    #importAnime(token['access_token'])
    ids=season()
    print(ids)
    details(ids)
    





# todayDate = str(datetime.now())
# ind=todayDate.index(" ")
# todayDate=todayDate[:ind]
# month=todayDate[5:7]
# year=todayDate[:4]
# if int(month)<5:
#     print("q1")

# print(month)
# print(year)
# print(todayDate)