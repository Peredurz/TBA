import json
import time
from traceback import print_stack
from termcolor import colored
import random
from playsound import playsound
#https://pypi.org/project/termcolor/ voor meer kleur en text info
#https://asciiflow.com/ om puzzel met ascii te tekenen

class game:

    
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
        for item in data["Inventory"]:
            print(item, ":", data["Inventory"][item]["amount"])
        print()    
            

    
    def PrintCharacter(data):
        print("\nCharacter: \n")
        result = '\n'.join(f'{key}: {value}' for key, value in data["Character"].items())
        print(result)

    def CheckThings(data, info):
        print(info, ":", data["Inventory"][info]["info"], "\nAmount:", data["Inventory"][info]["amount"])
        
    
    def reset(data):
        #Run a for loop over each key in the json file and set it to 0 if that is the desired value
        for  value in dict(data["Character"].items()):
            if value == "Hp" or value == "Food":
                data["Character"][value] = 100
            else:
                data["Character"][value] = 0
        
        for  value in dict(data["Inventory"].items()):
            data["Inventory"][value]["amount"] = 0
            if "equipped" in data["Inventory"][value]:
                data["Inventory"][value]["equipped"] = False
             
        data["Room"] = 0
                  
        game.WriteJson(data)

    #Functie om items te equippen
    def equip(info, data):
        #file = open("game.json", "r")
        #items = json.load(file)
        #e = info
        for item in data:
            if "Inventory" in item:
                for item2 in data["Inventory"]:
                    if info in item2:
                        data["Inventory"][info]["equipped"] = True
                        print("You have equipped the", info)
                        game.WriteJson(data)
    
    def unequip(info, data):
        #file = open("game.json", "r")
        #items = json.load(file)
        #e = info
        for item in data:
            if "Inventory" in item:
                for item2 in data["Inventory"]:
                    if info in item2:
                        data["Inventory"][info]["equipped"] = False
                        print("You have unequipped the", info)
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
                        if e == "Bread" and data["Inventory"][e] > 0 and data["Character"]["Food"] < 100:
                            data["Character"]["Food"] += 20
                            data["Inventory"][e]["amount"] -= 1
                            if data["Character"]["Food"] >= 100:
                                data["Character"]["Food"] = 100
                                print("You are full")
                            print("You have eaten", e)
                            game.WriteJson(data)
                        elif e == "DriedMeat" and data["Inventory"][e] > 0 and data["Character"]["Food"] < 100:
                            data["Character"]["Food"] += 30
                            data["Inventory"][e]["amount"] -= 1
                            if data["Character"]["Food"] >= 100:
                                data["Character"]["Food"] = 100
                                print("You are full")
                            print("You have eaten", e)
                            game.WriteJson(data)
                        elif e == "Meat" and data["Inventory"][e] > 0 and data["Character"]["Food"] < 100:
                            data["Character"]["Food"] += 40
                            data["Inventory"][e]["amount"] -= 1
                            if data["Character"]["Food"] >= 100:
                                data["Character"]["Food"] = 100
                                print("You are full")
                            print("You have eaten", e)
                            game.WriteJson(data)
                        elif e == "Water" and data["Inventory"][e] > 0 and data["Character"]["Food"] < 100:
                            data["Character"]["Food"] += 5
                            data["Inventory"][e]["amount"] -= 1
                            if data["Character"]["Food"] >= 100:
                                data["Character"]["Food"] = 100
                                print("You are full")
                            print("You have drunk", e)
                            game.WriteJson(data)
    
    def fight(data, enemy):
        print("You have encountered a", enemy)
        gevecht = input(colored("Attack, Defend or Heal?","red"))
        if enemy != "Boss":
            #randint between 100 and 200 with with steps of 5
            enemyhp = random.randrange(100, 201, 5)
        elif enemy == "Wendigo":
            enemyhp = random.randrange(200, 301, 5)
        else:
            enemyhp = 500
        if data["Inventory"]["RustySword"]["equipped"] == True:
            damage = 10
        elif data["Inventory"]["IronSword"]["equipped"] == True:
            damage = 20
        elif data["Inventory"]["SteelSword"]["equipped"] == True:
            damage = 30
        else:
            damage = 5
        while enemyhp > 0 :
            print(f"The {enemy} has {enemyhp} hp left and you have {data['Character']['Hp']} hp left")
            if gevecht.lower() == "attack":
                rand = random.randrange(1, 3)
                if rand == 2:
                    print("You have succesfully attacked")
                    enemyhp -= damage
                    print("The enemy has", enemyhp, "hp left")
                elif rand == 1 or rand == 3:
                    print("You have failed to attack")
                    data["Character"]["Hp"] -= 10
                gevecht = ""
            elif gevecht.lower() == "defend":
                rand = random.randrange(1, 3)
                if rand == 2:
                    print("You have succesfully defended")
                else:
                    print("You have failed to defend")
                    data["Character"]["Hp"] -= 5
                    print("You have taken 10 damage")
                    game.WriteJson(data)
                gevecht = ""
            elif gevecht.lower() == "heal":
                while data["Inventory"]["Herbs"]["amount"] > 2:
                    data["Inventory"]["Medicine"]["amount"] += 1
                    data["Inventory"]["Herbs"]["amount"] -= 2
                    print(f"You have {data['Inventory']['Medicine']} medicine")
                    game.WriteJson(data)
                if data['Inventory']['Medicine']["amount"] > 1 and data["Character"]["Hp"] < 100:
                    data["Character"]["Hp"] += 25
                    data["Inventory"]["Medicine"]["amount"] -= 1
                    
                elif  data["Character"]["Hp"] >= 100:
                    print("You havent taken any damage")
                else:
                    print("You dont have enough medicine")
                gevecht = ""
            else:
                data["Character"]["Hp"] -= 10
                gevecht = input(colored("Attack, Defend or Heal?","red"))
        if enemyhp <= 0 and enemy != "Boss":
            print("You have defeated the", enemy)
            game.LoadRoom(data)
        elif enemyhp <= 0 and enemy == "Boss":
            print("You have defeated the", enemy)
            print("You have won the game")
            game.EndScreen(data)
    
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
        elif data["Room"] == 6.1:
            game.subroom6_1(data)
        elif data["Room"] == 6.2:
            game.subroom6_2(data)
        elif data["Room"] == 7:
            game.room7(data)
        elif data["Room"] == 8:
            game.room8(data)
        elif data["Room"] == 9:
            game.room9(data)
        elif data["Room"] == 10:
            game.room10(data)
        elif data["Room"] == 10.1:
            game.subroom10_1(data)

        else:
            game.roomboss(data)

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
        print("INSPECT: to inspect an item")
        print("CHARACTER: to see your character")
        print("LOOK: to look around the room")
        print("GO: if you write go and then a statement that has been said when looking around a room you can go check that place.")
        print("EAT: to eat something")
        print("DRINK: to drink something")
        print("FIGHT: to fight a monster")
        print("TALK: to talk to a character")
        print("PICKUP: to pick up an item")
        print("EQUIP: to equip an item")
        print("UNEQUIP: to unequip an item")
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
        data["Character"]["Name"] = input(colored("What is the name you want to give your character? ","green"))	
        game.WriteJson(data)
        
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
                
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
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
                data["Inventory"]["WinterClothes"]["amount"] += 1
                data["Inventory"]["Coins"] += 400
                game.WriteJson(data)
                command = ""
                
            elif command.lower() == "check wall":
                print("\nYou go to the wall and find some shoes which you stash in your inventory.\n"
                    "You also see a weard painting.")
                data["Inventory"]["Shoes"]["amount"] += 1
                game.WriteJson(data)
                command = ""
            
            elif command.lower() == "check painting":
                print("\n You check the painting and find that there is nothing wrong with it.")
                print("You find that the painting is a beautiful painting of the mountains right outside this cottage.")
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
                
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
                
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
                
            elif command.lower() == "check fridge":
                print("\nYou check the fridge and find some nice food to take with you on the journey.")
                data["Inventory"]["Bread"]["amount"] += 1
                data["Inventory"]["Water"]["amount"] += 4
                data["Inventory"]["Meat"]["amount"] += 3
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
                
        
        if data["Inventory"]["WinterClothes"]["amount"] == 0 or data["Inventory"]["Shoes"]["amount"] == 0:
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
                
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                print("\n.When you look around u can see a small shed.\n"
                      "In the distance you see the opening to a path through the forest.")
                command = ""
                
            elif command.lower() == "check Shed":
                print("\nYou check the shed and find a piece of rope and a set of climbing picks.")
                data["Inventory"]["WinterClothes"]["amount"] = 1
                game.WriteJson(data)
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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

            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
                
            elif command.lower() == "look":
                print("\n.When you look around u can see that the path is encased in bushes and trees.\n"
                      "Maybe you can find some herbs and wood to help you in your journey")
                command = ""
                
            elif command.lower() == "check bushes":
                print("\nYou check the bushes and find some wood and a maybe few weird herbs.")
                data["Inventory"]["Wood"]["amount"] += 3
                BurkingBagCounter = int(random(1,100))
                if BurkingBagCounter <= 50:
                    data["Inventory"]["Herbs"]["amount"] += 2
                elif  BurkingBagCounter > 50 and BurkingBagCounter <= 75:
                    data["Inventory"]["Herbs"]["amount"] += 5
                else:
                    print("You find no herbs")	
                
                game.WriteJson(data)
                command = ""
                
            elif command.lower() == "check bushes":
                print("\nYou go to the wall and find some shoes which you stash in your inventory.\n"
                    "You also see a weard painting.")
                data["Inventory"]["Shoes"]["amount"] = 1
                game.WriteJson(data)
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
                command = input(colored("\nType a valid command... ","green"))
        
        if command.lower() == "go back":
            print("\nU go back to where u came from.")
            game.room2(data)
                
        
        elif command.lower() == "go further":
            print(colored("\nYou further on the path and eventually arrive at a steep stone cliff.... ","grey"))
            game.room3(data)
    
    #De eerste opstakel waar je tegen aan loopt, en je omhoog klimt
    def room3(data):
        data["Room"] = 3
        game.WriteJson(data)

        print("You feel that you are strong enough to climb up this cliff. Because it seems that it is only ten meters tall.")
        #time.sleep(5)
        command = input(colored("\nType a valid command... ", "green"))
        while command.lower() != "go wall":

            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""

            elif command.lower() == "look":
                print("\nYou look around to see if you can find something that you can work with.")
                #if(random.randint(0,100) > 30):
                print("You luckily notice that there is a crack in the wall.")
                print("The wall before you just seems like it got a little taller.")
                print("But it does not seem impossible to climb")
                command = ""
            
            elif command.lower() == "climb wall":
                print("\n You walk to the large wall which is only ten meters high.")
                print("You have the confidence to conquer this wall because it is not that tall.")
                
                break 

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
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
                command2 = command.split()
                game.food(command2[1], data)
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
        
        if command == "climb wall":
            if data["Inventory"]["climbing picks"]["amount"] >= 1:
                print("\nYou climb the wall with the help of your climbing picks.")
                
                game.room4(data)
            else:
                print("\nYou can't climb the wall with your bare hands.")
                game.room3(data)
        else:
            if data["Inventory"]["climbing picks"]["amount"] >= 1:
                print("\nYou climb the wall with the help of your climbing picks.")
                
                game.room4(data)
            else:
                print("\nYou can't climb the wall with your bare hands.")
                game.room3(data)

    
    #Geheime cave in de eerste muur waar je langs moet klimmen
    def subroom3(data):
        data["Room"] = 3.5
        game.WriteJson(data)
        print("\nYou have entered a subroom of stage 3.")
        command = input(colored("\nType a valid command... ","green"))
        while command.lower() != "go crack":
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
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
                
            elif command.lower() == "look":
                print("You look around the dimly lit cave to see a skeleton leaning against the wall.")
                print("Behind you is the crack where you came through.")
                command = ""

            elif command.lower() ==  "check skeleton":
                print("Upon checking the skeleton you find a small bag containing 700 coins.")
                print("You also find a rusty old sword and an old helmet.\n")
                data["Inventory"]["RustySword"]["amount"] = 1
                data["Inventory"]["Coins"]["amount"] += 700
                data["Inventory"]["OldHelmet"]["amount"] = 1
                game.WriteJson(data)
                command = ""
            
            elif command.lower() == "go crack":
                print("You are leaving the small cave")
                command = ""

            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
                command = input(colored("\nType a valid command... ","green"))
        print("You are leaving the small cave")
        game.WriteJson(data)
        game.room3(data)

    def room4(data):
        data["Room"] = 4
        game.WriteJson(data)
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "go further":
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
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
                
            elif command.lower() == "search herbs":
                timeToSeek = input(" How long do you want to search for herbs? (1-10) ")
                for i in range(int(timeToSeek)):
                    print("Searching for herbs...")
                    randomHerbNumber = random.randrange(0, 11,2)
                    data["Inventory"]["Herbs"]["amount"] += (randomHerbNumber*2)
                    time.sleep(1)
                command = ""
            
            elif command.lower() == "save":
                command = ""
                game.save(data)
                
            
            elif command.lower() == "exit":
                print(colored("Exiting game...","red"))
                exit()

            else:
                command = input(colored("\n Type a valid command... ", "green"))
        
        game.room5(data)
        
        
    #Het bergdorpje
    def room5(data):
        data["Room"] = 5
        game.WriteJson(data)
        print("\nYou have arrived in the miners town of Miners Vale.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "go Watchtower":
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
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                print("\nYou take a look around the small miners town and see three handy building.")
                print("The three buildings that are open right now are the tavern, the hotel and the store.")
                print("At the tavern you can have a nice drink for a cheap price and talk with the locals.")
                print("The hotel is obviously for sleeping and you can buy useful items at the store.")
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
                command2 = command.split()
                game.food(command2[1], data)
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
        while command.lower() != "leave tavern":

            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
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
                print("You go talk with the bartender and says that you can buy a meal or a beer. For 100 coins each")
                print("He asks if you'd like to have something.")
                command = ""
            
            elif command.lower() == "buy beer":
                if (data["Inventory"]["Coins"]["amount"] - 100) < 0:
                    print("Insufficient funds")
                    command = ""
                else: 
                    print("You bought a nice beer for 100 coins and feel your saturation going up.")
                    data["Character"]["Food"] += 20
                    data["Inventory"]["Coins"]["amount"] -= 100
                    time.sleep(2)
                    print("Food went up by 20")
                    left = data["Inventory"]["Coins"]["amount"]
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""

            elif command.lower() == "buy food":
                if (data["Inventory"]["Coins"]["amount"] - 100) < 0:
                    print("Insufficient funds")
                else: 
                    print("You bought yourself a nice and hot meal for 100 coins and fill yourselves.")
                    data["Character"]["Food"] += 30
                    data["Inventory"]["Coins"]["amount"] -= 100
                    time.sleep(2)
                    print("Food went up by 30")
                    left = data["Inventory"]["Coins"]["amount"]
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
                
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        game.room5()

    #Het hotel in het bergdorpje
    def subroom5_2(data):
        data["Room"] = 5.2
        game.WriteJson(data)
        print("You enter the nice hotel to maybe spend the night.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "leave hotel":
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""

            elif command.lower() == "look":
                print("Looking around the hotel lobby you see the helpdesk where you can pay 500 coins to spend the night.")
                command = ""
            
            elif command.lower() == "go helpdesk":
                print("You walk up to the helpdesk and ask if there are any rooms available.")
                print("The nice employee says yes and that a room for the night costs 500 coins.")
                command = ""
            
            elif command.lower() == "buy room":
                if (data["Inventory"]["Coins"]["amount"] - 500) < 0:
                    print("Insufficient funds.")
                    
                else:
                    print("You spend the night in a nice bed.")
                    data["Inventory"]["Coins"]["amount"] -= 500
                    left = data["Inventory"]["Coins"]["amount"]
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""

            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        game.room5()

    #De winkel in het bergdorpje
    def subroom5_3(data):
        data["Room"] = 5.3
        game.WriteJson(data)
        print("You enter the store to buy some supplies for your journey up the mountain.")
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "leave store":
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                print("\nWhen you take a look around the store you notice that it only sells a large knife, \nbetter armor and an encyclopedia full of pictyres and monsters.")
                print("The knife costs 300 Coins.")
                print("The armor costs 400 Coins.")
                print("The encyclopedia costs 500 Coins.")
                command = ""
            
            elif command.lower() == "buy knife":
                if (data["Inventory"]["Coins"]["amount"] - 300) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the large knife and it has been added to your inventory.")
                    data["Inventory"]["Coins"]["amount"] -= 300
                    left = data["Inventory"]["Coins"]["amount"]
                    data["Inventory"]["LargeKnife"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""

            elif command.lower() == "buy encylopedia":
                if (data["Inventory"]["Coins"]["amount"] - 500) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the encyclopedia and it has been added to your inventory.")
                    data["Inventory"]["Coins"]["amount"] -= 500
                    left = data["Inventory"]["Coins"]["amount"]
                    data["Inventory"]["Encyclopedia"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""
            
            elif command.lower() == "buy armor":
                if (data["Inventory"]["Coins"]["amount"] - 300) < 0:
                    print("Insufficient funds.")
                else:
                    print("You bought the armor and it has been added to your inventory.")
                    data["Inventory"]["Coins"]["amount"] -= 300
                    left = data["Inventory"]["Coins"]["amount"]
                    data["Invenory"]["Armor"] = 1
                    game.WriteJson(data)
                    print(f"You have {left} Coins left")
                command = ""

            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        game.room5()

    def room6(data):
        data["Room"] = 6
        data["Character"]["Food"] -= 10
        game.WriteJson(data)
        
        print(f"You see the old guard tower in the distance.")
        print(f"You walk up to the guard tower and see that it is deserted.")
        
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "go path":
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                print("Looking around you see the old guard tower has multiple stories and is in a bad shape.")
                print("You see the tower has a staricase leading down into a dungeon and a door leading up to the top of the tower.")
                print("You also see a path leading up the mountain.")
                command = ""
            
            elif command.lower() == "go down":
                print("You walk down the staircase and enter the dungeon.")
                break
            
            
            elif command.lower() == "go up":
                print("You walk up the staircase and enter the top of the tower.")
                break

            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        
        
        if command.lower() == "go down":
            game.subroom6_1(data)
        
        elif command.lower() == "go up":
            game.subroom6_2(data)
                
        else:
            print(colored("\nYou go further on the path and eventually arrive at a steep stone cliff.... ","grey"))
            game.room7(data)   
        


    def subroom6_1(data):
        data["Room"] = 6.1
        game.WriteJson(data)
        print("You walk down the staircase and enter the dungeon.")
        print("You see a three large metal doors on your left and a small door on your right.")
        print(colored(f"To go into the seperate rooms use: go door1, go door2 and so on.","red"))
        if randomFightRoom != 0:
            randomFightRoom = random.randint(1, 3)
        
        command = input(colored("\n Type a valid command... ", "green"))
        
        while command.lower() != "Go back":
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
                
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                print("You see a three large metal doors on your left and a small door on your right.")
                print(colored(f"To go into the seperate rooms use: go door1, go door2 and so on.","green"))
                command = ""
            
            elif command.lower() == "go room1":
                if randomFightRoom == 1:
                    print(colored("You walk into the room and see a skeleton. It tries to attacks you.","red"))
                    randomFightRoom = 0
                    game.fight(data, "Skeleton")
                    
                elif randomFightRoom == 2:
                    print("You find that the room is empty")
                    pass
                
                else:
                    print("You find 70 coins in the room.")
                    data["Inventory"]["Coins"]["amount"] += 70

                command = ""
            
            
            elif command.lower() == "go room2":
                if randomFightRoom == 2:
                    print(colored("You walk into the room and see a skeleton. It tries to attacks you.","red"))
                    randomFightRoom = 0
                    game.fight(data, "Skeleton")
                    
                elif randomFightRoom == 1:
                    print("You find that the room is empty")
                    pass
                
                else:
                    print("You find 70 coins in the room.")
                    data["Inventory"]["Coins"]["amount"] += 70    
                
                
                command = ""
            
            elif command.lower() == "go room3":
                if randomFightRoom == 3:
                    print(colored("You walk into the room and see a skeleton. It tries to attacks you.","red"))
                    randomFightRoom = 0
                    game.fight(data, "Skeleton")
                elif randomFightRoom == 2:
                    print("You find that the room is empty")
                    pass
                
                else:
                    print("You find 70 coins in the room.")
                    data["Inventory"]["Coins"]["amount"] += 70
                
                command = ""
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
                
        print("You walk back down the stairs.")
        
        game.room6(data)        
                
                
    def subroom6_2(data):
        data["Room"] = 6.1
        game.WriteJson(data)
        
        command = input(colored("\n Type a valid command... ", "green"))
        while command.lower() != "go back":
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
            
            elif command.lower() == "look":
                if data["Inventory"]["OldHelmet"]["amount"] == 1:
                    print("Looking around you see a old chest with the same emblem as the old helmet you found.")
                    print("The lock has a code consisting of 5 letters.")
                else:
                    print("Looking around you see a old chest with emblem u dont regognize, maybe you missed something.")
                
                command = ""
            
            elif command.lower() == "check chest":
                print("You go to enter the code to open the chest.")
                
                ChestCode = input(colored("\n Type the code for the chest... ", "green"))
                
                while ChestCode != data["Inventory"]["OldHelmet"]["Code"]:
                    print(colored("To stop trying type: stop.","red"))
                    if ChestCode.lower() == "stop":
                        break
                    else:
                        print("The code is incorrect. Look for clues and try again")
                        ChestCode = input(colored("\n Type the code for the chest... ", "green"))
                    ChestCode = ""
                    
                
                print("The chest opens and you find a old bow with some arrows.")
                data["Inventory"]["OldBow"]["amount"] = 1
                data["Inventory"]["Encyclopedia"]["amount"] = 1
                
                command = ""
            

            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""

            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        
        print("You walk back down the stairs.")
        
        game.room6(data)
        

        
    
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

            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
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
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        game.room9(data)

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
            
            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
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
                                    data["Inventory"]["IronSword"]["amount"] = 1
                                    data["Inventory"]["IronArmor"]["amount"] = 1
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
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""
            
            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
        name = data["Character"]["Name"]
        turnsleft = 8

        print(colored("\nYou enter a big hallway with a floating orb in the middle, when you approach it it talks to you:\n", "green"))
        print(colored(f"Hello there {name}, I am the orb of knowledge, I will only let you through the door if u guess the word correctly.\nYou only have {turnsleft} guesses before I reset you to the beginning of your adventure, so choose wisely.", "blue"))
        print(colored("You can find clues about the word in the room behind u.\n", "blue"))
        print(colored("Good luck!", "blue"))
        
        print(colored("To enter the rooms use the 'go' command with: room","grey"))
        print(colored("To play the game type: play, if u want to stop playing and look around in the rooms use the commands abouve and in the HELP function","grey"))
        
        GuessWordSentence = "The smartest gamer was born today"
        GuessStringList = list(GuessWordSentence)
        printstring = ""
        for i in range(len(GuessStringList)):
            if GuessStringList[i] != " ":
                printstring += "."
            else:
                printstring += "-"
                
        
        CompletedPuzzle = False
        
        
        command = input(colored("\nType a valid command... ", "green"))        
        while command.lower() != "go back" and CompletedPuzzle == False:
            
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""

            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
                
            elif command.lower() == "go room":
                game.subroom10_1(data)
                command = ""

            elif command.lower() == "play":
                #hangman code
                print(printstring)
                if turnsleft != 0:
                    playcommand = input(colored("\n Type a letter, or type 'guess word' to guess the complete sentence. type 'stop' to stop guessing look for clues.\n'-' signifies a space character.\nType now:", "green"))
                    while playcommand.lower() != "stop":
                        
                        if playcommand.lower() == "guess sentence" or playcommand.lower() == "guess word":
                            guess = input(colored("\nType the sentence you think is the correct answer. ", "green"))
                            if guess.lower() == GuessWordSentence.lower():
                                print(colored("\nYou guessed the sentence correctly, you may pass.", "grey"))
                                CompletedPuzzle = True
                                break
                            else:
                                print(colored("\nYou guessed the sentence wrong, try again.", "green"))
                                turnsleft -= 1
                                print(f"{turnsleft} turns left.")	
                                playcommand = ""
                        
                        elif len(playcommand.lower()) == 1:
                            if playcommand.lower() in GuessStringList:
                                
                                for i in range(len(GuessStringList)):
                                    
                                    if GuessStringList[i].lower() == playcommand.lower():
                                        printstring = printstring[:i] + GuessStringList[i] + printstring[i+1:]
                                print(colored("\nYou guessed a letter correctly, try again.", "green"))
                                print(colored("\n" + printstring, "white"))
                                playcommand = ""
                                
                            else:
                                print(colored("\nYou guessed the letter wrong, try again.", "green"))
                                turnsleft -= 1
                                print(f"{turnsleft} turns left.")
                                playcommand = ""
                        else:
                            playcommand = input(colored("Type a valid command or letter: ", "green"))
                            
                    if CompletedPuzzle != True:
                        print(colored("\nYou have stopped guessing, you may now look for clues in the rooms.", "grey"))           
                        pass
                    else:
                        pass
                else:
                    print(colored("\nYou have no more guesses left, you have to start over.", "red"))
                    break
                       
                command = ""
            
            
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
                command = input(colored("\nType a valid command... ", "green"))
                
        if CompletedPuzzle == True:
            print("You are going to the next room...")
            game.roomboss(data)
        elif command.lower() == "go back":
            print("You are going back to the last room...")
            game.room9(data)
        else:
            game.room1(data)
    
    
    
    
    def subroom10_1(data):
        data["Room"] = 10.1
        game.WriteJson(data)
        
        print(colored("You enter a room with a big bookshelf, you see a book with the title 'The smartest gamer; the life óf' on it.\nYou also see a big painting.\nYou also see a calendar.", "white"))
        
        Painting = """
 ┌─────────────────────────────────────────────────────────────────────────┐
 │┼───────────────────────────────────────────────────────────────────────┼│
 ││                                                                       ││
 ││                                                                       ││
 ││          ,███████,                                                    ││
 ││                                                                       ││
 ││         █████████▌                                                    ││
 ││                                                                       ││
 ││         ██████████                                                    ││
 ││                                                                       ││
 ││         ██████████▀                                                   ││
 ││                                                                       ││
 ││          █████████                                                    ││
 ││                                                                       ││
 ││        ,████████`                                                     ││
 ││                                                                       ││
 ││  ╓█   █████████▌                                      ,▀              ││
 ││                                                                       ││
 ││  ████████████████,                                   ,▀               ││
 ││                                                                       ││
 ││   ████████████████╕                                 ╒▀                ││
 ││                                                                       ││
 ││   ╘████████████████                                ,▌                 ││
 ││                                                                       ││
 ││    ████████████████▌          ,╓█████             ╒▌     █████        ││
 ││                                                                       ││
 ││     ▀█████████████████████████████▀▀██▌          ╒█      ████▌╛       ││
 ││                                                                       ││
 ││      █████████████████████▀███████████████████████████████████████    ││
 ││                                                                       ││
 ││      ███████████████████,█─»« ▓▓▓ ▓▓ ▓▓ ▓▓ ▓██████████████████████    ││
 ││                                                                       ││
 ││     ╒██████████████████████████████  "*⌐│  ' ] ▀██████████████████    ││
 ││                                                                       ││
 ││     ██████████████████████████████████`     `  ███████████████████    ││
 ││                                                                       ││
 ││     ███████████████████████████████████        j██████████████████    ││
 ││                                                                       ││
 ││     ███▌ █████████████████████████████▌        j██████████████████    ││
 ││                                                                       ││
 ││     █▌ ███████████████████████████████         j██████████████████    ││
 ││                                                                       ││
 ││     ▀█████████████████████████████████         j██████████████████    ││
 ││                                                                       ││
 ││         ██▀█▀▀▀▀▀██▀███`    .█████████         j██████████████████    ││
 ││                                                                       ││
 ││                  ██         █████████          j██████████████████    ││
 ││                                                                       ││
 ││                  ███        ████████           j██████████████████    ││
 ││                                                                       ││
 ││                  ███       █████████           j██████████████████    ││
 ││                                                                       ││
 ││                 ████      ██████████           j██████████████████    ││
 ││                                                                       ││
 ││        ,██████████████████████████████         j██████████████████    ││
 ││                                                                       ││
 ││       ███ ███  ███████  ██████████████████,    j██████████████████    ││
 ││                                                                       ││
 ││       ▀▀▌ ███           ██▌ ▀██    █▀██████    j██████████████████    ││
 ││                                                                       ││
 ││                                                                       ││
 ││                                                                       ││
 ││                                                                       ││
 │┼───────────────────────────────────────────────────────────────────────┼│
 └─────────────────────────────────────────────────────────────────────────┘
"""
        command = input(colored("\nType a valid command... ", "green"))
        while command.lower() != "go back":
            if command.lower() == "help":
                game.help()
                command = ""
                
            elif command.lower() == "inventory":
                game.PrintInventory(data)
                command = ""
                
            elif command.lower() == "character":
                game.PrintCharacter(data)
                command = ""

            elif command.lower().__contains__("inspect"):
                command2 = command.split()
                game.CheckThings(data, command2[1])
                command = ""
                
            elif command.lower() == "check painting":
                print(colored(Painting, "white"))
                command = ""
                
            elif command.lower() == "check book":
                data["Inventory"]["book"] = 1
                game.WriteJson(data)
                print(colored("The book tells a tale about a prophecy of a gamer to come: the one to defeat the boss and finally free the world of its wrath", "white"))
                print(colored("to read the book use the inventory commands", "grey"))
                command = ""
            
            elif command.lower() == "check calendar":
                ClueString = colored("The calendar looks really old and after turning the pages u see a red circle around a date...", "white")
                ClueString += colored(" today's date", "white", attrs=["bold", "underline"])	
                print(ClueString)
                command = ""               
                
                
            elif command.__contains__("unequip") or command.__contains__("UNEQUIP"):
                command2 = command.split()
                game.unequip(command2[1], data)
                command = ""

            elif command.__contains__("equip") or command.__contains__("EQUIP"):
                command2 = command.split()
                game.equip(command2[1], data)
                command = ""
            
            elif command.__contains__("eat") or command.__contains__("EAT"):
                command2 = command.split()
                game.food(command2[1], data)
                command = ""
            
            elif command.__contains__("drink") or command.__contains__("DRINK"):
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
                command = input(colored("\nType a valid command... ", "green"))
                
        
        print("You are going back to the last room...")
        game.room10(data)
            
    def roomboss(data):
        data["Room"] = 11
        game.WriteJson(data)
        
        print(colored("As you walk through the door it suddenly closes behind u.\nThe ground starts to shake as a Big and Ugly creature rises from the ground and starts to attack you.", "white"))
        game.fight(data, "Boss")
    
    def EndScreen(data):
        print(colored("The monster has finally been defeated and the world is free to live on in peace.","yellow"))
        
        
        game.PrintCharacter(data)
        game.PrintInventory(data)
        
        game.reset(data)
        quit()
            

            


game.start(game.data)


#16 panelen 1 naast raam 1 bovenaan