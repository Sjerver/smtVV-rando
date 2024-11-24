This is a randomizer for the Steam version of Shin Megami Tensei V Vengeance.

Installation Requirements:
- [.NET 8.0](https://dotnet.microsoft.com/en-us/download) is necessary to run the randomizer. Earlier versions of .NET are not compatible.

This randomizer randomizes the following things:
- Demons
- Encounters
- Bosses
- Items
- Miracles

You can choose a mix of any or all of these randomizations in the settings

Demon/Encounter randomization:
- Encounters get replaced with a demon at the same level as the original encounter
- For all playable demons and normal map encounters: Level (including EXP and Money adjustment), Press Turns (10%, doubled if normally two turns)
- Starting and learnable skills for demons can be randomized
- Skill distribution can be tied to their level and is based on the skill distribution of the main game, including Nahobino only and some Enemy only Skills.
  Skills are also weighted by how often they appear in the main game, and whether the demon has more strength or magic.
  Additonally some skills like Charge, Concentrate or Pleromas are only assigned to a demon if the demon would get use out of them or based on their potential it reasonable to assume that the demon could make good use of them.
- Skills can be distributed based on the demon's skill potentials
- Innate skills are randomized and guaranteed to avoid innates that have no effect
- You can randomize potentials and scale them based on the demon's level
- Races and alignments can be randomized
- Normal bosses, superbosses, abscesses, and punishing foes can be randomized within their own categories or mixed together
- Special fusions are randomized and will require demons of a lower level than the result
- Demons obtained from quests can be their randomized replacements at the same level as the original demon
- Stats of demons can be randomized

Unique Skill Inheritance:
- Vanilla: Unique skills can only show up on the skill's original owner
- Random: Unique skills get randomly assigned to a new owner, and therefore cannot be inherited to their original owner
- Free: Unique skills can be freely inherited and learned by any demon

Item/Miracle randomization:
- Shop Items are randomized, but dampeners are guaranteed to show up immediately
- Chest Items, enemy/boss drops, quest rewards, and miman rewards can be randomized
- Key Items required for quest progression will always be in obtainable in the same way
- The randomizer will try to provide one of each essence before giving any duplicates
- Miracle unlocks and glory costs can be randomized
- Progressive miracles like art of essences will be given to abscesses in order
- Some important miracles like divine amalgamation will be guaranteed at the start

Basic gameplay changes:
- All demons who are normally not recruitable as basic enemies have their tone changed, to make them recruitable resulting in the loss of unique level-up lines and similiar text
- Normally two demons which result in a special fusion do not result in a normal fusion. For the sake of simplicity they now are fusable normally.
  (Example: Barong and Rangda can not be fused normally because they are the requirement for special fusion Shiva. The randomizer adds a normal fusion of Barong + Rangda = Chimera according to normal fusion chart rules.)
- For some unique skills the animations might not play properly but the game should continue if the animation is skipped
- In the vengeance route, Yuzuru will be level 99 for the Glasya-Labolas check to avoid getting hard-walled
- In order to allow for more flexible assignment of random races and level, additional fusion combinations for previously unfusable races have been added to the fusion chart.

For detailed explanations of settings and gameplay changes, you can refer to the [wiki](https://github.com/Sjerver/smtVV-rando/wiki)

To run the randomizer, windows users can download a release and run randomizer.exe
Otherwise you can run the randomizer from source if you have python installed on your computer.
Download the GitHub repository and then run the following command in the main directory:

python randomizer.py

The folder "Rando" then features the result. Using UnrealPak you can then create a .pak file with this folder.
If on windows, the randomizer will automatically create rando.pak so you can skip this step
Then open the directory of the game via Steam and navigate to SMT5V/Project/Content/Paks.
Here create a folder named "~mods" and put the .pak file in it.
The mod should now work when loading the game.

Since the randomizer makes edits to a plethora of files it is incompatible with most mods. For a concrete list of files the randomizer modifies check the base folder.

One final note: using the 'Randomize Cutscene Models' setting is experimental and may cause the randomizer to take a long time to run (10-30+ minutes)

If you have any questions or technical difficulties, join the SMT Randomizer discord: https://discord.gg/d25ZAha
