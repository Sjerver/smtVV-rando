import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from randomizer import Randomizer
from gui import ConfigParser
from base_classes.settings import Settings 
from util import paths
from collections import defaultdict

def runRando(seed, settings):
    rando = Randomizer()
    rando.textSeed = seed
    rando.configSettings = settings

    rando.createSeed()

    rando.fullRando(rando.configSettings,True)

def setConfigSettings(configur):
    configSettings = Settings()
    configSettings.swapCutsceneModels = obtainBooleanValue(configur.get('Patches', 'swapCutsceneModels'))
    configSettings.randomDemonLevels = obtainBooleanValue(configur.get('Demon', 'RandomLevels'))
    configSettings.randomSkills = obtainBooleanValue(configur.get('Demon', 'RandomSkills'))
    configSettings.scaledSkills = obtainBooleanValue(configur.get('Demon', 'ScaledSkills'))
    configSettings.randomInnates = obtainBooleanValue(configur.get('Demon', 'RandomInnates'))
    configSettings.potentialWeightedSkills = obtainBooleanValue(configur.get('Demon', 'WeightSkillsToPotentials'))
    configSettings.randomPotentials = obtainBooleanValue(configur.get('Demon', 'RandomPotentials'))
    configSettings.scaledPotentials = obtainBooleanValue(configur.get('Demon', 'ScaledPotentials'))
    configSettings.multipleUniques = obtainBooleanValue(configur.get('Demon', 'multipleUniques'))
    configSettings.randomRaces = obtainBooleanValue(configur.get('Demon', 'randomRaces'))
    configSettings.randomAlignment = obtainBooleanValue(configur.get('Demon', 'randomAlignment'))
    configSettings.ensureDemonJoinLevel = obtainBooleanValue(configur.get('Demon', 'ensureDemonJoinLevel'))
    configSettings.randomDemonStats = obtainBooleanValue(configur.get('Demon', 'RandomDemonStats'))
    configSettings.reduceCompendiumCosts = obtainBooleanValue(configur.get('Demon', 'ReduceCompendiumCost'))
    configSettings.restrictLunationFlux = obtainBooleanValue(configur.get('Demon', 'RestrictLunationFlux'))
    configSettings.includeEnemyOnlySkills = obtainBooleanValue(configur.get('Demon', 'EnemyOnlySkills'))
    configSettings.includeMagatsuhiSkills = obtainBooleanValue(configur.get('Demon', 'MagatsuhiSkills'))
    configSettings.forceAllSkills = obtainBooleanValue(configur.get('Demon', 'ForceUniqueSkills'))

    configSettings.randomInheritance = obtainBooleanValue(configur.get('Inheritance', 'RandomInheritance'))
    configSettings.freeInheritance = obtainBooleanValue(configur.get('Inheritance', 'FreeInheritance'))

    configSettings.randomizeMagatsuhiSkillReq = obtainBooleanValue(configur.get('Magatsuhi', 'RandomRequirements'))
    configSettings.includeOmagatokiCritical = obtainBooleanValue(configur.get('Magatsuhi', 'IncludeCritical'))
    configSettings.includeOmnipotentSuccession = obtainBooleanValue(configur.get('Magatsuhi', 'IncludeSuccession'))

    configSettings.randomMusic = obtainBooleanValue(configur.get('Music', 'RandomMusic'))
    configSettings.checkBasedMusic = obtainBooleanValue(configur.get('Music', 'CheckBasedMusic'))

    configSettings.randomShopItems = obtainBooleanValue(configur.get('Item', 'RandomShopItems'))
    configSettings.randomShopEssences = obtainBooleanValue(configur.get('Item', 'RandomShopEssences'))
    configSettings.randomEnemyDrops = obtainBooleanValue(configur.get('Item', 'RandomEnemyDrops'))
    configSettings.randomChests = obtainBooleanValue(configur.get('Item', 'RandomChests'))
    configSettings.scaleItemsToArea = obtainBooleanValue(configur.get('Item', 'ScaleItemsToArea'))
    configSettings.randomizeMimanRewards = obtainBooleanValue(configur.get('Item', 'RandomizeMimanRewards'))
    configSettings.randomizeMissionRewards = obtainBooleanValue(configur.get('Item', 'RandomizeMissionRewards'))
    configSettings.randomizeGiftItems = obtainBooleanValue(configur.get('Item', 'RandomizeGiftItems'))
    configSettings.combineKeyItemPools = obtainBooleanValue(configur.get('Item', 'CombineKeyItemPools'))
    configSettings.includeTsukuyomiTalisman = obtainBooleanValue(configur.get('Item', 'IncludeTsukuyomiTalisman'))

    configSettings.scaleBossDamage = obtainBooleanValue(configur.get('Boss', 'ScaleBossDamage'))
    configSettings.scaleBossPressTurnsToCheck = obtainBooleanValue(configur.get('Boss', 'ScalePressTurns'))
    configSettings.randomizeLucifer = obtainBooleanValue(configur.get('Boss', 'RandomizeLucifer'))
    configSettings.preventEarlyAmbush = obtainBooleanValue(configur.get('Boss', 'PreventEarlyAmbush'))
    configSettings.bossDependentAmbush = obtainBooleanValue(configur.get('Boss', 'BossDependentAmbush'))
    configSettings.nerfBossHealing = obtainBooleanValue(configur.get('Boss', 'NerfBossHealing'))
    configSettings.scaleBossInstakillRates = obtainBooleanValue(configur.get('Boss', 'ScaleInstakillRates'))

    configSettings.selfRandomizeNormalBosses = obtainBooleanValue(configur.get('Boss', 'NormalBossesSelf'))
    configSettings.mixedRandomizeNormalBosses = obtainBooleanValue(configur.get('Boss', 'NormalBossesMixed'))
    configSettings.selfRandomizeAbscessBosses = obtainBooleanValue(configur.get('Boss', 'AbscessBossesSelf'))
    configSettings.mixedRandomizeAbscessBosses = obtainBooleanValue(configur.get('Boss', 'AbscessBossesMixed'))
    configSettings.selfRandomizeOverworldBosses = obtainBooleanValue(configur.get('Boss', 'OverworldBossesSelf'))
    configSettings.mixedRandomizeOverworldBosses = obtainBooleanValue(configur.get('Boss', 'OverworldBossesMixed'))
    configSettings.selfRandomizeSuperbosses = obtainBooleanValue(configur.get('Boss', 'SuperbossesSelf'))
    configSettings.mixedRandomizeSuperbosses = obtainBooleanValue(configur.get('Boss', 'SuperbossesMixed'))
    configSettings.selfRandomizeMinibosses = obtainBooleanValue(configur.get('Boss', 'MinibossesSelf'))
    configSettings.mixedRandomizeMinibosses = obtainBooleanValue(configur.get('Boss', 'MinibossesMixed'))

    configSettings.ishtarPressTurns = int(configur.get('Boss', 'IshtarPressTurns'))
    configSettings.randomizeIshtarPressTurns = obtainBooleanValue(configur.get('Boss', 'RandomizeIshtarPressTurns'))

    configSettings.randomMiracleUnlocks = obtainBooleanValue(configur.get('Miracle', 'RandomMiracleUnlocks'))
    configSettings.randomMiracleCosts = obtainBooleanValue(configur.get('Miracle', 'RandomMiracleCosts'))
    configSettings.reverseDivineGarrisons = obtainBooleanValue(configur.get('Miracle', 'ReverseDivineGarrisons'))

    configSettings.vanillaRankViolation = obtainBooleanValue(configur.get('Miracle', 'VanillaRankViolation'))

    configSettings.forcedEarlyMiracles.append(31 if obtainBooleanValue(configur.get('Miracle', 'EarlyRankViolation')) else None)
    configSettings.forcedEarlyMiracles.append(55 if obtainBooleanValue(configur.get('Miracle', 'EarlyDivineGarrison')) else None)
    configSettings.forcedEarlyMiracles.append(13 if obtainBooleanValue(configur.get('Miracle', 'EarlyForestall')) else None)
    configSettings.forcedEarlyMiracles.append(49 if obtainBooleanValue(configur.get('Miracle', 'EarlyEmpoweringCheer')) else None)
    configSettings.forcedEarlyMiracles.append(32 if obtainBooleanValue(configur.get('Miracle', 'EarlyArtOfEssences')) else None)
    configSettings.forcedEarlyMiracles.append(51 if obtainBooleanValue(configur.get('Miracle', 'EarlyDemonProficiency')) else None)
    configSettings.forcedEarlyMiracles.append(61 if obtainBooleanValue(configur.get('Miracle', 'EarlyDivineProficiency')) else None)
    configSettings.forcedEarlyMiracles.append(117 if obtainBooleanValue(configur.get('Miracle', 'EarlyDivineAmalgamation')) else None)
    configSettings.forcedEarlyMiracles.append(30 if obtainBooleanValue(configur.get('Miracle', 'EarlyInheritenceViolation')) else None)
    configSettings.forcedEarlyMiracles = [miracle for miracle in configSettings.forcedEarlyMiracles if miracle is not None]

    configSettings.fixUniqueSkillAnimations = obtainBooleanValue(configur.get('Patches', 'FixUniqueSkillAnimations'))
    configSettings.buffGuestYuzuru = obtainBooleanValue(configur.get('Patches', 'BuffGuestYuzuru'))
    configSettings.unlockFusions = obtainBooleanValue(configur.get('Patches', 'UnlockFusions'))

    configSettings.expMultiplier = float(configur.get('Patches', 'EXPMultiplier'))
    configSettings.pressTurnChance = float(configur.get('Patches', 'PressTurnChance'))
    return configSettings

def obtainBooleanValue(value):
    return str(value).lower() == 'true'

def test_presets():
    presetNames = ["Balanced", "Casual", "Challenge", "Speedrun", "Masochist","MAX CHAOS"]
    for preset in presetNames:
        presetTest(preset)

def presetTest(preset):
    print(preset)
    presetConfigur = ConfigParser()
    presetConfigur.read(paths.PRESET_SETTINGS_FOLDER + "/" +preset+ ".ini")
    presetSettings = setConfigSettings(presetConfigur)
    runRando("",presetSettings)
    assert True

def test_blank():
    rando = Randomizer()
    runRando("",rando.configSettings)
    assert True

def test_selfContainedBosses():
    rando = Randomizer()
    rando.configSettings.selfRandomizeNormalBosses = True
    rando.configSettings.selfRandomizeAbscessBosses = True
    rando.configSettings.selfRandomizeOverworldBosses = True
    rando.configSettings.selfRandomizeSuperbosses = True
    rando.configSettings.selfRandomizeMinibosses = True
    runRando("",rando.configSettings)
    assert True


def determineUntestedBooleanSettings():
    presetNames = ["Balanced", "Casual", "Challenge", "Speedrun", "Masochist","MAX CHAOS"]
    presets = []
    for name in presetNames:
        presetConfigur = ConfigParser()
        presetConfigur.read(paths.PRESET_SETTINGS_FOLDER + "/" +name+ ".ini")
        presets.append(presetConfigur)
    # Initialize a dictionary to track True/False occurrences for each setting
    setting_values = defaultdict(set)

    # Iterate over each preset
    for configur in presets:
        # Create a Settings object for the preset
        configSettings = setConfigSettings(configur)
        
        # Inspect and track each setting
        for attr in vars(configSettings):
            value = getattr(configSettings, attr)
            if type(value) == bool:
                setting_values[attr].add(value)

    blank = Settings()
    for attr in vars(blank):
        value = getattr(blank, attr)
        if type(value) == bool:
            setting_values[attr].add(value)

    # Find settings without both True and False values
    non_variating_settings = {
        setting for setting, values in setting_values.items() if not (True in values and False in values)
    }

    print(non_variating_settings)

if __name__ == "__main__":  
    determineUntestedBooleanSettings()