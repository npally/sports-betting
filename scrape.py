from bs4 import BeautifulSoup
import requests

matchups = []

source = "https://www.oddsshark.com/nba/consensus-picks"
page = requests.get(source)

soup = BeautifulSoup(page.text, 'lxml')

games = soup.find_all('tbody')
game = games[0]


for game in games:
    l = []
    for line in game:

        team = line.find("div", class_="name-wrap").text
        team = team.split()
        team = " ".join(team[1:])

        

        spread = line.find("td", class_="consensus-spread").text

        t = (team, spread)
        l.append(t)
    matchups.append(l)

print(matchups)

