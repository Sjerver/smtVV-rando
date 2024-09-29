import tkinter as tk
import tkinter.messagebox
from configparser import ConfigParser, NoOptionError, NoSectionError
import os
import util.paths as paths

NAHOBINO_BLUE = "#5b87d5"
NAHOBINO_BRIGHT_BLUE = "#6b97f5"
VENGEANCE_PURPLE = "#a698dd"
PRESS_TURN_RED = "#831530"
PRESS_TURN_BRIGHT_RED = "#ab1d33"
DISABLED_GRAY = "#333333"

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
    page3Frame = tk.Frame(window, width=1000, height=500, background="#cccccc")
    page3Frame.grid(row=1, column=0)
    page3Frame.pack_propagate(False)
    pages = [page1Frame, page2Frame, page3Frame]
    buttonControlsFrame = tk.Frame(window, width=400, height=30)
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
    page1FrameTopRight = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameTopRight.grid(row=0, column=1, columnspan = 1, sticky = tk.W+tk.E)
    page1FrameTopRight.pack_propagate(False)
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
    page3FrameTopLeft = tk.Frame(page3Frame, width=500, height=250, background="#cccccc")
    page3FrameTopLeft.grid(row=0, column=0)
    page3FrameTopLeft.pack_propagate(False)
    page3FrameTopRight = tk.Frame(page3Frame, width=500, height=250, background="#cccccc")
    page3FrameTopRight.grid(row=0, column=1)
    page3FrameTopRight.pack_propagate(False)
    page3FrameBottom = tk.Frame(page3Frame, width=1000, height=250, background="#cccccc")
    page3FrameBottom.grid(row=1, column=0, columnspan = 2, sticky = tk.W+tk.E)
    page3FrameBottom.pack_propagate(False)
        
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
        
    def apply_preset_settings():
        confirmation = tk.messagebox.askyesno(title="confirmation", message="Confirm overwriting settings?")
        if not confirmation:
            return
        presetConfigur = ConfigParser()
        presetConfigur.read(paths.PRESET_SETTINGS_FOLDER + "/" + dropdownPresetText.get() + ".ini")
        ApplySettings(presetConfigur)

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
    
    page3Button = tk.Button( #Button to go to page 2
        buttonControlsFrame,
        text="Page 3",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=2: switchPage(pageIndex),
    )
    page3Button.pack(side=tk.RIGHT)
    
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
        
    pageButtons = [page1Button, page2Button, page3Button]
       
    currentPage = tk.IntVar(window, 0)

    seedLabel = tk.Label(persistentFrameRight, text="Please input your desired seed value below (blank for random seed)")
    seedLabel.pack()

    seedEntry = tk.Entry(persistentFrameRight, fg="black", bg=NAHOBINO_BLUE, width=50)
    seedEntry.pack()
    
    apply_preset_button = tk.Button(
        persistentFrameRight,
        text="Use Preset",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        state=tk.DISABLED,
        command=apply_preset_settings
    )
    
    def EnableApplySettingsButton(event):
        apply_preset_button.config(state=tk.NORMAL)
        
    dropdownPresetText = tk.StringVar()
    dropdownPresetText.set("Recommended Settings Presets")
    dropdownPresets = tk.OptionMenu(persistentFrameRight, dropdownPresetText,"Balanced", "Casual", "Challenge", "Speedrun", "Masochist", "MAX CHAOS", command=EnableApplySettingsButton)
    dropdownPresets.config(fg="black",bg=NAHOBINO_BLUE,activebackground=NAHOBINO_BRIGHT_BLUE)
    dropdownPresets.pack()
    apply_preset_button.pack()

    demonLabel = tk.Label(page1FrameTop, text="Demon Randomizer")
    demonLabel.grid(row=0, column=0, sticky='nsew', columnspan= 2, padx = [10,0])

    listDemon = tk.Listbox(page1FrameTop, selectmode = "multiple", width=75, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listDemon.insert(0, "Randomize Levels")
    listDemon.insert(1, "Randomize Skills")
    listDemon.insert(2, "Scale Skills to Level")
    listDemon.insert(3, "Randomize Innate Skills")
    listDemon.insert(4, "Weight Skills by Potentials")
    listDemon.insert(5, "Randomize Potentials")
    listDemon.insert(6, "Scale Potentials to Level")
    listDemon.insert(7, "Unique Skills can show up more than once")
    listDemon.insert(8, "Randomize Races")
    listDemon.insert(9, "Randomize Alignment")
    listDemon.insert(10, "Same Level for Quest Join Demons")
    listDemon.insert(11, "Randomize Stat Modifiers")
    listDemon.insert(12, "Reduce Compendium Cost Drastically")
    listDemon.insert(13, "Restrict Lunation Flux to one demon")
    listDemon.insert(14, "Include Enemy Only Skills in Skill Pool")

    demonScrollbar = tk.Scrollbar(page1FrameTop, orient='vertical')
    demonScrollbar.config(command=listDemon.yview)
    listDemon.config(yscrollcommand=demonScrollbar.set)
    listDemon.grid(row=1, column=0, sticky="nsew", padx = [10,0])
    demonScrollbar.grid(row=1, column=1, sticky="ns")
    page1FrameTop.grid_rowconfigure(0, weight=1)
    page1FrameTop.grid_columnconfigure(0, weight=1)

    inheritanceLabel = tk.Label(page1FrameTopRight, text="Unique Skill Inheritance")
    inheritanceLabel.pack()

    listInheritance = tk.Listbox(page1FrameTopRight,selectmode= "single",exportselection=False, selectbackground = NAHOBINO_BLUE)
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
    listItem.insert(3, "Randomize Chests")
    listItem.insert(4, "Scale Items To Area")
    listItem.insert(5, "Randomize Miman Rewards ")
    listItem.insert(6, "Randomize Mission Rewards ")
    listItem.insert(7, "Randomize NPC/Story Item Gifts")
    listItem.insert(8, "Combine Unique Item Pools")
    listItem.insert(9, "Include Tsukuyomi Talisman as Item Gift")
    listItem.pack()
        
    bossLabel = tk.Label(page2FrameLeft, text="Boss Randomizer")
    bossLabel.pack()

    listBoss = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listBoss.insert(0, "Vanilla normal bosses")
    listBoss.insert(1, "Randomize normal bosses with each other")
    listBoss.insert(2, "Randomize normal bosses with all bosses")
    listBoss.selection_set(0)
    listBoss.pack()
    
    abscessLabel = tk.Label(page2FrameLeft, text="Abscess Bosses")
    abscessLabel.pack()

    listAbscess = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listAbscess.insert(0, "Vanilla abscess bosses")
    listAbscess.insert(1, "Randomize abscess bosses with each other")
    listAbscess.insert(2, "Randomize abscess bosses with all bosses")
    listAbscess.selection_set(0)
    listAbscess.pack()
    
    punishingLabel = tk.Label(page2FrameLeft, text="Punishing Foes (Overworld Bosses)")
    punishingLabel.pack()

    listPunishing = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listPunishing.insert(0, "Vanilla punishing foes")
    listPunishing.insert(1, "Randomize punishing foes with each other")
    listPunishing.insert(2, "Randomize punishing foes with all bosses")
    listPunishing.selection_set(0)
    listPunishing.pack()
    
    superbossLabel = tk.Label(page2FrameLeft, text="Superbosses")
    superbossLabel.pack()

    listSuperboss = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listSuperboss.insert(0, "Vanilla superbosses")
    listSuperboss.insert(1, "Randomize superbosses with each other")
    listSuperboss.insert(2, "Randomize superbosses with all bosses")
    listSuperboss.selection_set(0)
    listSuperboss.pack()
    
    minibossLabel = tk.Label(page2FrameLeft, text="Minibosses")
    minibossLabel.pack()

    listMiniboss = tk.Listbox(page2FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listMiniboss.insert(0, "Vanilla minibosses")
    listMiniboss.insert(1, "Randomize minibosses with each other")
    listMiniboss.insert(2, "Randomize minibosses with all bosses")
    listMiniboss.selection_set(0)
    listMiniboss.pack()
    
    bossSettingsLabel = tk.Label(page2FrameRight, text="Boss Settings")
    bossSettingsLabel.pack()

    listBossSettings = tk.Listbox(page2FrameRight, selectmode = "multiple", width=50, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listBossSettings.insert(0, "Scale boss damage to check (Recommended)")
    listBossSettings.insert(1, "Boss press turns match check")
    listBossSettings.insert(2, "Randomize Lucifer")
    listBossSettings.insert(3, "No story boss ambush until after Hydra check")
    listBossSettings.insert(4, "Ambushes are dependent on boss where possible")
    listBossSettings.insert(5, "Nerf bosses' healing skills")
    listBossSettings.insert(6, "Bosses' instakill susceptibility matches check")
    listBossSettings.pack()

    ishtarLabel = tk.Label(page2FrameRight, text="Ishtar's press turns")
    ishtarLabel.pack()
    
    ishtarScale = tk.Scale(page2FrameRight, from_=1, to=8, orient=tk.HORIZONTAL, bg=PRESS_TURN_RED, troughcolor="Black", activebackground=PRESS_TURN_BRIGHT_RED)
    ishtarScale.set(3)
    
    randomIshtarPressTurnsVar = tk.IntVar()
    
    def toggleIshtarCheckbox():
        if randomIshtarPressTurnsVar.get() == 0:
            ishtarScale.config(state=tk.NORMAL, bg=PRESS_TURN_RED)
        else:
            ishtarScale.config(state=tk.DISABLED, bg=DISABLED_GRAY)
    
    ishtarRandomizeCheckbox = tk.Checkbutton(page2FrameRight, text="Random", variable=randomIshtarPressTurnsVar, onvalue=1, offvalue=0, command=toggleIshtarCheckbox)
    ishtarRandomizeCheckbox.pack()
    ishtarScale.pack()
    
    miracleLabel = tk.Label(page3FrameTopLeft, text="Miracle Randomizer")
    miracleLabel.pack()

    listMiracle = tk.Listbox(page3FrameTopLeft, selectmode = "multiple", width = 75, height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listMiracle.insert(0, "Randomize Miracle unlocks")
    listMiracle.insert(1, "Randomize Miracle prices")
    listMiracle.insert(2, "Learn +3 stock Divine Garrisons first")            
    listMiracle.pack()
    
    rankViolationLabel = tk.Label(page3FrameTopLeft, text="Rank Violation")
    rankViolationLabel.pack()

    listRankViolation = tk.Listbox(page3FrameTopLeft, selectmode = "single", width = 50, height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listRankViolation.insert(0, "Randomize Rank Violation")
    listRankViolation.insert(1, "Vanilla Rank Violation")
    listRankViolation.insert(2, "Guarantee Rank Violation early")
    listRankViolation.selection_set(0)
    listRankViolation.pack()
    
    earlyMiracleLabel = tk.Label(page3FrameTopRight, text="Miracles to guarantee early")
    earlyMiracleLabel.pack()

    listEarlyMiracle = tk.Listbox(page3FrameTopRight, selectmode = "multiple", width = 50, height=8, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listEarlyMiracle.insert(0, "First Divine Garrison")
    listEarlyMiracle.insert(1, "Forestall")
    listEarlyMiracle.insert(2, "Empowering Cheer 1")
    listEarlyMiracle.insert(3, "Art of Essences 1")
    listEarlyMiracle.insert(4, "Demon Proficiency 1")
    listEarlyMiracle.insert(5, "Divine Proficiency 1")
    listEarlyMiracle.insert(6, "Divine Amalgamation")
    listEarlyMiracle.insert(7, "Inheritence Violation")
    listEarlyMiracle.pack()
    
    def toggleMiracleListboxes(event):
        if 0 in listMiracle.curselection():
            listRankViolation.config(state=tk.NORMAL, bg="White")
            listEarlyMiracle.config(state=tk.NORMAL, bg="White")
        else:
            listRankViolation.config(state=tk.DISABLED, bg=DISABLED_GRAY)
            listEarlyMiracle.config(state=tk.DISABLED, bg=DISABLED_GRAY)
            
    listMiracle.bind("<<ListboxSelect>>", toggleMiracleListboxes)
    
    uniqueSkillAnimationsNote = tk.Label(page3FrameBottom, text="If the wrong demon uses a unique skill, the game will hang until the skip animations button is pressed.\n"
                                         + "The 'Fix unique skill animations' patch replaces unique skill anims with normal skill anims to get around this.")
    uniqueSkillAnimationsNote.pack()

    patchesLabel = tk.Label(page3FrameBottom, text="Patches")
    patchesLabel.pack()

    listPatches = tk.Listbox(page3FrameBottom, selectmode = "multiple", width=50, height=2, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listPatches.insert(0, "Fix unique skill animations")
    listPatches.insert(1, "Buff guest Yuzuru to make first Labolas check easier")
    listPatches.pack()
    
    expLabel = tk.Label(page3FrameBottom, text="EXP Multiplier")
    expLabel.pack()
    
    expScale = tk.Scale(page3FrameBottom, from_=1, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg=NAHOBINO_BLUE, troughcolor="Black", activebackground=NAHOBINO_BRIGHT_BLUE)
    expScale.set(1)
    expScale.pack()

    expLabel = tk.Label(page3FrameBottom, text="Chance for basic enemies to receive additional press turns")
    expLabel.pack()

    pressTurnScale = tk.Scale(page3FrameBottom, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, bg=NAHOBINO_BLUE, troughcolor="Black", activebackground=NAHOBINO_BRIGHT_BLUE)
    pressTurnScale.set(0.1)
    pressTurnScale.pack()
        
    page1Frame.tkraise()
    
    def ApplySettings(configur):
        if configur.get('Demon', 'RandomLevels') == 'true':
            listDemon.selection_set(0)
        else:
            listDemon.selection_clear(0)
        if configur.get('Demon', 'RandomSkills') == 'true':
            listDemon.selection_set(1)
        else:
            listDemon.selection_clear(1)
        if configur.get('Demon', 'ScaledSkills') == 'true':
            listDemon.selection_set(2)
        else:
            listDemon.selection_clear(2)
        if configur.get('Demon', 'RandomInnates') == 'true':
            listDemon.selection_set(3)
        else:
            listDemon.selection_clear(3)
        if configur.get('Demon', 'WeightSkillsToPotentials') == 'true':
            listDemon.selection_set(4)
        else:
            listDemon.selection_clear(4)
        if configur.get('Demon', 'RandomPotentials') == 'true':
            listDemon.selection_set(5)
        else:
            listDemon.selection_clear(5)
        if configur.get('Demon', 'ScaledPotentials') == 'true':
            listDemon.selection_set(6)
        else:
            listDemon.selection_clear(6)
        if configur.get('Demon', 'multipleUniques') == 'true':
            listDemon.selection_set(7)
        else:
            listDemon.selection_clear(7)
        if configur.get('Demon', 'randomRaces') == 'true':
            listDemon.selection_set(8)
        else:
            listDemon.selection_clear(8)
        if configur.get('Demon', 'randomAlignment') == 'true':
            listDemon.selection_set(9)
        else:
            listDemon.selection_clear(9)
        if configur.get('Demon', 'ensureDemonJoinLevel') == 'true':
            listDemon.selection_set(10)
        else:
            listDemon.selection_clear(10)
        if configur.get('Demon', 'RandomDemonStats') == 'true':
            listDemon.selection_set(11)
        else:
            listDemon.selection_clear(11)
        if configur.get('Demon', 'ReduceCompendiumCost') == 'true':
            listDemon.selection_set(12)
        else:
            listDemon.selection_clear(12)
        if configur.get('Demon', 'RestrictLunationFlux') == 'true':
            listDemon.selection_set(13)
        else:
            listDemon.selection_clear(13)
        if configur.get('Demon', 'EnemyOnlySkills') == 'true':
            listDemon.selection_set(14)
        else:
            listDemon.selection_clear(14)
        listInheritance.selection_set(0)
        if configur.get('Inheritance', 'RandomInheritance') == 'true':
            listInheritance.selection_clear(0)
            listInheritance.selection_set(1)
        else:
            listInheritance.selection_clear(1)
        if configur.get('Inheritance', 'FreeInheritance') == 'true':
            listInheritance.selection_clear(0)
            listInheritance.selection_set(2)
        else:
            listInheritance.selection_clear(2)
        listMusic.selection_set(0)
        if configur.get('Music', 'RandomMusic') == 'true':
            listMusic.selection_clear(0)
            listMusic.selection_set(2)
        else:
            listMusic.selection_clear(2)
        if configur.get('Music', 'CheckBasedMusic') == 'true':
            listMusic.selection_clear(0)
            listMusic.selection_set(1)
        else:
            listMusic.selection_clear(1)
        if configur.get('Item', 'RandomShopItems') == 'true':
            listItem.selection_set(0)
        else:
            listItem.selection_clear(0)
        if configur.get('Item', 'RandomShopEssences') == 'true':
            listItem.selection_set(1)
        else:
            listItem.selection_clear(1)
        if configur.get('Item', 'RandomEnemyDrops') == 'true':
            listItem.selection_set(2)
        else:
            listItem.selection_clear(2)
        if configur.get('Item', 'RandomChests') == 'true':
            listItem.selection_set(3)
        else:
            listItem.selection_clear(3)
        if configur.get('Item', 'ScaleItemsToArea') == 'true':
            listItem.selection_set(4)
        else:
            listItem.selection_clear(4)
        if configur.get('Item', 'RandomizeMimanRewards') == 'true':
            listItem.selection_set(5)
        else:
            listItem.selection_clear(5)
        if configur.get('Item', 'RandomizeMissionRewards') == 'true':
            listItem.selection_set(6)
        else:
            listItem.selection_clear(6)

        if configur.get('Item', 'RandomizeGiftItems') == 'true':
            listItem.selection_set(7)
        else:
            listItem.selection_clear(7)

        if configur.get('Item', 'CombineKeyItemPools') == 'true':
            listItem.selection_set(8)
        else:
            listItem.selection_clear(8)
        
        if configur.get('Item', 'IncludeTsukuyomiTalisman') == 'true':
            listItem.selection_set(9)
        else:
            listItem.selection_clear(9)

        listBoss.selection_set(0)
        if configur.get('Boss', 'NormalBossesSelf') == 'true':
            listBoss.selection_clear(0)
            listBoss.selection_set(1)
        else:
            listBoss.selection_clear(1)
        if configur.get('Boss', 'NormalBossesMixed') == 'true':
            listBoss.selection_clear(0)
            listBoss.selection_set(2)
        else:
            listBoss.selection_clear(2)
        listAbscess.selection_set(0)
        if configur.get('Boss', 'AbscessBossesSelf') == 'true':
            listAbscess.selection_clear(0)
            listAbscess.selection_set(1)
        else:
            listAbscess.selection_clear(1)
        if configur.get('Boss', 'AbscessBossesMixed') == 'true':
            listAbscess.selection_clear(0)
            listAbscess.selection_set(2)
        else:
            listAbscess.selection_clear(2)
        listPunishing.selection_set(0)
        if configur.get('Boss', 'OverworldBossesSelf') == 'true':
            listPunishing.selection_clear(0)
            listPunishing.selection_set(1)
        else:
            listPunishing.selection_clear(1)
        if configur.get('Boss', 'OverworldBossesMixed') == 'true':
            listPunishing.selection_clear(0)
            listPunishing.selection_set(2)
        else:
            listPunishing.selection_clear(2)
        listSuperboss.selection_set(0)
        if configur.get('Boss', 'SuperbossesSelf') == 'true':
            listSuperboss.selection_clear(0)
            listSuperboss.selection_set(1)
        else:
            listSuperboss.selection_clear(1)
        if configur.get('Boss', 'SuperbossesMixed') == 'true':
            listSuperboss.selection_clear(0)
            listSuperboss.selection_set(2)
        else:
            listSuperboss.selection_clear(2)
        listMiniboss.selection_set(0)
        if configur.get('Boss', 'MinibossesSelf') == 'true':
            listMiniboss.selection_clear(0)
            listMiniboss.selection_set(1)
        else:
            listMiniboss.selection_clear(1)
        if configur.get('Boss', 'MinibossesMixed') == 'true':
            listMiniboss.selection_clear(0)
            listMiniboss.selection_set(2)
        else:
            listMiniboss.selection_clear(2)
        if configur.get('Boss', 'ScaleBossDamage') == 'true':
            listBossSettings.selection_set(0)
        else:
            listBossSettings.selection_clear(0)
        if configur.get('Boss', 'ScalePressTurns') == 'true':
            listBossSettings.selection_set(1)
        else:
            listBossSettings.selection_clear(1)
        if configur.get('Boss', 'RandomizeLucifer') == 'true':
            listBossSettings.selection_set(2)
        else:
            listBossSettings.selection_clear(2)
        if configur.get('Boss', 'PreventEarlyAmbush') == 'true':
            listBossSettings.selection_set(3)
        else:
            listBossSettings.selection_clear(3)
        if configur.get('Boss', 'BossDependentAmbush') == 'true':
            listBossSettings.selection_set(4)
        else:
            listBossSettings.selection_clear(4)
        if configur.get('Boss', 'NerfBossHealing') == 'true':
            listBossSettings.selection_set(5)
        else:
            listBossSettings.selection_clear(5)
        if configur.get('Boss', 'ScaleInstakillRates') == 'true':
            listBossSettings.selection_set(6)
        else:
            listBossSettings.selection_clear(6)
        if configur.get('Boss', 'RandomizeIshtarPressTurns') == 'true':
            ishtarRandomizeCheckbox.select()
        else:
            ishtarRandomizeCheckbox.deselect()
        toggleIshtarCheckbox()
        ishtarScale.set(configur.get('Boss', 'IshtarPressTurns'))
        if configur.get('Miracle', 'RandomMiracleUnlocks') == 'true':
            listMiracle.selection_set(0)
        else:
            listMiracle.selection_clear(0)
        if configur.get('Miracle', 'RandomMiracleCosts') == 'true':
            listMiracle.selection_set(1)
        else:
            listMiracle.selection_clear(1)
        if configur.get('Miracle', 'ReverseDivineGarrisons') == 'true':
            listMiracle.selection_set(2)
        else:
            listMiracle.selection_clear(2)
        toggleMiracleListboxes(None)
        listRankViolation.selection_set(0)
        if configur.get('Miracle', 'VanillaRankViolation') == 'true':
            listRankViolation.selection_clear(0)
            listRankViolation.selection_set(1)
        else:
            listRankViolation.selection_clear(1)
        if configur.get('Miracle', 'EarlyRankViolation') == 'true':
            listRankViolation.selection_clear(0)
            listRankViolation.selection_set(2)
        else:
            listRankViolation.selection_clear(2)
        if configur.get('Miracle', 'EarlyDivineGarrison') == 'true':
            listEarlyMiracle.selection_set(0)
        else:
            listEarlyMiracle.selection_clear(0)
        if configur.get('Miracle', 'EarlyForestall') == 'true':
            listEarlyMiracle.selection_set(1)
        else:
            listEarlyMiracle.selection_clear(1)
        if configur.get('Miracle', 'EarlyEmpoweringCheer') == 'true':
            listEarlyMiracle.selection_set(2)
        else:
            listEarlyMiracle.selection_clear(2)
        if configur.get('Miracle', 'EarlyArtOfEssences') == 'true':
            listEarlyMiracle.selection_set(3)
        else:
            listEarlyMiracle.selection_clear(3)
        if configur.get('Miracle', 'EarlyDemonProficiency') == 'true':
            listEarlyMiracle.selection_set(4)
        else:
            listEarlyMiracle.selection_clear(4)
        if configur.get('Miracle', 'EarlyDivineProficiency') == 'true':
            listEarlyMiracle.selection_set(5)
        else:
            listEarlyMiracle.selection_clear(5)
        if configur.get('Miracle', 'EarlyDivineAmalgamation') == 'true':
            listEarlyMiracle.selection_set(6)
        else:
            listEarlyMiracle.selection_clear(6)
        if configur.get('Miracle', 'EarlyInheritenceViolation') == 'true':
            listEarlyMiracle.selection_set(7)
        else:
            listEarlyMiracle.selection_clear(7)
        if configur.get('Patches', 'FixUniqueSkillAnimations') == 'true':
            listPatches.selection_set(0)
        else:
            listPatches.selection_clear(0)
        if configur.get('Patches', 'BuffGuestYuzuru') == 'true':
            listPatches.selection_set(1)
        else:
            listPatches.selection_clear(1)
        expScale.set(configur.get('Patches', 'EXPMultiplier'))
        pressTurnScale.set(configur.get('Patches','PressTurnChance'))
        
    #Set starting GUI values based on saved user settings
    configur = ConfigParser()
    if os.path.exists('config.ini'):
        configur.read('config.ini')

        try:
            ApplySettings(configur)
        except (NoOptionError, NoSectionError):
            createConfigFile(configur)
            ApplySettings(configur)
    else:
        createConfigFile(configur)
        ApplySettings(configur)
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
        bossFlags = [False for i in range(listBossSettings.size())]
        for i in listBossSettings.curselection():
            bossFlags[i] = True
        normalBossChoice = listBoss.curselection()
        abscessChoice = listAbscess.curselection()
        punishingChoice = listPunishing.curselection()
        superbossChoice = listSuperboss.curselection()
        minibossChoice = listMiniboss.curselection()
        ishtarChoice = ishtarScale.get()
        ishtarRandomizeChoice = randomIshtarPressTurnsVar.get()
        miracleFlags = [False for i in range(listMiracle.size())]
        for i in listMiracle.curselection():
            miracleFlags[i] = True
        earlyMiracleFlags = [False for i in range(listEarlyMiracle.size())]
        for i in listEarlyMiracle.curselection():
            earlyMiracleFlags[i] = True
        rankViolationChoice = listRankViolation.curselection()
        patchFlags = [False for i in range(listPatches.size())]
        for i in listPatches.curselection():
            patchFlags[i] = True
        expChoice = expScale.get()
        pressTurnChoice = pressTurnScale.get()
        
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
    
    if demonFlags[8]:
        configSettings.randomRaces = True
        configur.set('Demon', 'randomRaces', 'true')
    else:
        configur.set('Demon', 'randomRaces', 'false')
    
    if demonFlags[9]:
        configSettings.randomAlignment = True
        configur.set('Demon', 'randomAlignment', 'true')
    else:
        configur.set('Demon', 'randomAlignment', 'false')
    
    if demonFlags[10]:
        configSettings.ensureDemonJoinLevel = True
        configur.set('Demon', 'ensureDemonJoinLevel', 'true')
    else:
        configur.set('Demon', 'ensureDemonJoinLevel', 'false')
    
    if demonFlags[11]:
        configSettings.randomDemonStats = True
        configur.set('Demon', 'RandomDemonStats', 'true')
    else:
        configur.set('Demon', 'RandomDemonStats', 'false')
    
    if demonFlags[12]:
        configSettings.reduceCompendiumCosts = True
        configur.set('Demon', 'ReduceCompendiumCost', 'true')
    else:
        configur.set('Demon', 'ReduceCompendiumCost', 'false')
        
    if demonFlags[13]:
        configSettings.restrictLunationFlux = True
        configur.set('Demon', 'RestrictLunationFlux', 'true')
    else:
        configur.set('Demon', 'RestrictLunationFlux', 'false')
    
    if demonFlags[14]:
        configSettings.includeEnemyOnlySkills = True
        configur.set('Demon', 'EnemyOnlySkills', 'true')
    else:
        configur.set('Demon', 'EnemyOnlySkills', 'false')

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
        
    if itemFlags[3]:
        configSettings.randomChests = True
        configur.set('Item', 'RandomChests', 'true')
    else:
        configur.set('Item', 'RandomChests', 'false')
    
    if itemFlags[4]:
        configSettings.scaleItemsToArea = True
        configur.set('Item', 'ScaleItemsToArea', ' true')
    else:
        configur.set('Item', 'ScaleItemsToArea', ' false')

    if itemFlags[5]:
        configSettings.randomizeMimanRewards = True
        configur.set('Item', 'RandomizeMimanRewards', ' true')
    else:
        configur.set('Item', 'RandomizeMimanRewards', ' false')
    
    if itemFlags[6]:
        configSettings.randomizeMissionRewards = True
        configur.set('Item', 'RandomizeMissionRewards', ' true')
    else:
        configur.set('Item', 'RandomizeMissionRewards', ' false')
    
    if itemFlags[7]:
        configSettings.randomizeGiftItems = True
        configur.set('Item', 'RandomizeGiftItems', ' true')
    else:
        configur.set('Item', 'RandomizeGiftItems', ' false')
    
    if itemFlags[8]:
        configSettings.combineKeyItemPools = True
        configur.set('Item', 'CombineKeyItemPools', ' true')
    else:
        configur.set('Item', 'CombineKeyItemPools', ' false')
    
    if itemFlags[9]:
        configSettings.includeTsukuyomiTalisman = True
        configur.set('Item', 'IncludeTsukuyomiTalisman', ' true')
    else:
        configur.set('Item', 'IncludeTsukuyomiTalisman', ' false')
            
    if bossFlags[0]:
        configSettings.scaleBossDamage = True
        configur.set('Boss', 'ScaleBossDamage', 'true')
    else:
        configur.set('Boss', 'ScaleBossDamage', 'false')

    if bossFlags[1]:
        configSettings.scaleBossPressTurnsToCheck = True
        configur.set('Boss', 'ScalePressTurns', 'true')
    else:
        configur.set('Boss', 'ScalePressTurns', 'false')
        
    if bossFlags[2]:
        configSettings.randomizeLucifer = True
        configur.set('Boss', 'RandomizeLucifer', 'true')
    else:
        configur.set('Boss', 'RandomizeLucifer', 'false')
    
    if bossFlags[3]:
        configSettings.preventEarlyAmbush = True
        configur.set('Boss', 'PreventEarlyAmbush', 'true')
    else:
        configur.set('Boss', 'PreventEarlyAmbush', 'false')
    
    if bossFlags[4]:
        configSettings.bossDependentAmbush = True
        configur.set('Boss', 'BossDependentAmbush', 'true')
    else:
        configur.set('Boss', 'BossDependentAmbush', 'false')
        
    if bossFlags[5]:
        configSettings.nerfBossHealing = True
        configur.set('Boss', 'NerfBossHealing', 'true')
    else:
        configur.set('Boss', 'NerfBossHealing', 'false')
        
    if bossFlags[6]:
        configSettings.scaleBossInstakillRates = True
        configur.set('Boss', 'ScaleInstakillRates', 'true')
    else:
        configur.set('Boss', 'ScaleInstakillRates', 'false')
        
    if len(normalBossChoice) > 0 and normalBossChoice[0] == 1:
        configSettings.selfRandomizeNormalBosses = True
        configur.set('Boss', 'NormalBossesSelf', 'true')
    else:
        configur.set('Boss', 'NormalBossesSelf', 'false')
        
    if len(normalBossChoice) > 0 and normalBossChoice[0] == 2:
        configSettings.mixedRandomizeNormalBosses = True
        configur.set('Boss', 'NormalBossesMixed', 'true')
    else:
        configur.set('Boss', 'NormalBossesMixed', 'false')
            
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
        
    if len(minibossChoice) > 0 and minibossChoice[0] == 1:
        configSettings.selfRandomizeMinibosses = True
        configur.set('Boss', 'MinibossesSelf', 'true')
    else:
        configur.set('Boss', 'MinibossesSelf', 'false')

    if len(minibossChoice) > 0 and minibossChoice[0] == 2:
        configSettings.mixedRandomizeMinibosses = True
        configur.set('Boss', 'MinibossesMixed', 'true')
    else:
        configur.set('Boss', 'MinibossesMixed', 'false')
        
    configSettings.ishtarPressTurns = ishtarChoice
    configur.set('Boss', 'IshtarPressTurns', str(ishtarChoice))
    configSettings.randomizeIshtarPressTurns = ishtarRandomizeChoice
    if ishtarRandomizeChoice:
        configur.set('Boss', 'RandomizeIshtarPressTurns', 'true')
    else:
        configur.set('Boss', 'RandomizeIshtarPressTurns', 'false')
        
    if miracleFlags[0]:
        configSettings.randomMiracleUnlocks = True
        configur.set('Miracle', 'RandomMiracleUnlocks', 'true')
    else:
        configur.set('Miracle', 'RandomMiracleUnlocks', 'false')
        
    if miracleFlags[1]:
        configSettings.randomMiracleCosts = True
        configur.set('Miracle', 'RandomMiracleCosts', 'true')
    else:
        configur.set('Miracle', 'RandomMiracleCosts', 'false')
        
    if miracleFlags[2]:
        configSettings.reverseDivineGarrisons = True
        configur.set('Miracle', 'ReverseDivineGarrisons', 'true')
    else:
        configur.set('Miracle', 'ReverseDivineGarrisons', 'false')
        
    if len(rankViolationChoice) > 0 and rankViolationChoice[0] == 1:
        configSettings.vanillaRankViolation = True
        configur.set('Miracle', 'VanillaRankViolation', 'true')
    else:
        configur.set('Miracle', 'VanillaRankViolation', 'false')
        
    if len(rankViolationChoice) > 0 and rankViolationChoice[0] == 2:
        configSettings.forcedEarlyMiracles.append(31)
        configur.set('Miracle', 'EarlyRankViolation', 'true')
    else:
        configur.set('Miracle', 'EarlyRankViolation', 'false')
        
    if earlyMiracleFlags[0]:
        configSettings.forcedEarlyMiracles.append(55)
        configur.set('Miracle', 'EarlyDivineGarrison', 'true')
    else:
        configur.set('Miracle', 'EarlyDivineGarrison', 'false')
        
    if earlyMiracleFlags[1]:
        configSettings.forcedEarlyMiracles.append(13)
        configur.set('Miracle', 'EarlyForestall', 'true')
    else:
        configur.set('Miracle', 'EarlyForestall', 'false')
        
    if earlyMiracleFlags[2]:
        configSettings.forcedEarlyMiracles.append(49)
        configur.set('Miracle', 'EarlyEmpoweringCheer', 'true')
    else:
        configur.set('Miracle', 'EarlyEmpoweringCheer', 'false')
        
    if earlyMiracleFlags[3]:
        configSettings.forcedEarlyMiracles.append(32)
        configur.set('Miracle', 'EarlyArtOfEssences', 'true')
    else:
        configur.set('Miracle', 'EarlyArtOfEssences', 'false')
        
    if earlyMiracleFlags[4]:
        configSettings.forcedEarlyMiracles.append(51)
        configur.set('Miracle', 'EarlyDemonProficiency', 'true')
    else:
        configur.set('Miracle', 'EarlyDemonProficiency', 'false')
        
    if earlyMiracleFlags[5]:
        configSettings.forcedEarlyMiracles.append(61)
        configur.set('Miracle', 'EarlyDivineProficiency', 'true')
    else:
        configur.set('Miracle', 'EarlyDivineProficiency', 'false')
        
    if earlyMiracleFlags[6]:
        configSettings.forcedEarlyMiracles.append(117)
        configur.set('Miracle', 'EarlyDivineAmalgamation', 'true')
    else:
        configur.set('Miracle', 'EarlyDivineAmalgamation', 'false')
        
    if earlyMiracleFlags[7]:
        configSettings.forcedEarlyMiracles.append(30)
        configur.set('Miracle', 'EarlyInheritenceViolation', 'true')
    else:
        configur.set('Miracle', 'EarlyInheritenceViolation', 'false')
        
    if patchFlags[0]:
        configSettings.fixUniqueSkillAnimations = True
        configur.set('Patches', 'FixUniqueSkillAnimations', 'true')
    else:
        configur.set('Patches', 'FixUniqueSkillAnimations', 'false')
        
    if patchFlags[1]:
        configSettings.buffGuestYuzuru = True
        configur.set('Patches', 'BuffGuestYuzuru', 'true')
    else:
        configur.set('Patches', 'BuffGuestYuzuru', 'false')
        
    configSettings.expMultiplier = expChoice
    configur.set('Patches', 'EXPMultiplier', str(expChoice))

    configSettings.pressTurnChance = pressTurnChoice
    configur.set('Patches', 'PressTurnChance', str(pressTurnChoice))

    with open('config.ini', 'w') as configfile:
        configur.write(configfile)

    return (configSettings, textSeed)

#Initializes the config.ini file with default values if it is missing or there's a version difference
def createConfigFile(configur):
    configur.read('config.ini')
    configur['Demon'] = {'RandomLevels': False, 'RandomSkills': False, 'ScaledSkills': False, 'RandomInnates': False, 'WeightSkillsToPotentials': False,
                                 'RandomPotentials': False, 'ScaledPotentials': False, 'multipleUniques': False, 'randomRaces': False, 'randomAlignment': False,
                                'ensureDemonJoinLevel':False, 'RandomDemonStats': False, 'ReduceCompendiumCost': False, 'RestrictLunationFlux': False, 'EnemyOnlySkills':False}
    configur['Item'] = {'RandomShopItems': False, 'RandomShopEssences': False, 'RandomEnemyDrops': False,
                        'RandomChests': False, 'ScaleItemsToArea': False, 'RandomizeMimanRewards': False, 'RandomizeMissionRewards': False,
                        'RandomizeGiftItems': False, 'CombineKeyItemPools': False, 'IncludeTsukuyomiTalisman': False
                        }
    configur['Inheritance'] = {'RandomInheritance': False, 'FreeInheritance': False}
    configur['Music'] = {'CheckBasedMusic': False, 'RandomMusic': False}
    configur['Boss'] = {'NormalBossesSelf': False, 'NormalBossesMixed': False, 'RandomizeLucifer': False, 'AbscessBossesSelf': False, 'AbscessBossesMixed': False,
                                 'OverworldBossesSelf': False, 'OverworldBossesMixed': False, 'SuperbossesSelf': False, 'SuperbossesMixed': False,
                                 'MinibossesSelf': False, 'MinibossesMixed': False, 'ScaleBossDamage': False, 'ScalePressTurns': False, 'IshtarPressTurns': 3,
                                 'RandomizeIshtarPressTurns': False, 'PreventEarlyAmbush': False, 'BossDependentAmbush': False, 'NerfBossHealing': False,
                                 'ScaleInstakillRates': False}
    configur['Patches'] = {'FixUniqueSkillAnimations': False, 'BuffGuestYuzuru': False, 'EXPMultiplier': 1, 'PressTurnChance': 0.1}
    configur['Miracle'] = {'RandomMiracleUnlocks': False, 'RandomMiracleCosts': False, 'ReverseDivineGarrisons': False, 'VanillaRankViolation': False, 'EarlyForestall': False,
                        'EarlyEmpoweringCheer': False, 'EarlyDivineAmalgamation': False, 'EarlyDivineGarrison': False, 'EarlyDemonProficiency': False,
                        'EarlyDivineProficiency': False, 'EarlyArtOfEssences': False, 'EarlyRankViolation': False, 'EarlyInheritenceViolation': False}
   