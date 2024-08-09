import tkinter as tk
from configparser import ConfigParser, NoOptionError, NoSectionError
import os

NAHOBINO_BLUE = "#5b87d5"
VENGEANCE_PURPLE = "#a698dd"

#Creates page system with important information like randomize button always visible
def createGUI(configSettings):
    window = tk.Tk()
    window.geometry('1000x700+50+50')
    persistentFrame = tk.Frame(window, width=1000, height=170)
    persistentFrame.grid(row=0, column=0)
    persistentFrame.pack_propagate(False)
    page1Frame = tk.Frame(window, width=1000, height=500, background="#cccccc")
    page1Frame.grid(row=1, column=0)
    page1Frame.pack_propagate(False)
    page2Frame = tk.Frame(window, width=1000, height=500, background="#cccccc")
    page2Frame.grid(row=1, column=0)
    page2Frame.pack_propagate(False)
    pages = [page1Frame, page2Frame]
    buttonControlsFrame = tk.Frame(window, width=350, height=30)
    buttonControlsFrame.grid(row=2, column=0)
    buttonControlsFrame.pack_propagate(False)
    persistentFrameLeft = tk.Frame(persistentFrame, width=500, height=170)
    persistentFrameLeft.grid(row=1, column=0)
    persistentFrameLeft.pack_propagate(False)
    persistentFrameRight = tk.Frame(persistentFrame, width=500, height=170)
    persistentFrameRight.grid(row=1, column=1)
    persistentFrameRight.pack_propagate(False)
    page1FrameTop = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameTop.grid(row=0, column=0, columnspan = 1, sticky = tk.W+tk.E)
    page1FrameTop.pack_propagate(False)
    page1FrameTopLeft = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameTopLeft.grid(row=0, column=1, columnspan = 1, sticky = tk.W+tk.E)
    page1FrameTopLeft.pack_propagate(False)
    page1FrameLeft = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameLeft.grid(row=1, column=0)
    page1FrameLeft.pack_propagate(False)
    page1FrameRight = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameRight.grid(row=1, column=1)
    page1FrameRight.pack_propagate(False)
    page2FrameLeft = tk.Frame(page2Frame, width=500, height=500, background="#cccccc")
    page2FrameLeft.grid(row=0, column=0)
    page2FrameLeft.pack_propagate(False)
    page2FrameRight = tk.Frame(page2Frame, width=500, height=500, background="#cccccc")
    page2FrameRight.grid(row=0, column=1)
    page2FrameRight.pack_propagate(False)
        
    def randomizeClick():
        window.quit()
        
    #Changes the active page and sets interactability of navigation buttons accordingly
    def switchPage(pageIndex):
        if pageIndex < 0 or pageIndex >= len(pages):
            return
        pageButtons[currentPage.get()].config(state=tk.NORMAL)
        pageButtons[pageIndex].config(state=tk.DISABLED)
        currentPage.set(pageIndex)
        if pageIndex == 0:
            leftButton.config(state=tk.DISABLED)
        else:
            leftButton.config(state=tk.NORMAL)
        if pageIndex == len(pages) - 1:
            rightButton.config(state=tk.DISABLED)
        else:
            rightButton.config(state=tk.NORMAL)
        pages[pageIndex].tkraise()
        
    def previousPage():
        switchPage(currentPage.get() - 1)
            
    def nextPage():
        switchPage(currentPage.get() + 1)

    randomizeButton = tk.Button( #Button to start the randomizer
        persistentFrameLeft,
        text="Randomize!",
        width=25,
        height=5,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=randomizeClick,
    )
    randomizeButton.pack()
        
    leftButton = tk.Button( #Button to go to the previous page
        buttonControlsFrame,
        text="<-",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        state=tk.DISABLED,
        command=previousPage,
    )
    leftButton.pack(side=tk.LEFT)
        
    rightButton = tk.Button( #Button to go to the next page
        buttonControlsFrame,
        text="->",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=nextPage,
    )
    rightButton.pack(side=tk.RIGHT)
        
    page1Button = tk.Button( #Button to go to page 1
        buttonControlsFrame,
        text="Page 1",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        state=tk.DISABLED,
        command=lambda pageIndex=0: switchPage(pageIndex),
    )
    page1Button.pack(side=tk.LEFT)
        
    page2Button = tk.Button( #Button to go to page 2
        buttonControlsFrame,
        text="Page 2",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=1: switchPage(pageIndex),
    )
    page2Button.pack(side=tk.RIGHT)
        
    pageButtons = [page1Button, page2Button]
       
    currentPage = tk.IntVar(window, 0)

    seedLabel = tk.Label(persistentFrameRight, text="Please input your desired seed value below (blank for random seed)")
    seedLabel.pack()

    seedEntry = tk.Entry(persistentFrameRight, fg="black", bg=NAHOBINO_BLUE, width=50)
    seedEntry.pack()

    demonLabel = tk.Label(page1FrameTop, text="Demon Randomizer")
    demonLabel.pack()

    listDemon = tk.Listbox(page1FrameTop, selectmode = "multiple", width=75, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listDemon.insert(0, "Randomize Levels")
    listDemon.insert(1, "Randomize Skills")
    listDemon.insert(2, "Scale Skills to Level")
    listDemon.insert(3, "Randomize Innate Skills")
    listDemon.insert(4, "Weight Skills by Potentials")
    listDemon.insert(5, "Randomize Potentials")
    listDemon.insert(6, "Scale Potentials to Level")
    listDemon.insert(7, "Unique Skills can show up more than once")
    listDemon.pack()

    inheritanceLabel = tk.Label(page1FrameTopLeft, text="Unique Skill Inheritance")
    inheritanceLabel.pack()

    listInheritance = tk.Listbox(page1FrameTopLeft,selectmode= "single",exportselection=False, selectbackground = NAHOBINO_BLUE)
    listInheritance.insert(0, "Vanilla")
    listInheritance.insert(1, "Random")
    listInheritance.insert(2, "Free")
    listInheritance.selection_set(0)
    listInheritance.pack()

    musicLabel = tk.Label(page1FrameLeft, text="Boss Music Setting")
    musicLabel.pack()

    listMusic = tk.Listbox(page1FrameLeft, selectmode = "single", exportselection=False, selectbackground = NAHOBINO_BLUE)
    listMusic.insert(0, "Boss-based")
    listMusic.insert(1, "Check-based")
    listMusic.insert(2, "Random")
    listMusic.selection_set(0)
    listMusic.pack()
        
    itemLabel = tk.Label(page1FrameRight, text="Item Randomizer")
    itemLabel.pack()

    listItem = tk.Listbox(page1FrameRight, selectmode = "multiple", width = 75, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listItem.insert(0, "Randomize Shop Items")
    listItem.insert(1, "Randomize Shop Essences")
    listItem.insert(2, "Randomize Enemy Drops")
    listItem.pack()
        
    bossLabel = tk.Label(page2FrameLeft, text="Boss Randomizer")
    bossLabel.pack()

    listBoss = tk.Listbox(page2FrameLeft, selectmode = "multiple", width=50, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listBoss.insert(0, "Randomize normal bosses with each other only")
    listBoss.insert(1, "Randomize normal bosses with all bosses")
    listBoss.insert(2, "Randomize Lucifer")
    listBoss.pack()
    
    abscessLabel = tk.Label(page2FrameLeft, text="Abscess Bosses (N)")
    abscessLabel.pack()

    listAbscess = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listAbscess.insert(0, "Vanilla abscess bosses")
    listAbscess.insert(1, "Randomize abscess bosses with each other")
    listAbscess.insert(2, "Randomize abscess bosses with all bosses")
    listAbscess.selection_set(0)
    listAbscess.pack()
    
    punishingLabel = tk.Label(page2FrameRight, text="Punishing Foes (Overworld Bosses) (N)")
    punishingLabel.pack()

    listPunishing = tk.Listbox(page2FrameRight, selectmode = "single", width=50, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listPunishing.insert(0, "Vanilla punishing foes")
    listPunishing.insert(1, "Randomize punishing foes with each other")
    listPunishing.insert(2, "Randomize punishing foes with all bosses")
    listPunishing.selection_set(0)
    listPunishing.pack()
    
    superbossLabel = tk.Label(page2FrameRight, text="Superbosses")
    superbossLabel.pack()

    listSuperboss = tk.Listbox(page2FrameRight, selectmode = "single", width=50, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listSuperboss.insert(0, "Vanilla superbosses")
    listSuperboss.insert(1, "Randomize superbosses with each other")
    listSuperboss.insert(2, "Randomize superbosses with all bosses")
    listSuperboss.selection_set(0)
    listSuperboss.pack()
        
    page1Frame.tkraise()

    #Set starting GUI values based on saved user settings
    configur = ConfigParser()
    if os.path.exists('config.ini'):
        configur.read('config.ini')

        try:
            if configur.get('Demon', 'RandomLevels') == 'true':
                listDemon.selection_set(0)
            if configur.get('Demon', 'RandomSkills') == 'true':
                listDemon.selection_set(1)
            if configur.get('Demon', 'ScaledSkills') == 'true':
                listDemon.selection_set(2)
            if configur.get('Demon', 'RandomInnates') == 'true':
                listDemon.selection_set(3)
            if configur.get('Demon', 'WeightSkillsToPotentials') == 'true':
                listDemon.selection_set(4)
            if configur.get('Demon', 'RandomPotentials') == 'true':
                listDemon.selection_set(5)
            if configur.get('Demon', 'ScaledPotentials') == 'true':
                listDemon.selection_set(6)
            if configur.get('Demon', 'multipleUniques') == 'true':
                listDemon.selection_set(7)
            if configur.get('Inheritance', 'RandomInheritance') == 'true':
                listInheritance.selection_clear(0)
                listInheritance.selection_set(1)
            if configur.get('Inheritance', 'FreeInheritance') == 'true':
                listInheritance.selection_clear(0)
                listInheritance.selection_set(2)
            if configur.get('Music', 'RandomMusic') == 'true':
                listMusic.selection_clear(0)
                listMusic.selection_set(2)
            if configur.get('Music', 'CheckBasedMusic') == 'true':
                listMusic.selection_clear(0)
                listMusic.selection_set(1)
            if configur.get('Item', 'RandomShopItems') == 'true':
                listItem.selection_set(0)
            if configur.get('Item', 'RandomShopEssences') == 'true':
                listItem.selection_set(1)
            if configur.get('Item', 'RandomEnemyDrops') == 'true':
                listItem.selection_set(2)
            if configur.get('Boss', 'NormalBossesSelf') == 'true':
                listBoss.selection_set(0)
            if configur.get('Boss', 'NormalBossesMixed') == 'true':
                listBoss.selection_set(1)
            if configur.get('Boss', 'RandomizeLucifer') == 'true':
                listBoss.selection_set(2)
            if configur.get('Boss', 'AbscessBossesSelf') == 'true':
                listAbscess.selection_clear(0)
                listAbscess.selection_set(1)
            if configur.get('Boss', 'AbscessBossesMixed') == 'true':
                listAbscess.selection_clear(0)
                listAbscess.selection_set(2)
            if configur.get('Boss', 'OverworldBossesSelf') == 'true':
                listPunishing.selection_clear(0)
                listPunishing.selection_set(1)
            if configur.get('Boss', 'OverworldBossesMixed') == 'true':
                listPunishing.selection_clear(0)
                listPunishing.selection_set(2)
            if configur.get('Boss', 'SuperbossesSelf') == 'true':
                listSuperboss.selection_clear(0)
                listSuperboss.selection_set(1)
            if configur.get('Boss', 'SuperbossesMixed') == 'true':
                listSuperboss.selection_clear(0)
                listSuperboss.selection_set(2)
        except (NoOptionError, NoSectionError):
            createConfigFile(configur)
    else:
        createConfigFile(configur)
        
    window.mainloop()
    
    try:
        #Store all GUI selections into variables before closing the GUI
        textSeed = seedEntry.get()
        demonFlags = [False for i in range(listDemon.size())]
        for i in listDemon.curselection():
            demonFlags[i] = True
        inheritanceChoice = listInheritance.curselection()
        musicChoice = listMusic.curselection()
        itemFlags = [False for i in range(listItem.size())]
        for i in listItem.curselection():
            itemFlags[i] = True
        bossFlags = [False for i in range(listBoss.size())]
        for i in listBoss.curselection():
            bossFlags[i] = True
        abscessChoice = listAbscess.curselection()
        punishingChoice = listPunishing.curselection()
        superbossChoice = listSuperboss.curselection()
        
        window.destroy()
    except tk.TclError:
        raise(RuntimeError)        

    #Set the config settings
    if demonFlags[0]:
        configSettings.randomDemonLevels = True
        configur.set('Demon', 'RandomLevels', 'true')
    else:
        configur.set('Demon', 'RandomLevels', 'false')

    if demonFlags[1]:
        configSettings.randomSkills = True
        configur.set('Demon', 'RandomSkills', 'true')
    else:
        configur.set('Demon', 'RandomSkills', 'false')

    if demonFlags[2]:
        configSettings.scaledSkills = True
        configur.set('Demon', 'ScaledSkills', 'true')
    else:
        configur.set('Demon', 'ScaledSkills', 'false')

    if demonFlags[3]:
        configSettings.randomInnates = True
        configur.set('Demon', 'RandomInnates', 'true')
    else:
        configur.set('Demon', 'RandomInnates', 'false')

    if demonFlags[4]:
        configSettings.potentialWeightedSkills = True
        configur.set('Demon', 'WeightSkillsToPotentials', 'true')
    else:
        configur.set('Demon', 'WeightSkillsToPotentials', 'false')

    if demonFlags[5]:
        configSettings.randomPotentials = True
        configur.set('Demon', 'RandomPotentials', 'true')
    else:
        configur.set('Demon', 'RandomPotentials', 'false')

    if demonFlags[6]:
        configSettings.scaledPotentials = True
        configur.set('Demon', 'ScaledPotentials', 'true')
    else:
        configur.set('Demon', 'ScaledPotentials', 'false')

    if demonFlags[7]:
        configSettings.multipleUniques = True
        configur.set('Demon', 'multipleUniques', 'true')
    else:
        configur.set('Demon', 'multipleUniques', 'false')

    if len(inheritanceChoice) > 0 and inheritanceChoice[0] == 1:
        configSettings.randomInheritance = True
        configur.set('Inheritance', 'RandomInheritance', 'true')
    else:
        configur.set('Inheritance', 'RandomInheritance', 'false')
    
    if len(inheritanceChoice) > 0 and inheritanceChoice[0] == 2:
        configSettings.freeInheritance = True
        configur.set('Inheritance', 'FreeInheritance', 'true')
    else:
        configur.set('Inheritance', 'FreeInheritance', 'false')
            
    if len(musicChoice) > 0 and musicChoice[0] == 2:
        configSettings.randomMusic = True
        configur.set('Music', 'RandomMusic', 'true')
    else:
        configur.set('Music', 'RandomMusic', 'false')

    if len(musicChoice) > 0 and musicChoice[0] == 1:
        configSettings.checkBasedMusic = True
        configur.set('Music', 'CheckBasedMusic', 'true')
    else:
        configur.set('Music', 'CheckBasedMusic', 'false')
        
    if itemFlags[0]:
        configSettings.randomShopItems = True
        configur.set('Item', 'RandomShopItems', 'true')
    else:
        configur.set('Item', 'RandomShopItems', 'false')
        
    if itemFlags[1]:
        configSettings.randomShopEssences = True
        configur.set('Item', 'RandomShopEssences', 'true')
    else:
        configur.set('Item', 'RandomShopEssences', 'false')
        
    if itemFlags[2]:
        configSettings.randomEnemyDrops = True
        configur.set('Item', 'RandomEnemyDrops', 'true')
    else:
        configur.set('Item', 'RandomEnemyDrops', 'false')
            
    if bossFlags[0]:
        configSettings.selfRandomizeNormalBosses = True
        configur.set('Boss', 'NormalBossesSelf', 'true')
    else:
        configur.set('Boss', 'NormalBossesSelf', 'false')

    if bossFlags[1]:
        configSettings.mixedRandomizeNormalBosses = True
        configur.set('Boss', 'NormalBossesMixed', 'true')
    else:
        configur.set('Boss', 'NormalBossesMixed', 'false')
        
    if bossFlags[2]:
        configSettings.randomizeLucifer = True
        configur.set('Boss', 'RandomizeLucifer', 'true')
    else:
        configur.set('Boss', 'RandomizeLucifer', 'false')
            
    if len(abscessChoice) > 0 and abscessChoice[0] == 1:
        configSettings.selfRandomizeAbscessBosses = True
        configur.set('Boss', 'AbscessBossesSelf', 'true')
    else:
        configur.set('Boss', 'AbscessBossesSelf', 'false')

    if len(abscessChoice) > 0 and abscessChoice[0] == 2:
        configSettings.mixedRandomizeAbscessBosses = True
        configur.set('Boss', 'AbscessBossesMixed', 'true')
    else:
        configur.set('Boss', 'AbscessBossesMixed', 'false')
            
    if len(punishingChoice) > 0 and punishingChoice[0] == 1:
        configSettings.selfRandomizeOverworldBosses = True
        configur.set('Boss', 'OverworldBossesSelf', 'true')
    else:
        configur.set('Boss', 'OverworldBossesSelf', 'false')

    if len(punishingChoice) > 0 and punishingChoice[0] == 2:
        configSettings.mixedRandomizeOverworldBosses = True
        configur.set('Boss', 'OverworldBossesMixed', 'true')
    else:
        configur.set('Boss', 'OverworldBossesMixed', 'false')
        
    if len(superbossChoice) > 0 and superbossChoice[0] == 1:
        configSettings.selfRandomizeSuperbosses = True
        configur.set('Boss', 'SuperbossesSelf', 'true')
    else:
        configur.set('Boss', 'SuperbossesSelf', 'false')

    if len(superbossChoice) > 0 and superbossChoice[0] == 2:
        configSettings.mixedRandomizeSuperbosses = True
        configur.set('Boss', 'SuperbossesMixed', 'true')
    else:
        configur.set('Boss', 'SuperbossesMixed', 'false')

    with open('config.ini', 'w') as configfile:
        configur.write(configfile)

    return (configSettings, textSeed)

#Initializes the config.ini file with default values if it is missing or there's a version difference
def createConfigFile(configur):
    configur.read('config.ini')
    configur['Demon'] = {'RandomLevels': False, 'RandomSkills': False, 'ScaledSkills': False, 'RandomInnates': False, 'WeightSkillsToPotentials': False,
                                 'RandomPotentials': False, 'ScaledPotentials': False, 'multipleUniques': False}
    configur['Item'] = {'RandomShopItems': False, 'RandomShopEssences': False, 'RandomEnemyDrops': False}
    configur['Inheritance'] = {'RandomInheritance': False, 'FreeInheritance': False}
    configur['Music'] = {'CheckBasedMusic': False, 'RandomMusic': False}
    configur['Boss'] = {'NormalBossesSelf': False, 'NormalBossesMixed': False, 'RandomizeLucifer': False, 'AbscessBossesSelf': False, 'AbscessBossesMixed': False,
                                 'OverworldBossesSelf': False, 'OverworldBossesMixed': False, 'SuperbossesSelf': False, 'SuperbossesMixed': False}
   