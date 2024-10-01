//Change values of Propertys at the bottom to the ids from the uassets name array to use

u32 fileSizeWithoutHeaderFooter @ 0x10;
u32 entryCount @ 0x21;
u32 structSize @ 0x35;

struct textValue{
        s32 valueSize;
        if (valueSize > 0) {
            char string[valueSize];
        }

};

struct pageDataStrElement{
    s64 name;
    s64 type;
    s64 variant;
    u8 dupIndex;
    textValue;
      
};

struct pageDataElement{
    s64 name;
    s64 type;
    s32 variant;
    u8 dupIndex;
    s32 value1;s32 value2;s32 value3; s32 unknown;s32;
   
};

struct iconElement{
    s32;s64;s64;s64;s64;s32;u8;
    s64;s64;s64;s64;s64;s64;u8;
    s64;
};

struct pageDataEntry{
    pageDataStrElement strElements[2];
    pageDataElement elements[2];
};

struct pageDataArray{
    s32 pageDataCount;
    s64 pageDataName;
    s64 structProp;
    s32 structLength;
    s32 unknown1;
    s64 scriptMessagePageData;
    s64 unknown2;s64 unknown3;u8;
    
    pageDataEntry pageDataEntries[pageDataCount];
    
};

struct page{
u8;u32;
        textValue;
        textValue;
        textValue;

};

struct entryType{
    s64 name;
    s64 propertyType;
    if (propertyType == 16) { //Array Property
        s64 arraySize;
    }
    s64 variant;
    u8 dupIndex;
    if (propertyType == 55) {//Int Property
        s32 numberValue;
    }
    else if(propertyType == 65){ //Name Property
        s64 nameValue;
    }
    else if(propertyType == 16 && variant == 76){//Text Property
        s32 pageCount;
        
        page pages[pageCount];
        
        
    }
    else if(propertyType == 16 && variant == 75){//Strut Property
        pageDataArray;
        iconElement icons;
        
    }
    
    
    
};

struct message{
    
    entryType id;
    entryType label;
    entryType text;
    entryType pageData;
};

message messages[entryCount] @0x56;