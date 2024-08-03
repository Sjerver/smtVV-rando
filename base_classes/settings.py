class Settings(object):
    def __init__(self):
        self.randomDemonLevels = False              # Randomize demon levels (enables encounter randomizer)
        self.randomSkills = False                   # Randomize demon starting and learned skills
        self.scaledSkills = False                   # Ensure demons have appropriately strong skills for their level
        self.randomInnates = False                  # Randomize demon innate skills
        self.potentialWeightedSkills = False        # Weight demon skills based on their skill potentials and stats
        self.randomPotentials = False               # Randomize demon skill potentials
        self.scaledPotentials = False               # Scale demon potentials based on level
        self.multipleUniques = False                # Allows unique skills to be assigned to more than one demon
        self.randomMusic = False                    # Boss music is randomized
        self.checkBasedMusic = False                # Boss music is based on check rather than boss demon
        self.randomShopItems = False                # Randomizes what items are sold in the shop
        self.randomShopEssences = False             # Randomizes what essences are sold in the shop
        self.randomEnemyDrops = False               # Randomizes items that enemies drop
        self.selfRandomizeNormalBosses = False      # Randomize story and sidequest bosses only with each other
        self.mixedRandomizeNormalBosses = False     # Randomize story and sidequest bosses with all bosses
        self.selfRandomizeAbscessBosses = False     # Randomize abscess bosses only with each other
        self.mixedRandomizeAbscessBosses = False    # Randomize abscess bosses with all bosses
        self.selfRandomizeOverworldBosses = False   # Randomize punishing foes only with each other
        self.mixedRandomizeOverworldBosses = False  # Randomize punishing foes with all bosses
        self.selfRandomizeSuperbosses = False       # Randomize superbosses only with each other
        self.mixedRandomizeSuperbosses = False      # Randomize superbosses foes with all bosses
        self.randomInheritance = False              # Randomize to which demons unique skills belong to
        self.freeInheritance = False                # Make unique skills freely inheritable