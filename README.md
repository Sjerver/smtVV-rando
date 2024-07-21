This is a randomizer for the Steam version of Shin Megami Tensei V Vengeance.

This randomizer currently features no settings or GUI and therefore its features might change while no user input is possible.

Currently this randomizer randomizes the following things:
- Encounters get replaced with the demon at the same level
- All compendium demons and basic enemies get random skills that would be appropriate for their level
  Appropriateness for their level is based on the skill distribution of the main game, including Nahobino only and some Enemy only Skills.
  Skills are also weighted by how often they appear in the main game, the corresponding potential for the skill from the demon, and whether the demon has more strength or magic.
  Additonally some skills like Charge, Concentrate or Pleromas are only assigned to a demon if the demon would get use out of them or based on their potential it reasonable to assume that the demon could make good use of them.

Basic gameplay changes:
- All demons who are normally not recruitable as basic enemies have their tone changed, to make them recruitable resulting in the loss of unique level-up lines and similiar text
- Normally two demons which result in a special fusion do not result in a normal fusion. For the sake of simplicity they now are fusable normally.
  (Example: Barong and Rangda can not be fused normally because they are the requirement for special fusion Shiva. The randomizer adds a normal fusion of Barong + Rangda = Chimera according to normal fusion chart rules.)
- For some unique skills the animations might not play properly but the game should continue if the animation is skipped

These things are planned to be able to be randomized:
- Level, Race, Stats, Potentials, Innates of demons
- Special Fusions and demons which need to be unlocked for fusion
- Item Drops
- Shops
- Aogami Essences
- Magatsuhi Skills


To use the randomizer download the repo and execute the following command in the terminal after navigating to the folder.

node main.js

The folder "Rando" then features the result. Using UnrealPak you can then create pak file with this folder.
Then open the directory of the game via Steam and navigate to SMT5V/Project/Content/Paks.
Here create a folder named "~mods" and put the pak file in it.
The mod should now work when loading the game
