import tkinter as tk
import tkinter.messagebox
import webbrowser
from configparser import ConfigParser, NoOptionError, NoSectionError
import os
import util.paths as paths
from base_classes.settings import Settings

NAHOBINO_BLUE = "#5b87d5"
NAHOBINO_BRIGHT_BLUE = "#6b97f5"
VENGEANCE_PURPLE = "#a698dd"
PRESS_TURN_RED = "#831530"
PRESS_TURN_BRIGHT_RED = "#ab1d33"
DISABLED_GRAY = "#333333"

VANILLA_LIST_ITEMS_ORDER = ["Treasures","Miman Rewards","Mission Rewards","NPC/Story Gifts","Vending Machines","Basic Enemy Drops","Boss Drops"]

#Creates page system with important information like randomize button always visible
def createGUI(configSettings: Settings):
    oldSeed = ""
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
    page4Frame = tk.Frame(window, width=1000, height=500, background="#cccccc")
    page4Frame.grid(row=1, column=0)
    page4Frame.pack_propagate(False)
    page5Frame = tk.Frame(window, width=1000, height=500, background="#cccccc")
    page5Frame.grid(row=1, column=0)
    page5Frame.pack_propagate(False)
    pages = [page1Frame, page2Frame,page3Frame, page4Frame,page5Frame]
    buttonControlsFrame = tk.Frame(window, width=560, height=30)
    buttonControlsFrame.grid(row=2, column=0)
    buttonControlsFrame.pack_propagate(False)
    persistentFrameLeft = tk.Frame(persistentFrame, width=500, height=170)
    persistentFrameLeft.grid(row=1, column=0)
    persistentFrameLeft.pack_propagate(False)
    persistentFrameRight = tk.Frame(persistentFrame, width=500, height=170)
    persistentFrameRight.grid(row=1, column=1)
    persistentFrameRight.pack_propagate(False)
    page1FrameTopLeft = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameTopLeft.grid(row=0, column=0)#, rowspan = 2, columnspan = 1, sticky = tk.W+tk.E)
    page1FrameTopLeft.pack_propagate(False)
    page1FrameTopRight = tk.Frame(page1Frame, width=500, height=250, background="#cccccc")
    page1FrameTopRight.grid(row=0, column=1)
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

    page3FrameLeft = tk.Frame(page3Frame, width=500, height=500, background="#cccccc")
    page3FrameLeft.grid(row=0, column=0)
    page3FrameLeft.pack_propagate(False)
    page3FrameRight = tk.Frame(page3Frame, width=500, height=500, background="#cccccc")
    page3FrameRight.grid(row=0, column=1)
    page3FrameRight.pack_propagate(False)

    page4FrameTopLeft = tk.Frame(page4Frame, width=500, height=200, background="#cccccc")
    page4FrameTopLeft.grid(row=0, column=0)
    page4FrameTopLeft.pack_propagate(False)
    page4FrameTopRight = tk.Frame(page4Frame, width=500, height=200, background="#cccccc")
    page4FrameTopRight.grid(row=0, column=1)
    page4FrameTopRight.pack_propagate(False)
    page4FrameBottomLeft = tk.Frame(page4Frame, width=500, height=300, background="#cccccc")
    page4FrameBottomLeft.grid(row=1, column=0)
    page4FrameBottomLeft.pack_propagate(False)
    page4FrameBottomRight = tk.Frame(page4Frame, width=500, height=300, background="#cccccc")
    page4FrameBottomRight.grid(row=1, column=1)
    page4FrameBottomRight.pack_propagate(False)

    page5FrameTop = tk.Frame(page5Frame, width=1000, height=250, background="#cccccc")
    page5FrameTop.grid(row=0, column=0)
    page5FrameTop.pack_propagate(False)
    page5FrameBottom= tk.Frame(page5Frame, width=1000, height=250, background="#cccccc")
    page5FrameBottom.grid(row=1, column=0)
    page5FrameBottom.pack_propagate(False)
        
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
        ApplySettings(presetConfigur,preset = True)

    def reuseLastSeed():
        seedEntry.delete(0,len(seedEntry.get()))
        seedEntry.insert(0,oldSeed)

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

    swapCutsceneModels= tk.BooleanVar()
    swapCutsceneModelCheckbox = tk.Checkbutton(persistentFrameLeft, text="(Experimental) Swap Cutscene Models", variable=swapCutsceneModels, onvalue=True, offvalue=False)
    swapCutsceneModelCheckbox.pack()

    def wikiCallback(url):
        webbrowser.open_new(url)
    
    wikiLabel = tk.Label(persistentFrameLeft, text="For more information on what settings do, please refer to the wiki!",font='TkDefaultFont 12 bold',fg=NAHOBINO_BLUE, cursor="hand2")
    wikiLabel.pack()
    wikiLabel.bind("<Button-1>", lambda e: wikiCallback("https://github.com/Sjerver/smtVV-rando/wiki"))
        
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
        text="Demons",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        state=tk.DISABLED,
        command=lambda pageIndex=0: switchPage(pageIndex),
    )
    page1Button.pack(side=tk.LEFT)
    
    page4Button = tk.Button( #Button to go to page 4
        buttonControlsFrame,
        text="Other",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=3: switchPage(pageIndex),
    )
    page4Button.pack(side=tk.RIGHT)

    page5Button = tk.Button( #Button to go to page 3
        buttonControlsFrame,
        text="Items",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=4: switchPage(pageIndex),
    )
    page5Button.pack(side=tk.RIGHT)
    
    page3Button = tk.Button( #Button to go to page 3
        buttonControlsFrame,
        text="Bosses II",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=2: switchPage(pageIndex),
    )
    page3Button.pack(side=tk.RIGHT)

    page2Button = tk.Button( #Button to go to page 2
        buttonControlsFrame,
        text="Bosses",
        width=10,
        height=3,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=lambda pageIndex=1: switchPage(pageIndex),
    )
    page2Button.pack(side=tk.RIGHT)
    
    pageButtons = [page1Button, page2Button,page3Button, page4Button,page5Button]
       
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

    reuseLastSeedButton = tk.Button( persistentFrameRight,
        text="Last Seed",
        width=10,
        height=1,
        bg=NAHOBINO_BLUE,
        fg="black",
        command=reuseLastSeed
    )
    
    def EnableApplySettingsButton(event):
        apply_preset_button.config(state=tk.NORMAL)
        
    dropdownPresetText = tk.StringVar()
    dropdownPresetText.set("Recommended Settings Presets")
    dropdownPresets = tk.OptionMenu(persistentFrameRight, dropdownPresetText,"Balanced", "Casual", "Challenge", "Speedrun", "Masochist", "MAX CHAOS", command=EnableApplySettingsButton)
    dropdownPresets.config(fg="black",bg=NAHOBINO_BLUE,activebackground=NAHOBINO_BRIGHT_BLUE)
    dropdownPresets.pack()
    apply_preset_button.pack()
    reuseLastSeedButton.pack()

    demonLabel = tk.Label(page1FrameTopLeft, text="Demon Randomizer")
    demonLabel.pack()
    #demonLabel.grid(row=0, column=0, sticky='nsew', columnspan= 2, padx = [10,0])

    listDemon = tk.Listbox(page1FrameTopLeft, selectmode = "multiple", width=75, height = 11, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listDemon.insert(0, "Randomize Levels & Encounters")
    listDemon.insert(1, "Randomize Potentials")
    listDemon.insert(2, "Scale Potentials to Level")
    listDemon.insert(3, "Randomize Races")
    listDemon.insert(4, "Randomize Alignment")
    listDemon.insert(5, "Randomize Quest Demon Joins")
    listDemon.insert(6, "Randomize Stat Modifiers")
    listDemon.insert(7, "Reduce Compendium Cost Drastically")
    listDemon.insert(8, "Improved Special Fusions")
    listDemon.insert(9, "Swap Guests/Panagia with Demons")
    listDemon.insert(10, "Include Demi-Fiend as Guest Swap")
    listDemon.pack()

    voiceLabel = tk.Label(page1FrameLeft, text="Demon Voice Randomizer")
    voiceLabel.pack()

    listVoice = tk.Listbox(page1FrameLeft, selectmode = "single", width=50, height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listVoice.insert(0, "Disabled")
    listVoice.insert(1, "Shuffle Demons' Voices")
    listVoice.insert(2, "Shuffle Voice Lines Individually (Chaotic)")
    listVoice.selection_set(0)
    listVoice.pack()

    #demonScrollbar = tk.Scrollbar(page1FrameTop, orient='vertical')
    #demonScrollbar.config(command=listDemon.yview)
    #listDemon.config(yscrollcommand=demonScrollbar.set)
    #listDemon.grid(row=1, column=0, sticky="nsew", padx = [10,0])
    #demonScrollbar.grid(row=1, column=1, sticky="ns")
    #page1FrameTop.grid_rowconfigure(0, weight=1)
    #page1FrameTop.grid_columnconfigure(0, weight=1)

    demonResLabel = tk.Label(page1FrameLeft, text="Demon Resistances")
    demonResLabel.pack()

    listDemonResistances = tk.Listbox(page1FrameLeft, selectmode = "multiple", height=6,width = 75, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listDemonResistances.insert(0, "Randomize Resistances")
    listDemonResistances.insert(1, "Always at least one Weakness/Resistance")
    listDemonResistances.insert(2, "Scale Elemental Resistances To Level")
    listDemonResistances.insert(3, "Scale Phys Resistance To Level")
    listDemonResistances.insert(4, "Weight Resistance by Potential")
    listDemonResistances.insert(5, "Diversify Resistances")
    listDemonResistances.pack()

    inheritanceLabel = tk.Label(page1FrameRight, text="Unique Skill Inheritance")
    inheritanceLabel.pack()

    listInheritance = tk.Listbox(page1FrameRight,selectmode= "single",height=3,exportselection=False, selectbackground = NAHOBINO_BLUE)
    listInheritance.insert(0, "Vanilla")
    listInheritance.insert(1, "Random")
    listInheritance.insert(2, "Free")
    listInheritance.selection_set(0)
    listInheritance.pack()

    magatsuhiLabel = tk.Label(page1FrameRight, text="Magatsuhi Skills")
    magatsuhiLabel.pack()

    listMagatsuhi = tk.Listbox(page1FrameRight,selectmode= "multiple",height=4,width=50,exportselection=False, selectbackground = NAHOBINO_BLUE)
    listMagatsuhi.insert(0, "Randomize Requirements to Use Magatsuhi Skills")
    listMagatsuhi.insert(1, "Include Omagatoki:Critical Requirement")
    listMagatsuhi.insert(2, "Include Omnipotent Succession Requirement")
    listMagatsuhi.selection_set(0)
    listMagatsuhi.pack()

    skillsLabel = tk.Label(page1FrameTopRight, text="Demon Skill Settings")
    skillsLabel.pack()

    listSkills = tk.Listbox(page1FrameTopRight, selectmode = "multiple", width = 75,height=9, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listSkills.insert(0, "Randomize Innate Skills")
    listSkills.insert(1, "Randomize Skills")
    listSkills.insert(2, "Weight Skills by Potentials")
    listSkills.insert(3, "Unique Skills can show up more than once")
    listSkills.insert(4, "Restrict Lunation Flux to one demon")
    listSkills.insert(5, "Include Enemy Only Skills in Skill Pool")
    listSkills.insert(6, "Include Magatsuhi Skills in Skill Pool")
    listSkills.insert(7, "Force & Minimize Appearance of Skills in Learnsets")
    listSkills.insert(8, "Skills are limited by Max MP of demon")
    listSkills.pack()

    skillScalingLabel = tk.Label(page1FrameTopRight, text="Skill Level Scaling")
    skillScalingLabel.pack()

    listSkillScaling = tk.Listbox(page1FrameTopRight, selectmode = "single",width=50,height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listSkillScaling.insert(0, "Completely Random")
    listSkillScaling.insert(1, "Weight Skills by Level")
    listSkillScaling.insert(2, "Strictly Scale Skills to Level")
    listSkillScaling.selection_set(0)
    listSkillScaling.pack()

    def toggleSkillScalingListbox(event):
        if 1 in listSkills.curselection():
            listSkillScaling.config(state=tk.NORMAL,bg="White")
        else:
            listSkillScaling.config(state=tk.DISABLED, bg=DISABLED_GRAY)


    listSkills.bind("<<ListboxSelect>>", toggleSkillScalingListbox)
        
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

    musicLabel = tk.Label(page2FrameLeft, text="Boss Music Setting")
    musicLabel.pack()

    listMusic = tk.Listbox(page2FrameLeft, selectmode = "single", height=3,exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listMusic.insert(0, "Boss-based")
    listMusic.insert(1, "Check-based")
    listMusic.insert(2, "Random")
    listMusic.selection_set(0)
    listMusic.pack()
    
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
    listBossSettings.insert(7, "No early phys immunity")
    listBossSettings.pack()

    bossResLabel = tk.Label(page2FrameRight, text="Boss Resistances")
    bossResLabel.pack()

    listBossResistances = tk.Listbox(page2FrameRight, selectmode = "multiple", width=50, height = 5, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listBossResistances.insert(0, "Randomize Resistances")
    listBossResistances.insert(1, "Scale Resistances to Check")
    listBossResistances.insert(2, "Consistent Weakness Count for Boss (or Check)")
    listBossResistances.insert(4, "Sync to Player Version if Possible")
    listBossResistances.insert(5, "Diversify Resistances")
    listBossResistances.pack()

    bossTurnLabel = tk.Label(page2FrameRight, text="Chance for bosses to receive additional press turns")
    bossTurnLabel.pack()
    
    bossTurnScale = tk.Scale(page2FrameRight, from_=0.0, to=7.0, resolution=0.1, orient=tk.HORIZONTAL, bg=PRESS_TURN_RED, troughcolor="Black", activebackground=PRESS_TURN_BRIGHT_RED)
    bossTurnScale.set(0)
    bossTurnScale.pack()

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

    bossSkillLabel = tk.Label(page3FrameLeft, text="Boss Skills")
    bossSkillLabel.pack()

    listBossSkills = tk.Listbox(page3FrameLeft, selectmode = "multiple", width=50, height = 8, exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listBossSkills.insert(0, "Randomize Boss Skills")
    listBossSkills.insert(1, "Similiar Skill Rank")
    listBossSkills.insert(2, "Allow Magatsuhi Skills")
    listBossSkills.insert(3, "Allow Contempt of God")
    listBossSkills.insert(4, "Preserve Elemental Slots per Boss")
    listBossSkills.insert(5, "Add Impaler's Revenge if possible")
    listBossSkills.pack()

    passiveLabel = tk.Label(page3FrameLeft, text="Additional Passive Skills on Bosses")
    passiveLabel.pack()

    listPassive = tk.Listbox(page3FrameLeft,selectmode= "single",height=4, width = 50,exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listPassive.insert(0, "None")
    listPassive.insert(1, "Fill Up All Empty Slots")
    listPassive.insert(2, "Game Progression Scaling")
    listPassive.insert(3, "Level Gap Scaling")
    listPassive.selection_set(0)
    listPassive.pack()

    magatsuhiHarvestLabel = tk.Label(page3FrameRight, text="Generic Boss Magatsuhi")
    magatsuhiHarvestLabel.pack()

    listMagatsuhiHarvest = tk.Listbox(page3FrameRight,selectmode= "single",height=4,width=30,exportselection=False, selectbackground = VENGEANCE_PURPLE)
    listMagatsuhiHarvest.insert(0, "Vanilla")
    listMagatsuhiHarvest.insert(1, "If possible: Omagatoki:Critical")
    listMagatsuhiHarvest.insert(2, "If possible: Omagatoki:Pierce")
    listMagatsuhiHarvest.insert(3, "Random")
    listMagatsuhiHarvest.selection_set(0)
    listMagatsuhiHarvest.pack()

    itemSmallFrame2 = tk.Frame(page5FrameBottom,width=333, height=250,background="#cccccc")
    itemSmallFrame2.grid(row=0, column=0)
    itemSmallFrame2.pack_propagate(False)

    itemSmallFrame = tk.Frame(page5FrameBottom,width=333, height=250,background="#cccccc")
    itemSmallFrame.grid(row=0, column=1)
    itemSmallFrame.pack_propagate(False)

    itemInclusionLabel = tk.Label(itemSmallFrame2, text="Include Specific Items/Checks")
    itemInclusionLabel.pack()
    
    listItemInclusionOrder = ["Tsukuyomi Talisman as Gift","Empyrean Keys as Gifts","Include Mitama Drops as Basic Enemy Drops","Basic Enemies always drop Lifestone or Chakra Drop","Vending Machines have a higher chance for relics"]
    itemInclusionList = tk.Listbox(itemSmallFrame2, selectmode = "multiple", width = 75,height=len(listItemInclusionOrder), exportselection=False, selectbackground = NAHOBINO_BLUE)
    for index, item in enumerate(listItemInclusionOrder):
        itemInclusionList.insert(index,item)
    itemInclusionList.pack()

    itemRedoableCheckLabel = tk.Label(itemSmallFrame, text="Allow Item in Repeatable Check\n(Drops, Vending Machines)") #, Navigator Spots
    itemRedoableCheckLabel.pack()
    
    listRedoableOrder = ["Gospel","Grimoire","Whittled Goat","Essences (except fixed ones)","Incenses / Balms / Sutras",]
    listItemRedoable = tk.Listbox(itemSmallFrame, selectmode="multiple", width=45, height=len(listRedoableOrder), exportselection=False, selectbackground=NAHOBINO_BLUE)
    for index, item in enumerate(listRedoableOrder):
        listItemRedoable.insert(index,item)
    listItemRedoable.pack()    

    itemVanillaFrame = tk.Frame(page5FrameTop,width=200, height=250,background="#cccccc")
    itemVanillaFrame.grid(row=0, column=0)
    itemVanillaFrame.pack_propagate(False)

    itemSelfFrame = tk.Frame(page5FrameTop,width=200, height=250,background="#cccccc")
    itemSelfFrame.grid(row=0, column=1)
    itemSelfFrame.pack_propagate(False)

    itemSharedFrame = tk.Frame(page5FrameTop,width=200, height=250,background="#cccccc")
    itemSharedFrame.grid(row=0, column=2)
    itemSharedFrame.pack_propagate(False)

    itemOtherFrame = tk.Frame(page5FrameTop,width=400, height=250,background="#cccccc")
    itemOtherFrame.grid(row=0, column=3)
    itemOtherFrame.pack_propagate(False)

    itemScaleLabel = tk.Label(itemOtherFrame, text="Item Scaling Modes")
    itemScaleLabel.pack()

    itemScaleList = tk.Listbox(itemOtherFrame, selectmode = "multiple", width = 30, height=2, exportselection=False, selectbackground = NAHOBINO_BLUE)
    itemScaleList.insert(0, "Scale Macca per Area")
    itemScaleList.insert(1, "Scale Items per Area") #TODO: Maybe Weight Items per Area
    itemScaleList.pack()

    itemRandomLabel = tk.Label(itemOtherFrame, text="Item Random Modes")
    itemRandomLabel.pack()

    listRandomItem = tk.Listbox(itemOtherFrame, selectmode = "single", width = 50,height=2, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listRandomItem.insert(0, "Shuffle all existing item rewards")
    listRandomItem.insert(1, "Shuffle important items, generate the rest randomly")
    listRandomItem.selection_set(0)
    listRandomItem.pack()

    itemLabel = tk.Label(itemOtherFrame, text="Shop Randomizer")
    itemLabel.pack()

    listItem = tk.Listbox(itemOtherFrame, selectmode = "multiple", height= 2, width = 30, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listItem.insert(0, "Randomize Shop Items")
    listItem.insert(1, "Randomize Shop Essences") 
    #TODO:"Navigator Spots" maybe at some point
    listItem.pack()

    itemVanillaLabel = tk.Label(itemVanillaFrame, text="Vanilla Item Pools")
    itemVanillaLabel.pack()

    listItemsOrder = [v for v in VANILLA_LIST_ITEMS_ORDER]
    listItemVanilla = tk.Listbox(itemVanillaFrame, selectmode="multiple",width=30, height=len(listItemsOrder), exportselection=False, selectbackground=NAHOBINO_BLUE)
    for index, item in enumerate(listItemsOrder):
        listItemVanilla.insert(index,item)
    listItemVanilla.pack()

    itemSelfLabel = tk.Label(itemSelfFrame, text="Independent Item Pools")
    itemSelfLabel.pack()

    listItemSelf = tk.Listbox(itemSelfFrame, selectmode="multiple", width=30, height=len(listItemsOrder), exportselection=False, selectbackground=NAHOBINO_BLUE)
    listItemSelf.pack()

    itemSharedLabel = tk.Label(itemSharedFrame, text="Mixed Item Pools")
    itemSharedLabel.pack()

    listItemShared = tk.Listbox(itemSharedFrame, selectmode="multiple", width=30, height=len(listItemsOrder), exportselection=False, selectbackground=NAHOBINO_BLUE)
    listItemShared.pack()

    def moveItemsBetweenLists(source, target):
        selected_indices = sorted(source.curselection(), reverse=True)
        for index in selected_indices:
            item = source.get(index)
            source.delete(index)
            
            trueIndex = tk.END
            itemIndex = listItemsOrder.index(item)
            
            for i in range(target.size()):
                targetItem = target.get(i)
                if listItemsOrder.index(targetItem) > itemIndex:
                    trueIndex = i
                    break
            
            target.insert(trueIndex, item)

    def resetItemCheckLists():
        listItemVanilla.delete(0,tk.END)
        listItemSelf.delete(0,tk.END)
        listItemShared.delete(0,tk.END)
        listItemsOrder = [v for v in VANILLA_LIST_ITEMS_ORDER]
        for index, item in enumerate(listItemsOrder):
            listItemVanilla.insert(index,item)
        

    moveToSelfButton = tk.Button(itemVanillaFrame, text="→ Independent", command=lambda: moveItemsBetweenLists(listItemVanilla, listItemSelf))
    moveToSelfButton.pack()

    moveToSharedButton = tk.Button(itemVanillaFrame, text="→ Mixed", command=lambda: moveItemsBetweenLists(listItemVanilla, listItemShared))
    moveToSharedButton.pack()

    moveToVanillaFromSelfButton = tk.Button(itemSelfFrame, text="← Vanilla", command=lambda: moveItemsBetweenLists(listItemSelf, listItemVanilla))
    moveToVanillaFromSelfButton.pack()

    moveToSharedFromSelfButton = tk.Button(itemSelfFrame, text="→ Mixed", command=lambda: moveItemsBetweenLists(listItemSelf, listItemShared))
    moveToSharedFromSelfButton.pack()

    moveToVanillaFromSharedButton = tk.Button(itemSharedFrame, text="← Vanilla", command=lambda: moveItemsBetweenLists(listItemShared, listItemVanilla))
    moveToVanillaFromSharedButton.pack()

    moveToSelfFromSharedButton = tk.Button(itemSharedFrame, text="← Independent", command=lambda: moveItemsBetweenLists(listItemShared, listItemSelf))
    moveToSelfFromSharedButton.pack()


    miracleLabel = tk.Label(page4FrameTopLeft, text="Miracle Randomizer")
    miracleLabel.pack()

    listMiracle = tk.Listbox(page4FrameTopLeft, selectmode = "multiple", width = 75, height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listMiracle.insert(0, "Randomize Miracle unlocks")
    listMiracle.insert(1, "Randomize Miracle prices")
    listMiracle.insert(2, "Learn +3 stock Divine Garrisons first")            
    listMiracle.pack()
    
    rankViolationLabel = tk.Label(page4FrameTopLeft, text="Rank Violation")
    rankViolationLabel.pack()

    listRankViolation = tk.Listbox(page4FrameTopLeft, selectmode = "single", width = 50, height=3, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listRankViolation.insert(0, "Randomize Rank Violation")
    listRankViolation.insert(1, "Vanilla Rank Violation")
    listRankViolation.insert(2, "Guarantee Rank Violation early")
    listRankViolation.selection_set(0)
    listRankViolation.pack()
    
    earlyMiracleLabel = tk.Label(page4FrameTopRight, text="Miracles to guarantee early")
    earlyMiracleLabel.pack()

    listEarlyMiracle = tk.Listbox(page4FrameTopRight, selectmode = "multiple", width = 50, height=8, exportselection=False, selectbackground = NAHOBINO_BLUE)
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
    
    uniqueSkillAnimationsNote = tk.Label(page4FrameBottomLeft, text="If the wrong demon uses a unique skill, \nthe game will hang until the skip animations button is pressed.\n"
                                         + "The 'Fix unique skill animations' patch replaces \nunique skill anims with normal skill anims to get around this.")
    uniqueSkillAnimationsNote.pack()

    patchesLabel = tk.Label(page4FrameBottomLeft, text="Patches")
    patchesLabel.pack()

    listPatches = tk.Listbox(page4FrameBottomLeft, selectmode = "multiple", width=50, height=5, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listPatches.insert(0, "Fix unique skill animations")
    listPatches.insert(1, "Buff guest Yuzuru to make first Labolas check easier")
    listPatches.insert(2, "Unlock all fusions from the start")
    listPatches.insert(3, "Remove non-essential cutscenes (Up to end of first Da'at)")
    listPatches.insert(4, "Remove Tutorials")
    listPatches.pack()

    naviLabel = tk.Label(page4FrameBottomRight, text="Demon Navigators")
    naviLabel.pack()

    listNavi = tk.Listbox(page4FrameBottomRight, selectmode = "multiple", width = 75, height = 2, exportselection=False, selectbackground = NAHOBINO_BLUE)
    listNavi.insert(0, "Randomize Navigator Stats")
    listNavi.insert(1, "Navigator Model Swaps")
    listNavi.pack()

    expLabel = tk.Label(page4FrameBottomRight, text="EXP Multiplier")
    expLabel.pack()
    
    expScale = tk.Scale(page4FrameBottomRight, from_=1, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg=NAHOBINO_BLUE, troughcolor="Black", activebackground=NAHOBINO_BRIGHT_BLUE)
    expScale.set(1)
    expScale.pack()

    pressTurnLabel = tk.Label(page4FrameBottomRight, text="Chance for basic enemies to receive additional press turns")
    pressTurnLabel.pack()

    pressTurnScale = tk.Scale(page4FrameBottomRight, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, bg=NAHOBINO_BLUE, troughcolor="Black", activebackground=NAHOBINO_BRIGHT_BLUE)
    pressTurnScale.set(0.0)
    pressTurnScale.pack()
        
    page1Frame.tkraise()
    
    def ApplySettings(configur, preset = False):
        resetItemCheckLists()
        UI_MAP = {
            'Patches': {
                'swapCutsceneModels': ('Checkbutton',swapCutsceneModelCheckbox),
                'FixUniqueSkillAnimations': ('Listbox', listPatches, 0),
                'BuffGuestYuzuru': ('Listbox', listPatches, 1),
                'UnlockFusions': ('Listbox', listPatches, 2),
                'SkipCutscenes': ('Listbox', listPatches, 3),
                'SkipTutorials': ('Listbox', listPatches, 4),
            },
            'Demon': {
                'RandomLevels': ('Listbox', listDemon, 0),
                'RandomPotentials': ('Listbox', listDemon, 1),
                'ScaledPotentials': ('Listbox', listDemon, 2),
                'randomRaces': ('Listbox', listDemon, 3),
                'randomAlignment': ('Listbox', listDemon, 4),
                'ensureDemonJoinLevel': ('Listbox', listDemon, 5),
                'RandomDemonStats': ('Listbox', listDemon, 6),
                'ReduceCompendiumCost': ('Listbox', listDemon, 7),
                'BetterSpecialFusions': ('Listbox', listDemon, 8),
                'swapGuestsWithDemons': ('Listbox', listDemon, 9),
                'swapDemifiend': ('Listbox', listDemon, 10),

                'RandomSkills': ('Listbox', listSkills, 1),
                'RandomInnates': ('Listbox', listSkills, 0),
                'WeightSkillsToPotentials': ('Listbox', listSkills, 2),
                'multipleUniques': ('Listbox', listSkills, 3),
                'RestrictLunationFlux': ('Listbox', listSkills, 4),
                'EnemyOnlySkills': ('Listbox', listSkills, 5),
                'MagatsuhiSkills': ('Listbox', listSkills, 6),
                'ForceUniqueSkills': ('Listbox', listSkills, 7),
                'LimitSkillMPCost': ('Listbox', listSkills, 8),

                'ScaledSkills': ('Listbox_single', listSkillScaling, 2),
                'WeightSkillsToLevels': ('Listbox_single', listSkillScaling, 1)
                
            },
            'Voice': {
                'RandomVoicesNormal': ('Listbox_single', listVoice, 1),
                'RandomVoicesChaos': ('Listbox_single', listVoice, 2),
            },
            'Resistances': {
                'RandomResists': ('Listbox', listDemonResistances, 0),
                'AlwaysOneWeak': ('Listbox', listDemonResistances, 1),
                'ScaleElementalResist': ('Listbox', listDemonResistances, 2),
                'ScalePhysResist': ('Listbox', listDemonResistances, 3),
                'WeightResistByPotentials': ('Listbox', listDemonResistances, 4),
                'DiverseResists': ('Listbox', listDemonResistances, 5),

                'RandomBossResists': ('Listbox', listBossResistances, 0),
                'ConsistenBossWeakCount': ('Listbox', listBossResistances, 2),
                'ScaleResistToCheck': ('Listbox', listBossResistances, 1),
                'PlayerResistSync': ('Listbox', listBossResistances, 3),
                'DiverseBossResist': ('Listbox', listBossResistances, 4),
            },
            'Inheritance': {
                'RandomInheritance': ('Listbox_single', listInheritance, 1),
                'FreeInheritance': ('Listbox_single', listInheritance, 2),
            },
            'Magatsuhi': {
                'RandomRequirements': ('Listbox', listMagatsuhi, 0),
                'IncludeCritical': ('Listbox', listMagatsuhi, 1),
                'IncludeSuccession': ('Listbox', listMagatsuhi, 2),
            },
            'Music': {
                'RandomMusic': ('Listbox_single', listMusic, 2),
                'CheckBasedMusic': ('Listbox_single', listMusic, 1),
            },
            'Item': {
                'RandomShopItems': ('Listbox', listItem, 0),
                'RandomShopEssences': ('Listbox', listItem, 1),

                'ScaleMaccaPerArea': ('Listbox', itemScaleList, 0),
                'ScaleItemsPerArea': ('Listbox', itemScaleList, 1),
                'ShuffleExistingItems': ('Listbox_single', listRandomItem, 0),
                'TrulyRandomizeItems': ('Listbox_single', listRandomItem, 1),
                
                'IncludeTsukuyomiTalismanAsGift': ('Listbox', itemInclusionList, 0),
                'IncludeEmpyreanKeysAsGifts': ('Listbox', itemInclusionList, 1),
                'RandomizeMitamaDrops': ('Listbox', itemInclusionList, 2),
                'LifestoneOrChakraDrop': ('Listbox', itemInclusionList, 3),
                'relicBiasVendingMachine': ('Listbox', itemInclusionList, 4),

                
                
                'SelfItems': ('Listbox_Item_Move', listItemSelf),
                'SharedItems': ('Listbox_Item_Move', listItemShared),


                'RedoableGospel': ('Listbox', listItemRedoable, 0),
                'RedoableGrimoire': ('Listbox', listItemRedoable, 1),
                'RedoableWhittledGoat': ('Listbox', listItemRedoable, 2),   
                'RedoableEssences': ('Listbox', listItemRedoable, 3),
                'RedoableIncensesBalmsSutras': ('Listbox', listItemRedoable, 4),

            },
            'Boss': {
                'NormalBossesSelf': ('Listbox_single', listBoss, 1),
                'NormalBossesMixed': ('Listbox_single', listBoss, 2),
                'AbscessBossesSelf': ('Listbox_single', listAbscess, 1),
                'AbscessBossesMixed': ('Listbox_single', listAbscess, 2),
                'OverworldBossesSelf': ('Listbox_single', listPunishing, 1),
                'OverworldBossesMixed': ('Listbox_single', listPunishing, 2),
                'SuperbossesSelf': ('Listbox_single', listSuperboss, 1),
                'SuperbossesMixed': ('Listbox_single', listSuperboss, 2),
                'MinibossesSelf': ('Listbox_single', listMiniboss, 1),
                'MinibossesMixed': ('Listbox_single', listMiniboss, 2),

               'ScaleBossDamage': ('Listbox', listBossSettings, 0), 
               'ScalePressTurns': ('Listbox', listBossSettings, 1), 
               'RandomizeLucifer': ('Listbox', listBossSettings, 2), 
               'PreventEarlyAmbush': ('Listbox', listBossSettings, 3), 
               'BossDependentAmbush': ('Listbox', listBossSettings, 4), 
               'NerfBossHealing': ('Listbox', listBossSettings, 5), 
               'ScaleInstakillRates': ('Listbox', listBossSettings, 6), 
               'bossNoEarlyPhysImmunity': ('Listbox', listBossSettings, 7), 

               'RandomizeIshtarPressTurns': ('Checkbutton',ishtarRandomizeCheckbox),

               'RandomizeBossSkills': ('Listbox', listBossSkills, 0),
               'similiarBossSkillRank': ('Listbox', listBossSkills, 1),
               'allowBossMagatsuhiSkill': ('Listbox', listBossSkills, 2),
               'allowContemptOfGod': ('Listbox', listBossSkills, 3),
               'elementCountConsistency': ('Listbox', listBossSkills, 4),
               'addImpalersRevenge': ('Listbox', listBossSkills, 5),

               'fillEmptySlotsWithPassives': ('Listbox_single', listPassive, 1),
               'scalePassiveAmount': ('Listbox_single', listPassive, 2),
               'scalePassiveLevelGap': ('Listbox_single', listPassive, 3),

               'alwaysCritical': ('Listbox_single', listMagatsuhiHarvest, 1),
               'alwaysPierce': ('Listbox_single', listMagatsuhiHarvest, 2), 
               'randomMagatsuhi': ('Listbox_single', listMagatsuhiHarvest, 3),  
            },
            'Miracle': {
                'RandomMiracleUnlocks': ('Listbox', listMiracle, 0),
                'RandomMiracleCosts': ('Listbox', listMiracle, 1),
                'ReverseDivineGarrisons': ('Listbox', listMiracle, 2),

                'VanillaRankViolation': ('Listbox_single', listRankViolation, 1),
                'EarlyRankViolation': ('Listbox_single', listRankViolation, 2),

                'EarlyDivineGarrison': ('Listbox', listEarlyMiracle, 0),
                'EarlyForestall': ('Listbox', listEarlyMiracle, 1),
                'EarlyEmpoweringCheer': ('Listbox', listEarlyMiracle, 2),
                'EarlyArtOfEssences': ('Listbox', listEarlyMiracle, 3),
                'EarlyDemonProficiency': ('Listbox', listEarlyMiracle, 4),
                'EarlyDivineProficiency': ('Listbox', listEarlyMiracle, 5),
                'EarlyDivineAmalgamation': ('Listbox', listEarlyMiracle, 6),
                'EarlyInheritenceViolation': ('Listbox', listEarlyMiracle, 7),
            },
            'Navigators': {
                'RandomNavigatorStats': ('Listbox', listNavi, 0),
                'NavigatorModelSwap': ('Listbox', listNavi, 1),
            },
        }
        listVoice.selection_set(0)
        listSkillScaling.selection_set(0)
        listInheritance.selection_set(0)
        listMusic.selection_set(0)
        listBoss.selection_set(0)
        listAbscess.selection_set(0)
        listPunishing.selection_set(0)
        listSuperboss.selection_set(0)
        listMiniboss.selection_set(0)
        listPassive.selection_set(0)
        listMagatsuhiHarvest.selection_set(0)
        listRankViolation.selection_set(0)
        listRandomItem.selection_set(0)
        toggleMiracleListboxes(None)
        toggleSkillScalingListbox(None)

        if not preset:
            nonlocal oldSeed
            oldSeed = configur.get("Seed", "lastSeed")

        def applyUISetting(config, section, key, element, elementType, index=None, element2=None):
            value = config.get(section, key) == 'true'
            if section == "Miracle":
                toggleMiracleListboxes(None)
            if section == "Demon":
                toggleSkillScalingListbox(None)
            if elementType == 'Checkbutton':
                if value:
                    element.select()
                else:
                    element.deselect()
            elif elementType == 'Listbox':
                if value:
                    element.selection_set(index)
                else:
                    element.selection_clear(index)
            elif elementType == 'Listbox_single':
                if value:
                    element.selection_clear(0)
                    element.selection_set(index)
                else:
                    element.selection_clear(index)
            elif elementType =="Listbox_Item_Move":
                itemList = config.get(section, key).split(',')
                for i in range(element2.size()):
                    if element2.get(i) in itemList:
                        element2.selection_set(i)
                moveItemsBetweenLists(element2,element)
  
        for section, keys in UI_MAP.items():
            for key, (elementType, element, *index) in keys.items():
                if elementType == 'Listbox_Item_Move':
                    applyUISetting(configur, section, key, element, elementType, element2 = listItemVanilla)
                else:
                    applyUISetting(configur, section, key, element, elementType, index[0] if index else None)
        
        toggleIshtarCheckbox()
        ishtarScale.set(configur.get('Boss', 'IshtarPressTurns'))
        bossTurnScale.set(configur.get('Boss', 'BossPressTurnChance'))
        toggleMiracleListboxes(None)
        toggleSkillScalingListbox(None)
        
        expScale.set(configur.get('Patches', 'EXPMultiplier'))
        pressTurnScale.set(configur.get('Patches','PressTurnChance'))
        
        
    #Set starting GUI values based on saved user settings
    configur = ConfigParser()
    if os.path.exists('config.ini'):
        configur.read('config.ini')

        try:
            ApplySettings(configur)
        except (NoOptionError, NoSectionError) as e:
            print(f"Error: {e}")
            createConfigFile(configur)
            ApplySettings(configur)
    else:
        createConfigFile(configur)
        ApplySettings(configur)
    window.mainloop()
    
    try:
        #Store all GUI selections into variables before closing the GUI
        textSeed = seedEntry.get()
        cutsceneChoice = swapCutsceneModels.get()
        demonFlags = [False for i in range(listDemon.size())]
        for i in listDemon.curselection():
            demonFlags[i] = True
        voiceChoice = listVoice.curselection()
        demonResistFlags = [False for i in range(listDemonResistances.size())]
        for i in listDemonResistances.curselection():
            demonResistFlags[i] = True
        skillFlags = [False for i in range(listSkills.size())]
        for i in listSkills.curselection():
            skillFlags[i] = True
        skillScaleChoice = listSkillScaling.curselection()
        inheritanceChoice = listInheritance.curselection()
        magatsuhiFlags = [False for i in range(listMagatsuhi.size())]
        for i in listMagatsuhi.curselection():
            magatsuhiFlags[i] = True
        musicChoice = listMusic.curselection()
        itemFlags = [False for i in range(listItem.size())]
        for i in listItem.curselection():
            itemFlags[i] = True
        bossFlags = [False for i in range(listBossSettings.size())]
        for i in listBossSettings.curselection():
            bossFlags[i] = True
        bossResistFlags = [False for i in range(listBossResistances.size())]
        for i in listBossResistances.curselection():
            bossResistFlags[i] = True
        normalBossChoice = listBoss.curselection()
        abscessChoice = listAbscess.curselection()
        punishingChoice = listPunishing.curselection()
        superbossChoice = listSuperboss.curselection()
        minibossChoice = listMiniboss.curselection()
        ishtarChoice = ishtarScale.get()
        bossTurnChoice = bossTurnScale.get()
        bossSkillFlags = [False for i in range(listBossSkills.size())]
        for i in listBossSkills.curselection():
            bossSkillFlags[i] = True
        passiveChoice = listPassive.curselection()
        magatsuhiHarvestChoice = listMagatsuhiHarvest.curselection()
        ishtarRandomizeChoice = randomIshtarPressTurnsVar.get()
        itemScaleFlags = [False for i in range(itemScaleList.size())]
        for i in itemScaleList.curselection():
            itemScaleFlags[i] = True
        itemRandomChoice = listRandomItem.curselection()
        itemInclusionFlags = [False for i in range(itemInclusionList.size())]
        for i in itemInclusionList.curselection():
            itemInclusionFlags[i] = True
        itemsSelfChoice = listItemSelf.get(0,tk.END)
        itemsSharedChoice = listItemShared.get(0,tk.END)
        redoableItemFlags = [False for i in range(listItemRedoable.size())]
        for i in listItemRedoable.curselection():
            redoableItemFlags[i] = True
        
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
        naviFlags = [False for i in range(listNavi.size())]
        for i in listNavi.curselection():
            naviFlags[i] = True
        expChoice = expScale.get()
        pressTurnChoice = pressTurnScale.get()
        
        window.destroy()
    except tk.TclError:
        raise(RuntimeError)        

    #Set the config settings
    configSettings.swapCutsceneModels = cutsceneChoice
    configur.set('Patches', 'swapCutsceneModels', str(cutsceneChoice).lower())
    configSettings.randomDemonLevels = demonFlags[0]
    configur.set('Demon', 'RandomLevels', str(demonFlags[0]).lower())
    configSettings.randomPotentials = demonFlags[1]
    configur.set('Demon', 'RandomPotentials', str(demonFlags[1]).lower())
    configSettings.scaledPotentials = demonFlags[2]
    configur.set('Demon', 'ScaledPotentials', str(demonFlags[2]).lower())
    configSettings.randomRaces = demonFlags[3]
    configur.set('Demon', 'randomRaces', str(demonFlags[3]).lower())
    configSettings.randomAlignment = demonFlags[4]
    configur.set('Demon', 'randomAlignment', str(demonFlags[4]).lower())
    configSettings.ensureDemonJoinLevel = demonFlags[5]
    configur.set('Demon', 'ensureDemonJoinLevel', str(demonFlags[5]).lower())
    configSettings.randomDemonStats = demonFlags[6]
    configur.set('Demon', 'RandomDemonStats', str(demonFlags[6]).lower())
    configSettings.reduceCompendiumCosts = demonFlags[7]
    configur.set('Demon', 'ReduceCompendiumCost', str(demonFlags[7]).lower())
    configSettings.betterSpecialFusions = demonFlags[8]
    configur.set('Demon', 'BetterSpecialFusions', str(demonFlags[8]).lower())
    configSettings.swapGuestsWithDemons = demonFlags[9]
    configur.set('Demon', 'swapGuestsWithDemons', str(demonFlags[9]).lower())
    configSettings.swapDemifiend = demonFlags[10]
    configur.set('Demon', 'swapDemifiend', str(demonFlags[10]).lower())
    
    configSettings.randomInnates = skillFlags[0]
    configur.set('Demon', 'RandomInnates', str(skillFlags[0]).lower())
    configSettings.randomSkills = skillFlags[1]
    configur.set('Demon', 'RandomSkills', str(skillFlags[1]).lower())
    configSettings.potentialWeightedSkills = skillFlags[2]
    configur.set('Demon', 'WeightSkillsToPotentials', str(skillFlags[2]).lower())
    configSettings.multipleUniques = skillFlags[3]
    configur.set('Demon', 'multipleUniques', str(skillFlags[3]).lower())
    configSettings.restrictLunationFlux = skillFlags[4]
    configur.set('Demon', 'RestrictLunationFlux', str(skillFlags[4]).lower())
    configSettings.includeEnemyOnlySkills = skillFlags[5]
    configur.set('Demon', 'EnemyOnlySkills', str(skillFlags[5]).lower())
    configSettings.includeMagatsuhiSkills = skillFlags[6]
    configur.set('Demon', 'MagatsuhiSkills', str(skillFlags[6]).lower())
    configSettings.forceAllSkills = skillFlags[7]
    configur.set('Demon', 'ForceUniqueSkills', str(skillFlags[7]).lower())
    configSettings.limitSkillMPCost = skillFlags[7]
    configur.set('Demon', 'LimitSkillMPCost', str(skillFlags[7]).lower())

    configSettings.levelWeightedSkills = bool(skillScaleChoice and skillScaleChoice[0] == 1)
    configur.set('Demon', 'WeightSkillsToLevels', str(configSettings.levelWeightedSkills).lower())
    configSettings.scaledSkills = bool(skillScaleChoice and skillScaleChoice[0] == 2)
    configur.set('Demon', 'ScaledSkills', str(configSettings.scaledSkills).lower())

    configSettings.randomizeVoicesNormal = bool(voiceChoice and voiceChoice[0] == 1)
    configur.set('Voice', 'RandomVoicesNormal', str(configSettings.randomizeVoicesNormal).lower())
    configSettings.randomizeVoicesChaos = bool(voiceChoice and voiceChoice[0] == 2)
    configur.set('Voice', 'RandomVoicesChaos', str(configSettings.randomizeVoicesChaos).lower())
    
    configSettings.randomResists = demonResistFlags[0]
    configur.set('Resistances', 'RandomResists', str(demonResistFlags[0]).lower())
    configSettings.alwaysOneWeak = demonResistFlags[1]
    configur.set('Resistances', 'AlwaysOneWeak', str(demonResistFlags[1]).lower())
    configSettings.scaledElementalResists = demonResistFlags[2]
    configur.set('Resistances', 'ScaleElementalResist', str(demonResistFlags[2]).lower())
    configSettings.scaledPhysResists = demonResistFlags[3]
    configur.set('Resistances', 'ScalePhysResist', str(demonResistFlags[3]).lower())
    configSettings.potentialWeightedResists = demonResistFlags[4]
    configur.set('Resistances', 'WeightResistByPotentials', str(demonResistFlags[4]).lower())
    configSettings.diverseResists = demonResistFlags[5]
    configur.set('Resistances', 'DiverseResists', str(demonResistFlags[5]).lower())

    configSettings.randomInheritance = bool(inheritanceChoice and inheritanceChoice[0] == 1)
    configur.set('Inheritance', 'RandomInheritance', str(configSettings.randomInheritance).lower())
    configSettings.freeInheritance = bool(inheritanceChoice and inheritanceChoice[0] == 2)
    configur.set('Inheritance', 'FreeInheritance', str(configSettings.freeInheritance).lower())

    configSettings.randomizeMagatsuhiSkillReq = magatsuhiFlags[0]
    configur.set('Magatsuhi', 'RandomRequirements', str(magatsuhiFlags[0]).lower())
    configSettings.includeOmagatokiCritical = magatsuhiFlags[1]
    configur.set('Magatsuhi', 'IncludeCritical', str(magatsuhiFlags[1]).lower())
    configSettings.includeOmnipotentSuccession = magatsuhiFlags[2]
    configur.set('Magatsuhi', 'IncludeSuccession', str(magatsuhiFlags[2]).lower())
    
    configSettings.randomMusic = bool(musicChoice and musicChoice[0] == 2)
    configur.set('Music', 'RandomMusic', str(configSettings.randomMusic).lower())
    configSettings.checkBasedMusic = bool(musicChoice and musicChoice[0] == 1)
    configur.set('Music', 'CheckBasedMusic', str(configSettings.checkBasedMusic).lower())        

    configSettings.randomShopItems = itemFlags[0]
    configur.set('Item', 'RandomShopItems', str(itemFlags[0]).lower())
    configSettings.randomShopEssences = itemFlags[1]
    configur.set('Item', 'RandomShopEssences', str(itemFlags[1]).lower())    

    configSettings.scaleMaccaPerArea = itemScaleFlags[0]
    configur.set('Item', 'ScaleMaccaPerArea', str(itemScaleFlags[0]).lower())
    configSettings.scaleItemsPerArea = itemScaleFlags[1]
    configur.set('Item', 'ScaleItemsPerArea', str(itemScaleFlags[1]).lower())
    configSettings.shuffleExistingItems = bool(itemRandomChoice and itemRandomChoice[0] == 0)
    configur.set('Item', 'ShuffleExistingItems', str(configSettings.shuffleExistingItems).lower())
    configSettings.trulyRandomizeItems = bool(itemRandomChoice and itemRandomChoice[0] == 1)
    configur.set('Item', 'TrulyRandomizeItems', str(configSettings.trulyRandomizeItems).lower())

    configSettings.includeTsukuyomiTalismanAsGift = itemInclusionFlags[0]
    configur.set('Item', 'IncludeTsukuyomiTalismanAsGift', str(itemInclusionFlags[0]).lower())
    configSettings.includeEmpyreanKeysAsGifts = itemInclusionFlags[1]
    configur.set('Item', 'IncludeEmpyreanKeysAsGifts', str(itemInclusionFlags[1]).lower())
    configSettings.randomizeMitamaDrops = itemInclusionFlags[2]
    configur.set('Item', 'RandomizeMitamaDrops', str(itemInclusionFlags[2]).lower())
    configSettings.lifestoneOrChakraDrop = itemInclusionFlags[3]
    configur.set('Item', 'LifestoneOrChakraDrop', str(itemInclusionFlags[3]).lower())
    configSettings.relicBiasVendingMachine = itemInclusionFlags[4]
    configur.set('Item', 'relicBiasVendingMachine', str(itemInclusionFlags[4]).lower()) 

    configSettings.redoableGospel = redoableItemFlags[0]
    configur.set('Item', 'RedoableGospel', str(redoableItemFlags[0]).lower())
    configSettings.redoableGrimoire = redoableItemFlags[1]
    configur.set('Item', 'RedoableGrimoire', str(redoableItemFlags[1]).lower())
    configSettings.redoableWhittledGoat = redoableItemFlags[2]
    configur.set('Item', 'RedoableWhittledGoat', str(redoableItemFlags[2]).lower())
    configSettings.redoableEssencesAllowed = redoableItemFlags[3]
    configur.set('Item', 'RedoableEssences', str(redoableItemFlags[3]).lower())
    configSettings.redoableIncensesBalmsSutras = redoableItemFlags[4]
    configur.set('Item', 'RedoableIncensesBalmsSutras', str(redoableItemFlags[4]).lower())

    for item in itemsSelfChoice:
        configSettings.selfItemPools.append(item)
    configur.set('Item', 'SelfItems', ','.join(itemsSelfChoice))
    for item in itemsSharedChoice:
        configSettings.sharedItemPools.append(item)
    configur.set('Item', 'SharedItems', ','.join(itemsSharedChoice))
    

    configSettings.randomizeNavigatorStats = naviFlags[0]
    configur.set('Navigators', 'RandomNavigatorStats', str(naviFlags[0]).lower())
    configSettings.navigatorModelSwap = naviFlags[1]
    configur.set('Navigators', 'NavigatorModelSwap', str(naviFlags[1]).lower()) 
    
    configSettings.scaleBossDamage = bossFlags[0]
    configur.set('Boss', 'ScaleBossDamage', str(bossFlags[0]).lower())
    configSettings.scaleBossPressTurnsToCheck = bossFlags[1]
    configur.set('Boss', 'ScalePressTurns', str(bossFlags[1]).lower())
    configSettings.randomizeLucifer = bossFlags[2]
    configur.set('Boss', 'RandomizeLucifer', str(bossFlags[2]).lower())
    configSettings.preventEarlyAmbush = bossFlags[3]
    configur.set('Boss', 'PreventEarlyAmbush', str(bossFlags[3]).lower())
    configSettings.bossDependentAmbush = bossFlags[4]
    configur.set('Boss', 'BossDependentAmbush', str(bossFlags[4]).lower())
    configSettings.nerfBossHealing = bossFlags[5]
    configur.set('Boss', 'NerfBossHealing', str(bossFlags[5]).lower())
    configSettings.scaleBossInstakillRates = bossFlags[6]
    configur.set('Boss', 'ScaleInstakillRates', str(bossFlags[6]).lower())
    configSettings.bossNoEarlyPhysImmunity = bossFlags[7]
    configur.set('Boss', 'BossNoEarlyPhysImmunity', str(bossFlags[7]).lower())

    configSettings.selfRandomizeNormalBosses = bool(normalBossChoice and normalBossChoice[0] == 1)
    configur.set('Boss', 'NormalBossesSelf', str(configSettings.selfRandomizeNormalBosses).lower())
    configSettings.mixedRandomizeNormalBosses = bool(normalBossChoice and normalBossChoice[0] == 2)
    configur.set('Boss', 'NormalBossesMixed', str(configSettings.mixedRandomizeNormalBosses).lower())   
    
    configSettings.selfRandomizeAbscessBosses = bool(abscessChoice and abscessChoice[0] == 1)
    configur.set('Boss', 'AbscessBossesSelf', str(configSettings.selfRandomizeAbscessBosses).lower())
    configSettings.mixedRandomizeAbscessBosses = bool(abscessChoice and abscessChoice[0] == 2)
    configur.set('Boss', 'AbscessBossesMixed', str(configSettings.mixedRandomizeAbscessBosses).lower())       
    
    configSettings.selfRandomizeOverworldBosses = bool(punishingChoice and punishingChoice[0] == 1)
    configur.set('Boss', 'OverworldBossesSelf', str(configSettings.selfRandomizeOverworldBosses).lower())
    configSettings.mixedRandomizeOverworldBosses = bool(punishingChoice and punishingChoice[0] == 2)
    configur.set('Boss', 'OverworldBossesMixed', str(configSettings.mixedRandomizeOverworldBosses).lower())       
            
    configSettings.selfRandomizeSuperbosses = bool(superbossChoice and superbossChoice[0] == 1)
    configur.set('Boss', 'SuperbossesSelf', str(configSettings.selfRandomizeSuperbosses).lower())
    configSettings.mixedRandomizeSuperbosses = bool(superbossChoice and superbossChoice[0] == 2)
    configur.set('Boss', 'SuperbossesMixed', str(configSettings.mixedRandomizeSuperbosses).lower()) 
        
    configSettings.selfRandomizeMinibosses = bool(minibossChoice and minibossChoice[0] == 1)
    configur.set('Boss', 'MinibossesSelf', str(configSettings.selfRandomizeMinibosses).lower())
    configSettings.mixedRandomizeMinibosses = bool(minibossChoice and minibossChoice[0] == 2)
    configur.set('Boss', 'MinibossesMixed', str(configSettings.mixedRandomizeMinibosses).lower()) 

    configSettings.randomizeBossResistances = bossResistFlags[0]
    configur.set('Resistances', 'RandomBossResists', str(bossResistFlags[0]).lower())
    configSettings.scaleResistToCheck = bossResistFlags[1]
    configur.set('Resistances', 'ScaleResistToCheck', str(bossResistFlags[1]).lower()) 
    configSettings.consistentWeakCount = bossResistFlags[2]
    configur.set('Resistances', 'ConsistenBossWeakCount', str(bossResistFlags[2]).lower()) 
    configSettings.playerResistSync = bossResistFlags[3]
    configur.set('Resistances', 'PlayerResistSync', str(bossResistFlags[3]).lower()) 
    configSettings.diverseBossResists = bossResistFlags[4]
    configur.set('Resistances', 'DiverseBossResist', str(bossResistFlags[4]).lower())  
        
    configSettings.ishtarPressTurns = ishtarChoice
    configur.set('Boss', 'IshtarPressTurns', str(ishtarChoice))
    configSettings.randomizeIshtarPressTurns = ishtarRandomizeChoice
    configur.set('Boss', 'RandomizeIshtarPressTurns', str(ishtarRandomizeChoice).lower())
    configSettings.bossPressTurnChance = bossTurnChoice
    configur.set('Boss', 'BossPressTurnChance', str(bossTurnChoice))

    configSettings.randomizeBossSkills = bossSkillFlags[0]
    configur.set('Boss', 'RandomizeBossSkills', str(bossSkillFlags[0]).lower())
    configSettings.similiarBossSkillRank = bossSkillFlags[1]
    configur.set('Boss', 'similiarBossSkillRank', str(bossSkillFlags[1]).lower())
    configSettings.allowBossMagatsuhiSkill = bossSkillFlags[2]
    configur.set('Boss', 'allowBossMagatsuhiSkill', str(bossSkillFlags[2]).lower())
    configSettings.allowContemptOfGod = bossSkillFlags[3]
    configur.set('Boss', 'allowContemptOfGod', str(bossSkillFlags[3]).lower())
    configSettings.elementCountConsistency = bossSkillFlags[4]
    configur.set('Boss', 'elementCountConsistency', str(bossSkillFlags[4]).lower())
    configSettings.addImpalersRevenge = bossSkillFlags[5]
    configur.set('Boss', 'addImpalersRevenge', str(bossSkillFlags[5]).lower())

    configSettings.fillEmptySlotsWithPassives = bool(passiveChoice and passiveChoice[0] == 1)
    configur.set('Boss', 'fillEmptySlotsWithPassives', str(configSettings.fillEmptySlotsWithPassives).lower())
    configSettings.scalePassiveAmount = bool(passiveChoice and passiveChoice[0] == 2)
    configur.set('Boss', 'scalePassiveAmount', str(configSettings.scalePassiveAmount).lower())
    configSettings.scalePassiveLevelGap = bool(passiveChoice and passiveChoice[0] == 3)
    configur.set('Boss', 'scalePassiveLevelGap', str(configSettings.scalePassiveLevelGap).lower())
    
    configSettings.alwaysCritical = bool(magatsuhiHarvestChoice and magatsuhiHarvestChoice[0] == 1)
    configur.set('Boss', 'alwaysCritical', str(configSettings.alwaysCritical).lower())
    configSettings.alwaysPierce = bool(magatsuhiHarvestChoice and magatsuhiHarvestChoice[0] == 2)
    configur.set('Boss', 'alwaysPierce', str(configSettings.alwaysPierce).lower())
    configSettings.randomMagatsuhi = bool(magatsuhiHarvestChoice and magatsuhiHarvestChoice[0] == 3)
    configur.set('Boss', 'randomMagatsuhi', str(configSettings.randomMagatsuhi).lower())

    configSettings.randomMiracleUnlocks = miracleFlags[0]
    configur.set('Miracle', 'RandomMiracleUnlocks', str(miracleFlags[0]).lower())
    configSettings.randomMiracleCosts = miracleFlags[1]
    configur.set('Miracle', 'RandomMiracleCosts', str(miracleFlags[1]).lower())
    configSettings.reverseDivineGarrisons = miracleFlags[2]
    configur.set('Miracle', 'ReverseDivineGarrisons', str(miracleFlags[2]).lower())

    configSettings.vanillaRankViolation = bool(rankViolationChoice and rankViolationChoice[0] == 1)
    configur.set('Miracle', 'VanillaRankViolation', str(configSettings.vanillaRankViolation).lower())
        
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


    configSettings.fixUniqueSkillAnimations = patchFlags[0]
    configur.set('Patches', 'FixUniqueSkillAnimations', str(patchFlags[0]).lower()) 
    configSettings.buffGuestYuzuru = patchFlags[1]
    configur.set('Patches', 'BuffGuestYuzuru', str(patchFlags[1]).lower())
    configSettings.unlockFusions = patchFlags[2]
    configur.set('Patches', 'UnlockFusions', str(patchFlags[2]).lower())
    configSettings.removeCutscenes = patchFlags[3]
    configur.set('Patches', 'SkipCutscenes', str(patchFlags[3]).lower())
    configSettings.skipTutorials = patchFlags[4]
    configur.set('Patches', 'SkipTutorials', str(patchFlags[4]).lower())
        
    configSettings.expMultiplier = expChoice
    configur.set('Patches', 'EXPMultiplier', str(expChoice))

    configSettings.pressTurnChance = pressTurnChoice
    configur.set('Patches', 'PressTurnChance', str(pressTurnChoice))

    configur.set('Seed','lastSeed', textSeed)

    with open('config.ini', 'w') as configfile:
        configur.write(configfile)

    return (configSettings, textSeed)

#Initializes the config.ini file with default values if it is missing or there's a version difference
def createConfigFile(configur):
    configur.read('config.ini')
    configur['Seed'] = {'lastSeed': ""}
    configur['Demon'] = {'RandomLevels': False, 'RandomSkills': False, 'ScaledSkills': False, 'RandomInnates': False, 'WeightSkillsToPotentials': False,
                                 'RandomPotentials': False, 'ScaledPotentials': False, 'multipleUniques': False, 'randomRaces': False, 'randomAlignment': False,
                                'ensureDemonJoinLevel':False, 'RandomDemonStats': False, 'ReduceCompendiumCost': False, 'RestrictLunationFlux': False, 
                                'EnemyOnlySkills':False, 'MagatsuhiSkills': False, 'ForceUniqueSkills': False, 'BetterSpecialFusions': False, 'WeightSkillsToLevels': False,
                                'LimitSkillMPCost': False, 'swapGuestsWithDemons': False,'swapDemifiend': False}
    configur['Item'] = {'RandomShopItems': False, 'RandomShopEssences': False,
                        'ScaleMaccaPerArea': False, 'ScaleItemsPerArea': False, 'ShuffleExistingItems': False, 'TrulyRandomizeItems': False,
                        'IncludeTsukuyomiTalismanAsGift': False,'IncludeEmpyreanKeysAsGifts': False, 'RandomizeMitamaDrops': False, "LifestoneOrChakraDrop":False,
                        'relicBiasVendingMachine': False, 'SelfItems': [], 'SharedItems': [],
                        'RedoableGospel': False,'RedoableGrimoire': False, 'RedoableWhittledGoat': False, 'RedoableEssences': False,
                        'RedoableIncensesBalmsSutras': False,
                        }
    configur['Inheritance'] = {'RandomInheritance': False, 'FreeInheritance': False}
    configur['Magatsuhi'] = {'RandomRequirements': False,'IncludeCritical': False,'IncludeSuccession': False}
    configur['Music'] = {'CheckBasedMusic': False, 'RandomMusic': False}
    configur['Boss'] = {'NormalBossesSelf': False, 'NormalBossesMixed': False, 'RandomizeLucifer': False, 'AbscessBossesSelf': False, 'AbscessBossesMixed': False,
                                 'OverworldBossesSelf': False, 'OverworldBossesMixed': False, 'SuperbossesSelf': False, 'SuperbossesMixed': False,
                                 'MinibossesSelf': False, 'MinibossesMixed': False, 'ScaleBossDamage': False, 'ScalePressTurns': False, 'IshtarPressTurns': 3,
                                 'RandomizeIshtarPressTurns': False, 'PreventEarlyAmbush': False, 'BossDependentAmbush': False, 'NerfBossHealing': False,
                                 'ScaleInstakillRates': False, 'bossNoEarlyPhysImmunity': False, 'BossPressTurnChance': 0.0, 'RandomizeBossSkills': False,
                                 'alwaysCritical': False,'alwaysPierce': False,'randomMagatsuhi': False,'similiarBossSkillRank':False,'allowBossMagatsuhiSkill':False,
                                 'allowContemptOfGod':False, 'elementCountConsistency': False, 'fillEmptySlotsWithPassives':False, 'addImpalersRevenge': False,
                                 'scalePassiveAmount': False, 'scalePassiveLevelGap': False}
    configur['Patches'] = {'FixUniqueSkillAnimations': False, 'BuffGuestYuzuru': False, 'EXPMultiplier': 1, 'PressTurnChance': 0.0, 'UnlockFusions': False, 'swapCutsceneModels': False,
                           'SkipCutscenes': False, 'SkipTutorials': False}
    configur['Miracle'] = {'RandomMiracleUnlocks': False, 'RandomMiracleCosts': False, 'ReverseDivineGarrisons': False, 'VanillaRankViolation': False, 'EarlyForestall': False,
                        'EarlyEmpoweringCheer': False, 'EarlyDivineAmalgamation': False, 'EarlyDivineGarrison': False, 'EarlyDemonProficiency': False,
                        'EarlyDivineProficiency': False, 'EarlyArtOfEssences': False, 'EarlyRankViolation': False, 'EarlyInheritenceViolation': False}
    configur['Resistances'] = {'RandomResists': False, 'AlwaysOneWeak': False,'ScaleElementalResist': False,'ScalePhysResist': False,'WeightResistByPotentials': False,
                             'DiverseResists': False, 'RandomBossResists': False, 'ConsistenBossWeakCount': False, 'ScaleResistToCheck':False, 'PlayerResistSync': False, 'DiverseBossResist': False}
    configur['Voice'] = {'RandomVoicesNormal': False, 'RandomVoicesChaos': False}
    configur['Navigators'] = {'RandomNavigatorStats': False, 'NavigatorModelSwap': False}