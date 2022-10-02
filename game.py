import json
import time
from termcolor import colored
import random
from playsound import playsound
#https://pypi.org/project/termcolor/ voor meer kleur en text info
#https://asciiflow.com/ om puzzel met ascii te tekenen
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
            if value == "Hp" or value == "Food":
                data["Character"][value] = 100
            else:
                data["Character"][value] = 0
        
        for  value in dict(data["Inventory"].items()):
            data["Inventory"][value] = 0
            
        data["Room"] = 0
                  
        game.WriteJson(data)

    #Functie om items te equippen
    def equip(info, data):
        file = open("game.json", "r")
        items = json.load(file)
        e = info
        for item in items:
            if "Inventory" in item:
                for item2 in items["Inventory"]:
                    if info in item2:
                        data["Character"][e] = 1
                        data["Inventory"][e] = 0
                        print("You have equipped the", e)
                        game.WriteJson(data)
    
    #Functie om voedsel te consumeren
    def food(info, data):
        file = open("game.json", "r")
        food = json.load(file)
        e = info
        for item in food:
            if "Inventory" in item:
                for item2 in food["Inventory"]:
                    if info in item2:
                        if e == "Bread" and data["Inventory"][e] > 0:
                            data["Character"]["Food"] += 20
                            data["Inventory"][e] -= 1
                            print("You have eaten", e)
                            game.WriteJson(data)
                        elif e == "DriedMeat" and data["Inventory"][e] > 0:
                            data["Character"]["Food"] += 30
                            data["Inventory"][e] -= 1
                            print("You have eaten", e)
                            game.WriteJson(data)
                        elif e == "Meat" and data["Inventory"][e] > 0:
                            data["Character"]["Food"] += 40
                            data["Inventory"][e] -= 1
                            print("You have eaten", e)
                            game.WriteJson(data)
    
    #Als je verder wil gaan met het spel op de laatste plek waar je was
    #dan wordt deze functie aangeroepen.
    def LoadRoom(data):
        if data["Room"] == 0:
            print(colored("No savegame, starting new game","red"))
            game.reset(data)
            game.Pre_Game_Story(data)
        elif data["Room"] == 1:
            game.room1(data)
        elif data["Room"] == 2:
            game.room2(data)
        elif data["Room"] == 2.5:
            game.subroom2(data)
        elif data["Room"] == 3:
            game.room3(data)
        elif data["Room"] == 3.5:
            game.subroom3(data)
        elif data["Room"] == 4:
            game.room4(data)
        elif data["Room"] == 5:
            game.room5(data)
        elif data["Room"] == 5.1:
            game.subroom5_1(data)
        elif data["Room"] == 5.2:
            game.subroom5_2(data)
        elif data["Room"] == 5.3:
            game.subroom5_3(data)
        elif data["Room"] == 6:
            game.room6(data)
        elif data["Room"] == 7:
            game.room7(data)
        elif data["Room"] == 8:
            game.room8(data)
        elif data["Room"] == 9:
            game.room9(data)
        elif data["Room"] == 10:
            game.room10(data)

    #functie waarmee je het spel kan opslaan via een json file               
    def save(data):
        print(colored("\nSaving game...", "red"))
        game.WriteJson(data)
        time.sleep(0.5)
        print(colored("\nSaved Game!", "red"))
        game.LoadRoom(data)
        

    #Functie dat wordt aangeroepen als je help schrijft
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
        print("SAVE: to save the game")
        print("EXIT: to exit the game")
        print("HELP: to see this menu again")
        print("")

    def start(data):
        
        begin = input("Do you want to start the game or resume with the latest save? ")
        while begin != "start" and begin != "resume":
            print(colored("Please enter start or resume","red"))	
            begin = input("Do you want to start the game or resume with the latest save? ")
            
        if begin == "start":
            game.reset(data)
            game.Pre_Game_Story(data)
            #reset json data
        else:
            #Uiteindelijk de juiste ruimte aanroepen dat in de json file is opgeslagen
            print(f"resuming game in room {data['Room']}")
            print("This is the inventory u saved: ")
            game.PrintInventory(data)
            
            game.LoadRoom(data)
            
            
          
        
    #De functie die in het begin wordt aangeroepen om het verhaal te starten
    def Pre_Game_Story(data):
        print(colored("You can write different commands to look around the room (Write HELP for more info WHEN ASKED FOR A COMMAND)...","red",attrs=['bold','underline']))	
        print("\nYou suddenly wake up with the worst headache you have ever had.")
        print("You don't know where you are and you don't know how you got here.")
        print("You only know that you want to climb the mountain and slay the boss.")
        game.room1(data)
    
    def room1(data):
        data["Room"] = 1
        game.WriteJson(data)
        command = input(colored("\nType a valid command... ","green"))
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
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
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
                
            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()
       
            else:
                command = input(colored("\nType a valid command... ","green"))
                
        
        if data["Inventory"]["WinterClothes"] == 0 or data["Inventory"]["Shoes"] == 0:
             print("It is cold outside, check if you can find some clothing and shoes.")
             game.room1(data)
             
        else:
            print("\nYou go through the door and find yourself in a opening in the forest.")
            game.room2(data)
            
        
        
        
        
        
        
    def room2(data):
        data["Room"] = 2
        game.WriteJson(data)
        command = input(colored("\nType a valid command... ","green"))
        while command.lower() != "go path" or command.lower() != "go back":
            
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
                print("\n.When you look around u can see a small shed.\n"
                      "In the distance you see the opening to a path through the forest.")
                command = ""
                
            elif command.lower() == "check Shed":
                print("\nYou check the shed and find a piece of rope and a set of climbing picks.")
                data["Inventory"]["WinterClothes"] = 1
                game.WriteJson(data)
                command = ""
                
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
                
            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()
       
            else:
                command = input(colored("\nType a valid command... ","green"))
        
        if command.lower() == "go back":
                print("\nU go back to where u came from.")
                game.room1(data)
                
        
        elif command.lower() == "go path":
                print(colored("\nYou walk onto the path and stand infront of a decision, will you look around or go further... ","grey"))
                game.subroom2(data)
                
        
    
    
    def subroom2(data):
        data["Room"] = 2.5
        game.WriteJson(data)
        	
        command = input(colored("\nType a valid command... ","green"))
        while command.lower() != "go further" or command.lower() != "go back":
            
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
                print("\n.When you look around u can see that the path is encased in bushes and trees.\n"
                      "Maybe you can find some herbs and wood to help you in your journey")
                command = ""
                
            elif command.lower() == "check bushes":
                print("\nYou check the bushes and find some wood and a maybe few weird herbs.")
                data["Inventory"]["Wood"] += 3
                BurkingBagCounter = int(random(1,100))
                if BurkingBagCounter <= 50:
                    data["Inventory"]["Herbs"] += 2
                elif  BurkingBagCounter > 50 and BurkingBagCounter <= 75:
                    data["Inventory"]["Herbs"] += 5
                else:
                    print("You find no herbs")	
                
                game.WriteJson(data)
                command = ""
                
            elif command.lower() == "check bushes":
                print("\nYou go to the wall and find some shoes which you stash in your inventory.\n"
                    "You also see a weard painting.")
                data["Inventory"]["Shoes"] = 1
                game.WriteJson(data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
                
                
            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()
       
            else:
                command = input(colored("\nType a valid command... ","green"))
        
        if command.lower() == "go back":
            print("\nU go back to where u came from.")
            game.room2(data)
                
        
        elif command.lower() == "go further":
            print(colored("\nYou further on the path and eventually arrive at a steep stone cliff.... ","grey"))
            game.room3(data)
    
    #DEe eerste opstakel waar je tegen aan loopt, en je omhoog klimt
    def room3(data):
        data["Room"] = 3
        game.WriteJson(data)

        print("You feel that you are strong enough to climb up this cliff. Because it seems that it is only ten meters tall.")
        #time.sleep(5)
        command = input(colored("\nType a valid command... ", "green"))
        while command != "go wall":

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
                print("\nYou look around to see if you can find something that you can work with.")
                #if(random.randint(0,100) > 30):
                print("You luckily notice that there is a crack in the wall.")
                print("The wall before you just seems like it got a little taller.")
                print("But it does not seem impossible to climb")
                command = ""
            
            elif command.lower() == "go wall":
                print("\n You walk to the large wall which is only ten meters high.")
                print("You have the confidence to conquer this wall because it is not that tall.")
                print("So you swiftly make your way to the top.\n")
                command = ""

            elif command.lower() == "check crack":
                print("\nYou check the crack that you have previously seen when taking a look around.\n"
                "And you notice that it is just big enough for your body to go through.\n")
                command = ""
            
            elif command.lower() == "go crack":
                print("\nYou manage to squeeze yourself through the crack.")
                game.subroom3(data)
                command = ""
            
            elif command.lower() == "go pathway":
                game.room2(data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.lower() == "previous room":
                game.room2(data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\nType a valid command... ","green"))
        game.room4(data)
        
    #Geheime cave in de eerste muur waar je langs moet klimmen
    def subroom3(data):
        data["Room"] = 3.5
        game.WriteJson(data)
        print("\nYou have entered a subroom of stage 3.")
        command = input(colored("\nType a valid command... ","green"))
        while command != "go crack":
            command2 = command.split()
            
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
                print("You look around the dimly lit cave to see a skeleton leaning against the wall.")
                print("Behind you is the crack where you came through.")
                command = ""

            elif command.lower() ==  "check skeleton":
                print("Upon checking the skeleton you find a small bag containing 200 bronze coins.")
                print("You also find a rusty old sword and an old helmet.\n")
                data["Inventory"]["RustySword"] = 1
                data["Inventory"]["BronzeCoins"] += 200
                data["Inventory"]["OldHelmet"] = 1
                game.WriteJson(data)
                command = ""
            
            elif command.lower() == "go crack":
                print("You are leaving the small cave")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\nType a valid command... ","green"))
        print("You are leaving the small cave")
        game.room3(data)

    def room4(data):
        data["Room"] = 4
        game.WriteJson(data)
        
    #Het bergdorpje
    def room5(data):
        data["Room"] = 5
        game.WriteJson(data)
        print("\nYou have arrived in the miners town of Miners Vale.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command != "go Watchtower":
            command2 = command.split()
            command2[0] = command2[0].lower()
            
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
                print("\nYou take a look around the small miners town and see three handy building.")
                print("The three buildings that are open right now are the tavern, the hotel and the store.")
                print("At the tavern you can have a nice drink for a cheap price and talk with the locals.")
                print("The hotel is obviously for sleeping and you can buy useful items at the store.")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.lower() == "go tavern":
                print("\nYou walk over to the tavern to check it out.")
                game.subroom5_1(data)
                command = ""

            elif command.lower() == "go hotel":
                print("\nYou walk over to the hotel to check if they have a cheap room available for you.")
                game.subroom5_2(data)
                command = ""

            elif command.lower() == "go store":
                print("\nYou walk over to the tavern to check if they have useful items that you can buy for your climb and fight with the evil monsters.")
                game.subroom5_3(data)
                command = ""
            
            elif command.lower() == "go Watchtower":
                print("\nYou leave the village and start walking to the watchtower.")

            elif command.lower() == "previous room":
                game.room4(data)

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))

        print("\nYou leave the village and start walking to the watchtower.")
        game.room6(data)

    #De bar in het hotel bergdorpje
    def subroom5_1(data):
        data["Room"] = 5.1
        game.WriteJson(data)
        print("\nYou arrived in the tavern where you can eat and drink and maybe gather some useful information.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command != "leave tavern":

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
                print("\nYou see two people whilst looking through the tavern.")
                print("One is the bartender and the other is a guest.")
                print("Watch out for the guest thoug, because you have a small chance to end up in a fight")
                command = ""
            
            elif command.lower() == "talk guest":
                print("The guest asks you are you an adventurer, where you answer yes.")
                print("He says to you in an ominous voice: 'Don't climb the mountain, it is dangerous and filled with strong monsters.'")
                print("'If you still plan to go then you need to check out the old watchtower, it is said to contain some nice loot.'")
                print("You thank the guest and go back to your own table")
                command = ""

            elif command.lower() == "talk bartender":
                print("You go talk with the bartender and says that you can buy a meal or a beer. For 100 bronze each")
                print("He asks if you'd like to have something.")
                command = ""
            
            elif command.lower() == "buy beer":
                if (data["Inventory"]["BronzeCoins"] - 100) < 0:
                    print("Insufficient funds")
                    command = ""
                else: 
                    print("You bought a nice beer for 100 bronzecoins and feel your saturation going up.")
                    data["Character"]["Food"] += 20
                    data["Inventory"]["BronzeCoins"] -= 100
                    time.sleep(2)
                    print("Food went up by 20")
                    left = data["Inventory"]["BronzeCoins"]
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""

            elif command.lower() == "buy food":
                if (data["Inventory"]["BronzeCoins"] - 100) < 0:
                    print("Insufficient funds")
                else: 
                    print("You bought yourself a nice and hot meal for 100 bronze and fill yourselves.")
                    data["Character"]["Food"] += 30
                    data["Inventory"]["BronzeCoins"] -= 100
                    time.sleep(2)
                    print("Food went up by 30")
                    left = data["Inventory"]["BronzeCoins"]
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        game.room5()

    #Het hotel in het bergdorpje
    def subroom5_2(data):
        data["Room"] = 5.2
        game.WriteJson(data)
        print("You enter the nice hotel to maybe spend the night.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command != "leave hotel":
            
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
                print("Looking around the hotel lobby you see the helpdesk where you can pay 1 silver to spend the night.")
                command = ""
            
            elif command.lower() == "go helpdesk":
                print("You walk up to the helpdesk and ask if there are any rooms available.")
                print("The nice employee says yes and that a room for the night costs 1 silver.")
                command = ""
            
            elif command.lower() == "buy room":
                if (data["Inventory"]["BronzeCoins"] - 1000) < 0:
                    print("Insufficient funds.")
                else:
                    print("You spend the night in a nice bed.")
                    data["Inventory"]["BronzeCoins"] -= 1000
                    left = data["Inventory"]["BronzeCoins"]
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        game.room5()

    #De winkel in het bergdorpje
    def subroom5_3(data):
        data["Room"] = 5.3
        game.WriteJson(data)
        print("You enter the store to buy some supplies for your journey up the mountain.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command != "leave store":
            
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
                print("\nWhen you take a look around the store you notice that it only sells a large knife, \nbetter armor and an encyclopedia full of pictyres and monsters.")
                print("The knife costs 300 BronzeCoins.")
                print("The armor costs 400 BronzeCoins.")
                print("The encyclopedia costs 500 BronzeCoins.")
                command = ""
            
            elif command.lower() == "buy knife":
                if (data["Inventory"]["BronzeCoins"] - 300) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the large knife and it has been added to your inventory.")
                    data["Inventory"]["BronzeCoins"] -= 300
                    left = data["Inventory"]["BronzeCoins"]
                    data["Inventory"]["LargeKnife"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""

            elif command.lower() == "buy encylopedia":
                if (data["Inventory"]["BronzeCoins"] - 500) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the encyclopedia and it has been added to your inventory.")
                    data["Inventory"]["BronzeCoins"] -= 500
                    left = data["Inventory"]["BronzeCoins"]
                    data["Inventory"]["Encyclopedia"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""
            
            elif command.lower() == "buy armor":
                if (data["Inventory"]["BronzeCoins"] - 300) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the armor and it has been added to your inventory.")
                    data["Inventory"]["BronzeCoins"] -= 300
                    left = data["Inventory"]["BronzeCoins"]
                    data["Invenory"]["Armor"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} BronzeCoins left")
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        game.room5()

    def room6(data):
        data["Room"] = 6
        game.WriteJson(data)

    #Ruimte 7 waar je een puzzel met morsecode moet oplossen om de brug te laten komen en door te kunnen gaan naar de volgende ruimte.
    def room7(data):
        data["Room"] = 7
        game.WriteJson(data)
        print("\nYou suddenly arrive at a big canyon. With a big pedestal in front of you.")
        command = input(colored("\n Type a valid command... ", "green"))
        raadsel = False
        morsecode =  {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 'spatie': '/'}
        while raadsel == False:
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""

            elif command.lower() == "check pedestal":
                print("It seems that you should look for clues in your surrounding area to write the correct sentence.")
                print("A bridge to the other side of the canyon will appear when you write the correct sentence.")
                code = input("What is the correct sentence? ")
                if code.lower() == "open sesame":
                    print("The bridge has extended to your side.")
                    print("You have crossed the canyon to the next area.")
                    raadsel = True
                else:
                    print("Incorrect answer")
                    print("The bridge has not appeared.")
                command = ""

            elif command.lower() == "look":
                print("You also see the pedestal infront of you")
                print("Looking around you, you see a big stone with some weird writing on it.")
                print("There is also this weird looking tree.")
                print("There are also a few bushes.")
                print("And there is a bridge on the other side of the canyon.")
                command = ""
            
            elif command.lower() == "check tree":
                print("This tree seems to have a conversion table for morse code.")
                for key, value in morsecode.items():
                    print(" ",key, value, end="")
                command = ""

            elif command.lower() == "check boulder":
                print("This boulder seems to have a message in some morse code.")
                print("Maybe I can find a conversion table for it.")
                print("--- .--. . -. / ... . ... .- -- .")
                playsound('./' + 'morse.wav')
                command = ""
            
            elif command.lower() == "check bushes":
                print("There seems nothing wrong with the bushes.")
                command = ""
            
            elif command.lower() == "check canyon":
                print("The canyon is very big, but you can see a bridge on the other side.")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        game.room8(data)

    def room8(data):
        data["Room"] = 8
        game.WriteJson(data)


    #Ruimte 9 waar je door middel van een puzzel een ijsklif omhoog moet klimmen
    def room9(data):
        data["Room"] = 9
        game.WriteJson(data)
        print("\n You have arrived at a large clifside made of ice.")
        command = input(colored("\n Type a valid command... ", "green"))
        finish = False
        route = '''
                                 ┌─────┐
                                 │ TOP ├─────┐
                                 └┬────┘     │  
                                  │          │
                                  │          │  
                                  │         ┌┴┐
                   ┌─┐            │ ┌───────┤J│
                   │K├────────┐   │ │       └┬┘
                   └┬┘        │   │ │        │
                    │         │   │ │        │
                    │         │   │ │        │
                    │        ┌┴┬──┘ │       ┌┴┐
                    │        │I│    │       │G├─────┐
                    │        └┬┘    │       └┬┘     │
                    │         │     │        │     ┌┴┐
                    │         │     │        │     │H│
                    │         │     │ ┌──────┘     └─┘
                    │         │    ┌┴┬┘       ┌─┐
                    │         └────┤E├────────┤F│
                    │    ┌─┐       └┬┘        └┬┘
                    │  ┌─┤C│        │          │
                    │  │ └─┤        │          │
                    │  │   │       ┌┴┐        ┌┴┐
                    │  │   └───────┤B├────────┤D│
                    │  │           └┬┘        └─┘
                    │  │            │
                    │  │            │
                    │  └─────┬─┬────┘
                    │        │A│
                    └────────┴─┘
                              X
                    '''#Dit is voor de snakes and ladders puzzel
        while finish == False:
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
                print("You see a large clifside made of ice.")
                print("After inspecting the cliffside you feel confident thast you can climb it.")
                command = ""
            
            elif command.lower() == "check cliffside":#Dit is voor de snakes and ladders puzzel
                print(route)
                climb = input(colored("Do you want to climb the cliffside? (YES or NO) ", "green"))
                if climb.lower() == "yes":
                    print("When climbing your position will be indicated by the letter X.")
                    top = False
                    positie = "Begin"
                    keuze = input("Choose the letter that is connected to the letter you are standing on, \nbut watch out some choices make you fall down... ")
                    while top == False:
                        if keuze.lower() == "a":
                            if positie == "Begin" or positie == "B":
                                route = route.replace("X", positie)
                                route = route.replace("A", "X")
                                positie = "A"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to A")
                            keuze = ""
                        elif keuze.lower() == "b":
                            if positie == "A" or positie == "D" or positie == "E":
                                route = route.replace("X", positie)
                                route = route.replace("B" , "X")
                                route = route.replace("Xegin", "Begin")
                                positie = "B"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to B")
                            keuze = ""
                        elif keuze.lower() == "c":
                            if positie == "B":
                                route = route.replace("X", positie)
                                route = route.replace("C", "X")
                                positie = "C"
                                print(route)
                                print("\nYou notice that C is the wrong choice and you fall down to A.")
                                route = route.replace("X", positie)
                                route = route.replace("A", "X")
                                positie = "A"
                                print(route)
                            elif positie == "A":
                                print("\nC is a slippery slope so you can't climb it via this route.")
                            else:
                                print("\nYou are not on a place that is connected to C")
                            keuze = ""
                        elif keuze.lower() == "d":
                            if positie == "B":
                                route = route.replace("X", positie)
                                route = route.replace("D", "X")
                                positie = "D"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to D")
                            keuze = ""
                        elif keuze.lower() == "e":
                            if positie == "B" or positie == "G" or positie == "I":
                                route = route.replace("X", positie)
                                route = route.replace("E", "X")
                                positie = "E"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to E")
                            keuze = ""
                        elif keuze.lower() == "f":
                            if positie == "E":
                                route = route.replace("X", positie)
                                route = route.replace("F", "X")
                                positie = "F"
                                print(route)
                                print("\nYou notice that F is the wrong choice and you fall down to D.")
                                route = route.replace("X", positie)
                                route = route.replace("D", "X")
                                positie = "D"
                                print(route)
                            elif positie == "D":
                                print("\nYou notice that F is a slippery slope so you can't climb it via this route.")
                            else:
                                print("\nYou are not on a place that is connected to F")
                            keuze = ""
                        elif keuze.lower() == "g":
                            if positie == "E" or positie == "I" or positie == "H":
                                route = route.replace("X", positie)
                                route = route.replace("G", "X")
                                positie = "G"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to G")
                            keuze = ""
                        elif keuze.lower() == "h":
                            if positie == "G":
                                route = route.replace("X", positie)
                                route = route.replace("H", "X")
                                positie = "H"
                                print(route)
                                vraag = input("\nDo you want to check the crack in the wall? (YES or NO)")
                                if vraag.lower() == "yes":
                                    print("You check the secret crack in the wall.")
                                    print("To your surprise you find an iron sword and Iron armor.")
                                    data["Inventory"]["IronSword"] = 1
                                    data["Inventory"]["IronArmor"] = 1
                                    game.WriteJson(data)
                                else:
                                    print("\nYou choose not to enter the cave.")
                            else:
                                print("\nYou are not on a place that is connected to H")
                            keuze = ""
                        elif keuze.lower() == "i":
                            if positie == "TOP" or positie == "E":
                                route = route.replace("X", positie)
                                route = route.replace("I", "X")
                                positie = "I"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to I.")
                            keuze = ""
                        elif keuze.lower() == "j":
                            if positie == "G" or positie == "TOP":
                                route = route.replace("X", positie)
                                route = route.replace("I", "X")
                                positie = "I"
                                print(route)
                                print("\nYou notice that I is the wrong choice and you fall down to E.")
                                route = route.replace("X", positie)
                                route = route.replace("E", "X")
                                positie = "E"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to I")
                            keuze = ""
                        elif keuze.lower() == "k":
                            if positie == "I":
                                route = route.replace("X", positie)
                                route = route.replace("K", "X")
                                positie = "K"
                                print(route)
                                print("\nYou notice that K is the wrong choice and you fall down to G.")
                                route = route.replace("X", positie)
                                route = route.replace("A", "X")
                                positie = "A"
                                print(route)
                            elif positie == "A":
                                print("\nThe route to K is a slippery slope so you can't climb it via this route.")
                            else:
                                print("\nYou are not on a place that is connected to K")
                            keuze = ""
                        elif keuze.lower() == "top":
                            if positie == "I":
                                route = route.replace("X", positie)
                                route = route.replace("TOP", " X ")
                                positie = "TOP"
                                print(route)
                            else:
                                print("\nYou are not on a place that is connected to TOP")
                            keuze = ""
                            top = True
                        else:
                            keuze = input("\nChoose the letter that is connected to the letter you are standing on, \nbut watch out some choices make you fall down... ")
                    print("\nYou have reached the top of the icy cliff.")
                    finish = True
                elif climb.lower() == "no":
                    print("You have chosen not to climb the cliff.")
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""

            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        print("You are going to the next room...")
        game.room10(data)

    def room10(data):
        data["Room"] = 10
        game.WriteJson(data)

    
    
    
    
    #PrintInventory(data)

    #PrintCharacter(data)
    
    #data["Character"]["hp"] = 100
    
    #WriteJson(data)




game.start(game.data)


#16 panelen 1 naast raam 1 bovenaan