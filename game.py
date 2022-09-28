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
        #Run a for loop over each key in the json file and set it to 0 if that is the desired value
        for  value in dict(data["Character"].items()):
            if value == "hp" or value == "food":
                data["Character"][value] = 100
            else:
                data["Character"][value] = 0
        
        for  value in dict(data["Inventory"].items()):
            data["Inventory"][value] = 0
                  
        game.WriteJson(data)
    
    def help():
        print("HELP: \n")
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
        print("EQUIP: to equip an item")
        print("USE: to use an item")
        print("SAVE: to save the game")
        print("EXIT: to exit the game")
        print("HELP: to see this menu again")
        print("")

    def start(data):
        
        begin = input("Do you want to start the game or resume with the latest save?")
        while begin != "start" and begin != "resume":
            print("Please enter start or resume")
            begin = input("Do you want to start the game or resume with the latest save?")
            
        if begin == "start":
            game.reset(data)
            
            #reset json data
        else:
            #Uiteindelijk de juiste ruimte aanroepen dat in de json file is opgeslagen
            print("resuming game")
            print("This is the inventory u saved: ")
            game.PrintInventory(data)
            
          
        game.Pre_Game_Story(data)
    
    def Pre_Game_Story(data):
        print("\nYou suddenly wake up with the worst headache you have ever had.")
        print("You don't know where you are and you don't know how you got here.")
        print("You only know that you want to climb the mountain and slay the boss.\n")
        game.room1(data)
    
    def room1(data):
        
        print("You can write different commands to look around the room (Write HELP for more info)...")
        command = input("\nType a command...")
        while command.lower() != "go door":
            
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
                
            elif command.lower() == "look":
                print("\nYou look around the room and notice that it is a nice cozy cabin in the woods.\n"
                      "You also notice that there is a closet as well as a fridge.\nThere is also a nice"
                      "wall with a paint on it.")
                command = ""
                
            elif command.lower() == "check closet":
                print("\nYou check the closet and find some nice and warm winter clothes which you put in your inventory.")
                data["Inventory"]["WinterClothes"] = 1
                game.WriteJson(data)
                command = ""
                
            elif command.lower() == "check wall":
                print("\nYou go to the wall and find some shoes which you stash in your inventory.\n"
                    "You also see a weard painting.")
                data["Inventory"]["Shoes"] = 1
                game.WriteJson(data)
                command = ""
                    
            elif command.lower() == "check painting":
                print("\nYou notice that there is a lever, you can pull it.")
                command = ""
                
            elif command.lower() == "pull lever":
                print("\nPulling the lever opens a secret room.")
                #functie aanroepen voor die subroom
                command = ""
                
            elif command.lower() == "check fridge":
                print("\nYou check the fridge and find some nice food to take with you on the journey.")
                data["Inventory"]["Bread"] = 1
                data["Inventory"]["Water"] = 4
                data["Inventory"]["Meat"] = 3
                game.WriteJson(data)
                command = ""
                
            else:
                command = input("\nType a valid command... ")
                
        
        if data["Inventory"]["WinterClothes"] == 0 or data["Inventory"]["Shoes"] == 0:
             print("It is cold outside, check if you can find some clothing and shoes.")
             
        else:
            game.room2(data)
            
        #pass
    def room2(data):
        print("You are in the room 2")
        pass
    
    def room3(data):
        pass
    
    def room4(data):
        pass
    
    def room5(data):
        pass
    #PrintInventory(data)

    #PrintCharacter(data)
    
    #data["Character"]["hp"] = 100
    
    #WriteJson(data)




game.start(game.data)
