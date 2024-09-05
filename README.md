This is a randomizer for the Steam version of Shin Megami Tensei V Vengeance.

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
- All compendium demons and basic enemies get random skills that would be appropriate for their level
  Appropriateness for their level is based on the skill distribution of the main game, including Nahobino only and some Enemy only Skills.
  Skills are also weighted by how often they appear in the main game, the corresponding potential for the skill from the demon, and whether the demon has more strength or magic.
  Additonally some skills like Charge, Concentrate or Pleromas are only assigned to a demon if the demon would get use out of them or based on their potential it reasonable to assume that the demon could make good use of them.
- Innate skills are randomized and guaranteed to avoid innates that have no effect
- You can randomize potentials and scale them based on the demon's level
- Races and alignments can be randomized
- Normal bosses, superbosses, abscesses, and punishing foes can be randomized within their own categories or mixed together
- Special fusions are randomized and will require demons of a lower level than the result

Item/Miracle randomization:
- Shop Items are randomized, but dampeners are guaranteed to show up immediately
- Chest Items, enemy/boss drops, quest rewards, and miman rewards can be randomized
- The randomizer will try to provide one of each essence before giving any duplicates
- Miracle unlocks and glory costs can be randomized
- Progressive miracles like art of essences will be given to abscesses in order
- Some important miracles like divine amalgamation will be guaranteed at the start

Basic gameplay changes:
- All demons who are normally not recruitable as basic enemies have their tone changed, to make them recruitable resulting in the loss of unique level-up lines and similiar text
- Normally two demons which result in a special fusion do not result in a normal fusion. For the sake of simplicity they now are fusable normally.
  (Example: Barong and Rangda can not be fused normally because they are the requirement for special fusion Shiva. The randomizer adds a normal fusion of Barong + Rangda = Chimera according to normal fusion chart rules.)
- For some unique skills the animations might not play properly but the game should continue if the animation is skipped
- Demons obtained from quests will be their randomized replacements at the same level as the original demon
- In the vengeance route, Yuzuru will be level 99 for the Glasya-Labolas check to avoid getting hard-walled

These things are planned for future updates:
- Randomizing Magatsuhi
- Removing unlock conditions for fusing demons
- Updating more text to reflect randomized bosses/demons
- Randomizing NPC models
- Improvements to overworld encounters for demons who are not normally in the overworld

To run the randomizer, windows users can download a release and run randomizer.exe
Otherwise you can run the randomizer from source if you have python installed on your computer.
Download the GitHub repository and then run the following command in the main directory:

python randomizer.py

The folder "Rando" then features the result. Using UnrealPak you can then create a .pak file with this folder.
If on windows, the randomizer will automatically create rando.pak so you can skip this step
Then open the directory of the game via Steam and navigate to SMT5V/Project/Content/Paks.
Here create a folder named "~mods" and put the .pak file in it.
The mod should now work when loading the game.
