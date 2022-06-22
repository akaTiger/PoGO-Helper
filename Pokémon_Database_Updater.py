import lib
import urllib.error
import urllib.request
import json
from collections import namedtuple
import os

class pokeNotFound(Exception):
    pass

class setUpError(Exception):
    pass

class argumentError(Exception):
    pass
    
class pokedexOnlineAPI(object):
    def __init__(self):
        self.name = None
        print(lib.getInitMessage())
    
    def setPoke(self, name: str):
        if self.existCheck(name.lower()) is True:
            self.name = name.lower()
            print(f"Pokemon are currently set to {self.name.title()}!")
            request = urllib.request.Request(url=(lib.getURL() + self.name),headers=lib.getHeader())
            self.info = json.loads(urllib.request.urlopen(request).read().decode())
        else:
            raise pokeNotFound
    
    def existCheck(self, name: str):
        try:
            request = urllib.request.Request(url=(lib.getURL() + name),headers=lib.getHeader())
            checkJob = urllib.request.urlopen(request)
            return True
        except urllib.error.HTTPError:
            return False
    
    def preCheck(self):
        if self.name is None:
            raise setUpError
         
    def getType(self):
        self.preCheck()
        return [i["type"]["name"] for i in self.info["types"]]
    
    def getID(self):
        self.preCheck()
        return self.info["id"]
    
    def getWeight(self):
        self.preCheck()
        return self.info["weight"]
    
    def getHeight(self):
        self.preCheck()
        return self.info["height"]
    
    def getAbilities(self):
        self.preCheck()
        return [i["ability"]["name"] for i in self.info["abilities"]]
    
    def getStats(self):
        self.preCheck()
        statsDict = {}
        for i in self.info["stats"]:
            if "-" in i["stat"]["name"]:
                statName = str(i["stat"]["name"]).replace("-", " ")
                statsDict[statName.title()] = i["base_stat"]
            else:
                statsDict[str(i["stat"]["name"]).title()] = i["base_stat"]
        return statsDict
    
    def getAllPokemon(self, outputType: str):
        request = urllib.request.Request(url=(lib.getListAllURL()),headers=lib.getHeader())
        info = json.loads(urllib.request.urlopen(request).read().decode())
        if outputType == "list":
            return [i["name"] for i in info["results"] if "-" not in i["name"]]
        elif outputType == "dict":
            dOut = {}
            startNum = 1
            for i in info["results"]:
                if "-" not in i["name"]:
                    dOut[f"{startNum:0>3}"] = i["name"]
                    startNum += 1
            return dOut
        elif outputType == "lont":
            l = []
            pokeTuple = namedtuple('pokeTuple', ['name', 'id', 'type'])
            for i in [i["name"] for i in info["results"] if "-" not in i["name"]]:
                self.setPoke(i)
                thisPoke = pokeTuple(name=str(i).title(), id=self.getID(), type=self.getType())
                l.append(thisPoke)
            return l

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    api = pokedexOnlineAPI()
    api.setPoke("charizard")
    print(api.getAllPokemon("lont"))