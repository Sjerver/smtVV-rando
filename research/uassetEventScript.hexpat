struct NameEntry{
    s32 size;
    
    if (size < 0) {
        u32 reverseSize = size * -1;
        char16 string[reverseSize];
    }
    else if (size > 0) {
        char string[size];
    }
    
    u32 hashes;
};



u32 nameMapSize @ 0x29;

NameEntry *names[nameMapSize] : u32 @ 0x2D;

struct FName{
    u32 nameMapPointer;
    u32 unknownNumber;
};

struct importEntry{
    FName classPackage;
    FName className;
    s32 outerIndex;
    FName objectName;
};

u32 importMapSize @ 0x41;

importEntry *importData[importMapSize] : u32 @ 0x45;


struct exportEntry{
    s32 classIndex;
    s32 superIndex;
    s32 templateIndex;
    s32 outerIndex;
    FName objectName;
    u32 objectFlags;
    s64 serialSize; 
    s64 serialOffset;
    
    u32 bForcedExport;
    u32 bNotForClient;
    u32 bNotForServer;
    u128 packageGuid;
    u32 isInheritedInstance;
     
    u32 packageFlags;
    u32 bNotAlwaysLoadedForEditorGame;
    u32 bIsAsset;
    //u32 generatePublicHash;
    //s32 firstExportDependcyOffset;
    //s32 sbsds;
    //s32 cBSDS;
    //s32 sBCDS;
    //s32 cBCDS;
    s64 scriptSerializationStartOffset;
    s64 scriptSerializationEndOffset;
    
    
    
};

u32 exportMapSize @ 0x39;

exportEntry *exportMap[exportMapSize] : u32 @ 0x3D;



struct dependsMap{
    s32 size;
    s32 dependsIndeces[size];
};

dependsMap *dependsData[exportMapSize] : u32 @ 0x49;

u32 softPackageCount @ 77;
u32 softPackageOffset  @ 81;
u32 searchNameOffset @ 85;
u32 thumbnailTableOffset @ 89;

s128 packageGuid @93;

s32 generationCount @ 0x6D;

struct generation{
    s32 genNumExports;
    s32 genNumNames;
};

generation generations[generationCount] @ 0x71;


struct engineVersion {
    u16 major;
    u16 minor;
    u16 patch;
    u32 changelist;
    s32 fstring;
};

engineVersion engineVer @ (0x71 + generationCount * 8);
engineVersion compatibleEngineVer @ (0x7F + generationCount * 8);

u32 compressionFlags  @ (0x8D + generationCount * 8); 
s32 numCompressedChunks @ (0x91 + generationCount * 8);
 
u32 packageSource @ (0x95 + generationCount * 8);
s32 additionalPackages @ (0x99 + generationCount * 8); 
  
s64 bulkDataStart @ (0xA1 + generationCount * 8);
     
s32 worldTileInfoDataOffset @  (0xA9 + generationCount * 8);
  
struct assetRegistryData{
    s32 test;
  
};
  
assetRegistryData *assetRegistryOffset: s32 @ (0x9D + generationCount * 8);


s32 chunkCount @ (0xAD + generationCount * 8);

s32 chunks[chunkCount] @ (0xB1 + generationCount * 8);

s32 PreloadDependencyCount @ (0xB1 + generationCount * 8 + chunkCount * 4);
s32 PreloadDependencyOffset @(0xB5 + generationCount * 8 + chunkCount * 4);