PROTOFIEND_IDS = [1101,1102,1103,1104,1105,1106,1107,1108,1109,110,1111,1112,1113,1114,1115,1116,1117,1118]


BANNED_BOSSES = [0, 7, 33, 42, 48, 53, 89] #Dummy Abbadon, Tutorial Pixie, Hydra (game hangs when supposed to lose limbs), Normal Cleopatra, Normal Andras, Dummy Mandrake+Shiva, Dummy Demi-Fiend

BOSS_SUMMONS = {
    519: [517, 518],    #Khonsu Ra - Anubis and Thoth
    845: [871, 872, 873, 874, 875], #Shiva - Ganesha, Kali, Dakini, Ananta and Parvati
    934: [940, 941, 942, 943, 944, 945, 946], #Demi-Fiend - Cerberus, Jack Frost, Pixie, Thor, Girimekhala, Parvati, Cu Chulainn
    529: [531, 532, 533], #Lucifer True Ending - Brimstone Star, Cocytus Star, Morning Star
    537: [538, 539], #Lucifer Normal Endings - Brimstone Star, Cocytus Star
    839: [846, 847, 848, 849], #Huang Long - Qing Long, Zhuque, Baihu, Xuanwu
    760: [761, 762, 763, 764, 765, 766, 767], #Samael - Lilith's Shadow, Agrat's Shadow x2, Eisheth's Shadow x2, Naamah's Shadow x2
    569: [570, 571, 572, 573, 574, 575], #Lilith - Agrat x2, Eisheth x2, Naamah x2
    473: [474, 475] #Alilat - Flauros, Ose
}

def getMaccaValues ():
    return [0,10,13,15,16,17,18,20,21,23,24,26,28,29,31,33,34,36,38,40,41,44,46,49,51,55,58,61,65,68,71,74,78,82,87,90,94,98,103,107,111,116,121,126,131,137,142,147,153,159,164,170,177,184,190,198,204,212,218,225,233,241,249,257,264,273,281,290,298,307,315,356,374,415,456,542,629,758,887,1016,1145,1274,1403,1532,1661,1790,1919,2048,2177,2306,2435,2564,2693,2822,2951,3080,3209,3338,3467,3596]


def getExpValues():
    return [0,24,26,29,32,37,42,47,57,74,87,98,123,151,182,217,257,300,347,398,453,512,575,642,713,788,867,949,1035,1124,1216,1312,1427,1548,1675,1807,1946,2090,2241,2397,2559,2727,2901,3081,3267,3459,3657,3861,4071,4281,4500,4728,4856,4927,4997,5165,5334,5372,5410,5460,5509,5597,5672,5773,5821,5860,5933,6000,6058,6132,6172,6280,6326,6447,6568,6665,6762,6858,6954,7050,7146,7242,7338,7434,7530,7626,7722,7818,7914,8010,8106,8202,8298,8394,8490,8586,8682,8778,8874,8970]


def getBonusSkills():
    return [["Impaler's Revenge",510,90,90],['Intercalation',452,69,69],['Elusive Eclipse',451,52,52],['Rooted Soul',450,12,12],[ 'Moonlight Frost',255,83,83],[ 'Frenzy',283,15,15],[ 'Galvanic Slash',284,46,49],[ 'Sakanagi',292,25,25],[ 'Divine Arrowfall',293,41,41],[ 'Murakumo',294,67,67],[ 'Red Capote',295,24,24],[ 'Aramasa',298,8,8],[ 'Wrath Tempest',299,44,44],[ 'Ruinous Thunder',300,31,31],[ 'Thalassic Calamity',301,54,54],[ 'Kannabi Veil',306,36,36],[ 'Profaned Land',307,48,48],[ 'Miracle Water',310,17,17],[ 'Dreadful Gleam',312,52,52],[ 'Purgatorium',320,83,83],[ 'Impetus',321,83,83],[ 'Inferno of God',329,95,99],[ 'Hailstorm of God',330,95,99],[ 'Lightning of God',331,95,99],[ 'Tornado of God',332,95,99],[ 'Cold Dark Matter',333,90,99],[ 'Hot Dark Matter',334,95,99],[ 'Freikugel',335,95,99],[ 'Gaea Rage',336,95,99],[ 'Magma Axis',337,95,99],[ 'Javelin Rain',338,90,99],[ 'Xeros Beat',339,95,99],[ 'Deadly Fury',340,90,99],[ 'Wild Dance',341,95,99],[ 'Contempt of God',342,95,99],[ 'Freikugel',370,95,99],[ 'Javelin Rain',372,95,99],[ 'Deadly Fury',373,95,99],[ 'Evil Gleam',390,95,99],[ 'Sonic Boom',392,35,35],[ 'Gaea Rage',394,95,99],[ 'Chaotic Will',395,95,99],[ 'Javelin Rain',397,95,99],[ 'Deadly Fury',398,95,99],[ 'Abyssal Beckoning',861,84,84],[ 'Seething Mansemat',863,84,84],[ 'Untainted Wind',864,84,84],[ 'Boundless Sea',865,83,83],[ 'Bufu',902,8,8],[ 'Rakunda',903,8,8],[ 'Gram Slice',904,8,8],[ 'Charge',905,44,47],[ 'Bufula',906,44,47],[ 'Carnage Fang',908,44,47],[ "Sun's Radiance",909,44,47],[ 'Witness Me',910,44,47],[ 'Hama',911,8,8],[ 'Mahamaon',912,44,44],[ 'Mirage Shot',913,44,44],[ 'Zanma',914,44,44],[ 'Trafuri',915,44,44],[ 'Cautious Cheer',916,44,44],[ 'Toxic Cloud',917,44,44],[ 'Paraselene Blur',918,80,80],[ 'Evergreen Dance',921,51,51],[ 'Inflaming Divinity',922,28,28],[ 'Heavenly Ikuyumi',923,72,72],[ 'Moonlight Frost',924,52,52],[ 'Lunar Hurricane',925,69,69],[ 'Luminescent Mirage',926,80,80],[ 'Lunation Flux',927,69,69]]