from bs4 import BeautifulSoup 
from urllib2 import urlopen
from time import sleep
import sys
import csv

ESPNDayBaseURL = "http://scores.espn.go.com/ncb/scoreboard?confId=50&date="
ESPNPlayByPlayBaseURL = "http://scores.espn.go.com/ncb/playbyplay?gameId=" 

def getPlaysSoup(gameId):
	return BeautifulSoup(urlopen(ESPNPlayByPlayBaseURL + gameId), "lxml")

def getPlays(gameId):
	playSoup = getPlaysSoup(gameId)
	playTable = playSoup.find("table", "mod-data mod-pbp")
	plays = []
	if playTable:
		for row in playTable.find_all("tr", lambda tr: tr == "odd" or tr == "even"):
			play = []
			for info in row.find_all("td"):
				if info: play.append(info.string.replace(u"\xa0", "")) 
			plays.append(play)
	return plays

def getDaySoup(day):
	return BeautifulSoup(urlopen(ESPNDayBaseURL + day), "lxml")

def getGameId(teamName, day):
	daySoup = getDaySoup(day)
	teams = daySoup.find_all("span", {"id": lambda idName: idName and idName.endswith("hTeamName")})
	for team in teams:
		if team.find_all("a")[0].get("title").lower() == teamName.lower():
			return team.get("id")

'''
Example website: http://scores.espn.go.com//ncb/scoreboard?confId=50&date=20150208
'''
#Takes in a day and team parameter
day = sys.argv[1] #assume that the format is YYYYMMDD 
team = sys.argv[2]

#Gets the gameId
gameId = getGameId(team, day).replace('-hTeamName', '')
print gameId

#Gets plays from the gameID
plays = getPlays(gameId)

#Prints out all the plays from the game
for play in plays:
	print play


