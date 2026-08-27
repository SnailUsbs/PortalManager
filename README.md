# PortalManager
A python based mod manager for portal 1

I got tired of constantly having to manually swap out mods in Portal 1, so I went ahead and made a simple cross platform mod manager for it.  

# Features

- **Start Game Button:** In program button to start the game

- **Custom Models/Skins:** Portal Manager supports custom portal guns, portals, chell models, glados models, turret models, and companion models.

# How It Works:

- **Portal Manager Folder:** PortalManager will make its own folder inside of your portal game folder. Inside of this PortalManager folder there are sub folders for the various types of mods. We place our mods here, as only one type of each mod can be "active" at one time, like only having one custom portal gun mod alongside one custom portal mod. The sub folders allows the program to easily swap out these mods into your actual game with the click of button, without deleting anything.

- **PMInfo.txt:** This is a text file that goes in the root of every mod, telling PortalManager what type of mod it is. If the mod doesn't already have a PMInfo file inside of it, then PortalManager will make one itself when you move a mod into it's specific folder, like a portal gun mod into the *PortalGuns* folder

- **Custom Textures/Models/SkinsL** Portal Manager supports custom portal guns, portals, chell models, glados models, turret models, and companion models. It does this by first checking every mod in the "custom" folder of your portal game, which is where your active mods are stored. If it finds an active mod of the same type of the one you are currently trying to make active, i.e a portal gun mod, then PortalManager will first move the already active mod over to the PortalManager Mods folder, and then it will move over the mod that you just selected to make active.

## Future Features:

- General Game File support
- Custom map support (just handles auto installing it, with an easy delete option)
- Custom Texture Support
- Custom GUI Support
- Custom Effects Support
- Godot Based Version (Way better GUI, while still working on linux/windows with almost no code changes)

## Important Info

- **Why Make This?:** Mods that are required to go into the "custom" folder replace things in the game, so you can't have more than 1 type of mod replacing the same thing. This means every time you want to switch your portal's looks, the portal gun, the turrets, etc, you will have to take out what you have in there to begin with, and then add in the new mod you want. This process makes it very easy to lose mods over time, and is just annoying to work with, so PortalManager fixes that 

- **Why Python?:** Python easily works across both windows and linux, while also making the project extremely easy to edit. We aren't doing any injecting or heavy mod setups, just moving and managing files/folders, so python is perfect for this. 
