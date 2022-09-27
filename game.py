import json
import time

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

    def reset(data):
        data["Character"]["hp"] = 100
        data["Character"]["food"] = 100
        data["Character"]["WinterClothes"] = 0
        data["Character"]["Shoes"] = 0

        data["Inventory"]["GoldCoins"] = 0
        data["Inventory"]["SilverCoins"] = 0
        data["Inventory"]["BronzeCoins"] = 0
        data["Inventory"]["Bread"] = 0
        data["Inventory"]["Meat"] = 0
        data["Inventory"]["DriedMeat"] = 0	
        data["Inventory"]["Water"] = 0
        data["Inventory"]["Wood"] = 0
        data["Inventory"]["gay"] = 0
        data["Inventory"]["WinterClothes"] = 0
        data["Inventory"]["Shoes"] = 0
        game.WriteJson(data)
    
    def help():
        print("HELP")
        print("You can write different commands to look around the room")
        print("You can write the following commands: ")
        print("INVENTORY: to see your inventory")
        print("CHARACTER: to see your character")
        print("LOOK: to look around the room")
        print("GO: if you write go and then a statement that has been said when looking around a room you can go check that place.")
        print("EAT: to eat something")
        print("DRINK: to drink something")
        print("FIGHT: to fight a monster")
        print("TALK: to talk to a character")
        print("PICKUP: to pick up an item")
        print("EQUIP: to equip an ite")
        print("USE: to use an item")
        print("SAVE: to save the game")
        print("EXIT: to exit the game")
        print("HELP: to see this menu again")
        print("")

    def start(data):
        goed = False
        begin = input("Do you want to start the game or resume with the latest save?")
        while goed == False:
            if begin == "start":
                game.reset(data)
                goed = True
            #reset json data
            elif begin == "resume":
                #Uiteindelijk de juiste ruimte aanroepen dat in de json file is opgeslagen
                goed = True
                pass
            else:
                print("Please enter start or resume")
        game.room1(data)
    
    def room1(data):
        print("You suddenly wake up with the worst headache you have ever had.")
        print("You don't know where you are and you don't know how you got here.")
        print("You only know that you want to climb the mountain and slay the boss.")
        
        loop = False
        while loop == False:
            command = input("You can write different commands to look around the room (Write HELP for more info)...")
            if command.lower() == "help":
                game.help()
            elif command.lower() == "inventory":
                game.PrintInventory(data)
            elif command.lower() == "character":
                game.PrintCharacter(data)
            elif command.lower() == "look":
                print("You look around the room and notice that it is a nice cozy cabin in the woods.\n"
                      "You also notice that there is a closet as well as a fridge. There is also a nice\n"
                      "wall with a paint on it.")
            elif command.lower() == "check closet":
                print("You check the closet and find some nice and warm winter clothes which you put in your inventory.")
                data["Inventory"]["WinterClothes"] = 1
            elif command.lower() == "equip clothes":
                data["Character"]["WinterClothes"] = 1
                game.WriteJson(data)
            elif command.lower() == "go door":
                if data["Inventory"]["WinterClothes"] == 0:
                    print("It is cold outside, check if you can find some winterclothes.")
                elif data["Inventory"]["Shoes"] == 0:
                    print("Are you not going to wear some shoes when going outside?")
                else:
                    loop = True
            elif command.lower() == "check wall":
                print("You go to the wall and find some shoes which you stash in your inventory.\n"
                    "You also see a weard painting.")
                data["Inventory"]["Shoes"] = 1
                game.WriteJson(data)
            elif command.lower() == "equip shoes":
                    data["Character"]["Shoes"] = 1
                    game.WriteJson(data)
            elif command.lower() == "check painting":
                print("You notice that there is a lever, you can pull it.")
            elif command.lower() == "pull lever":
                print("Pulling the lever opens a secret room.")
                #functie aanroepen voor die subroom
            elif command.lower() == "check fridge":
                print("You check the fridge and find some nice food to take with you on the journey.")
                data["Inventory"]["Bread"] = 1
                data["Inventory"]["Water"] = 4
                data["Inventory"]["Meat"] = 3
                game.WriteJson(data)
            else:
                print("Please enter a valid command")
            
        #pass

    #PrintInventory(data)

    #PrintCharacter(data)
    
    #data["Character"]["hp"] = 100
    
    #WriteJson(data)




game.start(game.data)
