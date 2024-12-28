import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from randomizer import Randomizer, readBinaryTable
import util.paths as paths
import util.numbers as numbers


def prepareRando(seed = None, settings = None):
    rando = Randomizer()
    if seed:
        rando.textSeed = seed
    if settings:
        rando.configSettings = settings

    rando.createSeed()
    buffers = {
        "compendiumBuffer": readBinaryTable(paths.NKM_BASE_TABLE_IN),
        "skillBuffer": readBinaryTable(paths.SKILL_DATA_IN),
        "normalFusionBuffer": readBinaryTable(paths.UNITE_COMBINE_TABLE_IN),
        "otherFusionBuffer": readBinaryTable(paths.UNITE_TABLE_IN),
        "encountBuffer": readBinaryTable(paths.ENCOUNT_DATA_IN),
        "playGrowBuffer": readBinaryTable(paths.MAIN_CHAR_DATA_IN),
        "itemBuffer": readBinaryTable(paths.ITEM_DATA_IN),
        "shopBuffer": readBinaryTable(paths.SHOP_DATA_IN),
        "eventEncountBuffer": readBinaryTable(paths.EVENT_ENCOUNT_IN),
        "missionBuffer": readBinaryTable(paths.MISSION_DATA_IN),
        "bossFlagBuffer": readBinaryTable(paths.BOSS_FLAG_DATA_IN),
        "battleEventsBuffer": readBinaryTable(paths.BATTLE_EVENTS_IN),
        "battleEventUassetBuffer": readBinaryTable(paths.BATTLE_EVENT_UASSET_IN),
        "devilAssetTableBuffer": readBinaryTable(paths.DEVIL_ASSET_TABLE_IN),
        "abscessBuffer": readBinaryTable(paths.ABSCESS_TABLE_IN),
        "devilUIBuffer": readBinaryTable(paths.DEVIL_UI_IN),
        "talkCameraBuffer": readBinaryTable(paths.TALK_CAMERA_OFFSETS_IN),
        "eventEncountPostBuffer": readBinaryTable(paths.EVENT_ENCOUNT_POST_DATA_TABLE_IN),
        "miracleBuffer": readBinaryTable(paths.MIRACLE_TABLE_IN),
        "eventEncountUassetBuffer": readBinaryTable(paths.EVENT_ENCOUNT_UASSET_IN),
        "uniqueSymbolBuffer": readBinaryTable(paths.UNIQUE_SYMBOL_DATA_IN),
        "encountPostBuffer": readBinaryTable(paths.ENCOUNT_POST_DATA_TABLE_IN),
        "encountPostUassetBuffer": readBinaryTable(paths.ENCOUNT_POST_DATA_TABLE_UASSET_IN),
        "chestBuffer": readBinaryTable(paths.CHEST_TABLE_IN),
        "mapSymbolParamBuffer": readBinaryTable(paths.MAP_SYMBOL_PARAM_IN),
        "eventEncountPostUassetBuffer": readBinaryTable(paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_IN),
        "mapEventBuffer": readBinaryTable(paths.MAP_EVENT_DATA_IN),
    }
    rando.readDemonNames()
    rando.readSkillNames()
    rando.readItemNames()
    rando.readDataminedEnemyNames()
    rando.fillCompendiumArr(buffers["compendiumBuffer"])
    rando.fillSkillArrs(buffers["skillBuffer"])
    rando.fillNormalFusionArr(buffers["normalFusionBuffer"])
    rando.fillFusionChart(buffers["otherFusionBuffer"])
    rando.fillSpecialFusionArr(buffers["otherFusionBuffer"])
    rando.fillBasicEnemyArr(buffers["compendiumBuffer"])
    rando.fillEncountArr(buffers["encountBuffer"])
    rando.fillEncountSymbolArr(buffers["encountBuffer"])
    rando.fillEventEncountArr(buffers["eventEncountBuffer"])
    rando.fillBattleEventArr(buffers["battleEventsBuffer"])
    rando.fillDevilAssetArr(buffers["devilAssetTableBuffer"])
    rando.fillAbscessArr(buffers["abscessBuffer"])
    rando.fillDevilUIArr(buffers["devilUIBuffer"])
    rando.fillTalkCameraArr(buffers["talkCameraBuffer"])
    rando.fillMiracleArr(buffers["miracleBuffer"])

    # Requires asset arr, eventEncounter and needs to be before bossArr
    rando.createOverlapCopies(buffers["compendiumBuffer"])
    buffers["compendiumBuffer"] = rando.writeOverlapCopiesToBuffer(rando.overlapCopies, buffers["compendiumBuffer"])

    rando.fillBossArr(buffers["compendiumBuffer"])
    rando.fillPlayerBossArr(buffers["compendiumBuffer"])
    rando.fillBossFlagArr(buffers["bossFlagBuffer"])
    rando.fillNahobino(buffers["playGrowBuffer"])
    rando.fillEssenceArr(buffers["itemBuffer"])
    rando.fillShopArr(buffers["shopBuffer"])
    rando.fillProtofiendArr(buffers["compendiumBuffer"])
    rando.fillMissionArr(buffers["missionBuffer"])
    rando.fillUniqueSymbolArr(buffers["uniqueSymbolBuffer"])
    rando.fillChestArr(buffers["chestBuffer"])
    rando.fillMimanRewardArr(buffers["shopBuffer"])
    rando.fillMapSymbolArr(buffers["mapSymbolParamBuffer"])
    rando.fillConsumableArr(buffers["itemBuffer"])
    rando.fillFusionSkillReqs(buffers["skillBuffer"])
    rando.fillMapEventArr(buffers["mapEventBuffer"])

    rando.findValidBossDemons()

    # rando.fullRando(rando.configSettings,True)
    return rando,buffers

#TODO: Write tests for functions of the randomizer here eventually
    
