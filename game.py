import json


class game:
    #print(data["Character"]["hp"]) als we iets uit de jsonfile uit willen printen
    #data["Character"]["hp"] = 90 #zo pas je dingen aan
    
    def ReadJson():
        JsonFile = open("game.json", "r")
        data = json.load(JsonFile)
        JsonFile.close()
        return data
    
    def WriteJson(data):
        with open("game.json", "w") as outfile:
            json.dump(data, outfile, indent=2)
        outfile.close()
    data = ReadJson()
    
    #print json data without the curly brackets
    def PrintInventory(data):
        print("\nInventory: \n")
        result = '\n'.join(f'{key}: {value}' for key, value in data["Inventory"].items())
        print(result)
    
    def PrintCharacter(data):
        print("\nCharacter: \n")
        result = '\n'.join(f'{key}: {value}' for key, value in data["Character"].items())
        print(result)


    def start(data):
        goed = False
        begin = input("Do you want to start the game or resume with the latest save?")
        while goed:
            if begin == "start":
                #reset json file to default values
                data["Character"]["hp"] = 100
                data.fromkeys(data["Inventory"],0)#reset de json file (kan je denk beter doen door de file weer leeg te overwriten aangezien je nu ook charachter en Inventory weghaald)
                data.fromkeys(data["Character"],100)#zou dit werken denk je? denk het wel
                game.WriteJson(data)#doe is een normale debug, gwn f5
                goed = True
            #reset json data
            elif begin == "resume":
                goed = True
                pass
            else:
                print("Please enter start or resume")
        
            

    #PrintInventory(data)

    #PrintCharacter(data)
    
    #data["Character"]["hp"] = 100
    
    WriteJson(data)
    

game.start(game.data)
