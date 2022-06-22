import helper
import os

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    Pokedex = helper.Pokedex()
    Pokedex.setPoke("charizard")
    print(Pokedex.getStats())