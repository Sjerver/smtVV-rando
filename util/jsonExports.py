import copy
#Format for RelativeScale3D Property with 2 for values x,y,z
RELATIVE_SCALE_3D = {'$type': 'UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI', 'StructType': 'Vector', 'SerializeNone': True, 'StructGUID': '{00000000-0000-0000-0000-000000000000}', 'SerializationControl': 'NoExtension', 'Operation': 'None', 'Name': 'RelativeScale3D', 'ArrayIndex': 0, 'IsZero': False, 'PropertyTagFlags': 'None', 'PropertyTagExtensions': 'NoExtension', 'Value': [
    {'$type': 'UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI', 'Name': 'RelativeScale3D', 'ArrayIndex': 0, 'IsZero': False, 'PropertyTagFlags': 'None', 'PropertyTagExtensions': 'NoExtension', 'Value': {'$type': 'UAssetAPI.UnrealTypes.FVector, UAssetAPI', 'X': 2.0, 'Y': 2.0, 'Z': 2.0}}
]}

#KismetBytecode Expression for a jump in the bytecode
BYTECODE_JUMP = {
          "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_Jump, UAssetAPI",
          "CodeOffset": 0
        }

#KismetBytecode Expression for an empty expression (useful as filler)
BYTECODE_NOTHING = {"$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_Nothing, UAssetAPI"}

BYTECODE_EX_NAMECONST= {
              "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_NameConst, UAssetAPI",
              "Value": "PLACEHOLDER"
            }

BYTECODE_EX_INTCONST= {
                  "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_IntConst, UAssetAPI",
                  "Value": 0
                }

BASE_MAPSYMBOLPARAMS = {
            "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
            "StructType": "MapSymbolParam",
            "SerializeNone": True,
            "StructGUID": "{00000000-0000-0000-0000-000000000000}",
            "Name": "デフォルト",
            "DuplicationIndex": 0,
            "IsZero": False,
            "Value": [
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI",
                "Name": "DevilId_7_329BFC6143ACC514C3F26DAEEF5AE0B2",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": 0
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 200.0,
                "Name": "WalkSpeed_3_7ED0C64D46445B3F5AB86082C81E8A32",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 700.0,
                "Name": "AssaultSpeed_4_A8F866DC4972D996F783CBB4B4BAB98D",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 800.0,
                "Name": "AttackChangeLength_35_DE6A46A54D83A507DEFC24BB675AE95D",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 1.2000000476837158,
                "Name": "MapSymbolScale_21_1FBF88074CD086C174AFDFBC8C9BFEF8",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 60.0,
                "Name": "EncountCollision_SizeX_41_8F92E1144508B1A5CAA11897146919C3",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 100.0,
                "Name": "EncountCollision_SizeY_40_C30F23F04766F301FF299E9BA00E1BD0",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 60.0,
                "Name": "EncountCollision_SizeZ_42_954969E74583F20E26B7AB99DB23D0BD",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": "+0",
                "Name": "EncountCollision_BottomSize_76_7AF5F6824243A1DC241349A05322FB9B",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": "+0",
                "Name": "AttackCollision_AddSize_45_E78B3E3A48655E56F45B19A0747E6ADB",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 80.0,
                "Name": "AttackCollision_AddBottomSize_72_032D6CC74A49F3DE09CD178066C11CFF",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 0.5,
                "Name": "AttackCollision_ChangeTime_47_A65C5701464C6F6900C4B1BBE8CBF51A",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": -1.0,
                "Name": "AttackCollision_ReturnTime_49_8A764C074A194653E1B9AF89443764F1",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.EnumPropertyData, UAssetAPI",
                "EnumType": "E_CHARA_MOTION_ID",
                "InnerType": None,
                "Name": "AttackMotionID_82_B265863C4FEB2AF3E0681A83D6D5096D",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": "E_CHARA_MOTION_ID::ATTACK"
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 0.30000001192092896,
                "Name": "MotionBlendTime_30_6E49A558411DFAF97EAC3DB7684E03F2",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 270.0,
                "Name": "TurnSpeed_31_B6251F5448BC8A42741C4C9646A4365F",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 50.0,
                "Name": "MovingTurnSpeed_34_CBD370044FE0C820DC0DDBA0172E4E9F",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": "+0",
                "Name": "AddForward_CheckWall_63_FDD8F8B5454DB72CE0E6C5B7FA29A5E7",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": "+0",
                "Name": "AddWidth_CheckWall_64_9550918743896AE8DF977D9DF518B4C7",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                "Value": 110.0,
                "Name": "ClimbableHeight_62_1AF33E984D582351F695DC9834429B31",
                "DuplicationIndex": 0,
                "IsZero": False
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Objects.ArrayPropertyData, UAssetAPI",
                "ArrayType": "StructProperty",
                "DummyStruct": {
                  "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                  "StructType": "MapSymbolDiscoveryMotion",
                  "SerializeNone": True,
                  "StructGUID": "{BFB65238-4E02-8497-6283-C2908279F7E5}",
                  "Name": "DiscoveryMotions_68_0CF7D35F497F0B077C1067B1949CA36A",
                  "DuplicationIndex": 0,
                  "IsZero": False,
                  "Value": []
                },
                "Name": "DiscoveryMotions_68_0CF7D35F497F0B077C1067B1949CA36A",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": []
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                "StructType": "MapSymbolParam_Inhale",
                "SerializeNone": True,
                "StructGUID": "{F8F5C5C7-4F79-BBF7-C39D-BFAC95FAB2CA}",
                "Name": "InhaleParam_83_0BA84A5242A7371DC9568E933CC0BC07",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": [
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                    "Value": 600.0,
                    "Name": "ForceMax_2_C85CB22546382B62786ED492ECDF4627",
                    "DuplicationIndex": 0,
                    "IsZero": False
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                    "Value": 1300.0,
                    "Name": "InhaleDistanceMin_11_E943582B4A5044374A3FA1A5B7D4E017",
                    "DuplicationIndex": 0,
                    "IsZero": False
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.FloatPropertyData, UAssetAPI",
                    "Value": 2000.0,
                    "Name": "InhaleDistanceMax_12_1ACBAE24428616E2BFE64A994984747B",
                    "DuplicationIndex": 0,
                    "IsZero": False
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.EnumPropertyData, UAssetAPI",
                    "EnumType": "E_CHARA_MOTION_ID",
                    "InnerType": None,
                    "Name": "InhaleMotion_13_3F10AFEA4E91079A9C9B03A1838B61FD",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": "E_CHARA_MOTION_ID::IDLE01"
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.EnumPropertyData, UAssetAPI",
                    "EnumType": "E_CHARA_MOTION_ID",
                    "InnerType": None,
                    "Name": "InhaleEndMotion_16_FEBAFE0B433F7E5C7ED07F8309E8447F",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": "E_CHARA_MOTION_ID::NONE"
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.SoftObjectPropertyData, UAssetAPI",
                    "Name": "InhaleEffect_20_C0E2E51E4F163FC2B32FED9179A8211F",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": {
                      "$type": "UAssetAPI.PropertyTypes.Objects.FSoftObjectPath, UAssetAPI",
                      "AssetPath": {
                        "$type": "UAssetAPI.PropertyTypes.Objects.FTopLevelAssetPath, UAssetAPI",
                        "PackageName": None,
                        "AssetName": "None"
                      },
                      "SubPathString": None
                    }
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.NamePropertyData, UAssetAPI",
                    "Name": "InhaleEffectSocket_23_14EA742A47D4695301B1588D9C413FCD",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": "None"
                  },
                  {
                    "$type": "UAssetAPI.PropertyTypes.Objects.SoftObjectPropertyData, UAssetAPI",
                    "Name": "InhaleDecal_29_CF8BCF1D4220755104AAC59667658B80",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": {
                      "$type": "UAssetAPI.PropertyTypes.Objects.FSoftObjectPath, UAssetAPI",
                      "AssetPath": {
                        "$type": "UAssetAPI.PropertyTypes.Objects.FTopLevelAssetPath, UAssetAPI",
                        "PackageName": None,
                        "AssetName": "None"
                      },
                      "SubPathString": None
                    }
                  }
                ]
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                "StructType": "Vector",
                "SerializeNone": True,
                "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                "Name": "AttackCollision2_Offset_87_6D920E984A4E74ECE79C48B753EDA9F5",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": [
                  {
                    "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                    "Name": "AttackCollision2_Offset_87_6D920E984A4E74ECE79C48B753EDA9F5",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": {
                      "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                      "X": "+0",
                      "Y": "+0",
                      "Z": "+0"
                    }
                  }
                ]
              },
              {
                "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                "StructType": "Vector",
                "SerializeNone": True,
                "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                "Name": "AttackCollision2_Size_88_C4F598AE415A4EE7F953C997B3CBD076",
                "DuplicationIndex": 0,
                "IsZero": False,
                "Value": [
                  {
                    "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                    "Name": "AttackCollision2_Size_88_C4F598AE415A4EE7F953C997B3CBD076",
                    "DuplicationIndex": 0,
                    "IsZero": False,
                    "Value": {
                      "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                      "X": "+0",
                      "Y": "+0",
                      "Z": "+0"
                    }
                  }
                ]
              }
            ]
          }

VOICEMAP_ESCAPE = [[
                        {
                          "$type": "UAssetAPI.PropertyTypes.Objects.EnumPropertyData, UAssetAPI",
                          "EnumType": None,
                          "InnerType": None,
                          "Name": "VoiceMap",
                          "DuplicationIndex": 0,
                          "IsZero": False,
                          "Value": "EDevilVoiceType::Escape"
                        },
                        {
                          "$type": "UAssetAPI.PropertyTypes.Objects.SoftObjectPropertyData, UAssetAPI",
                          "Name": "VoiceMap",
                          "DuplicationIndex": 0,
                          "IsZero": False,
                          "Value": {
                            "$type": "UAssetAPI.PropertyTypes.Objects.FSoftObjectPath, UAssetAPI",
                            "AssetPath": {
                              "$type": "UAssetAPI.PropertyTypes.Objects.FTopLevelAssetPath, UAssetAPI",
                              "PackageName": None,
                              "AssetName": "/Game/Sound/CueSheet/Devil/Devil_vo/dev303_vo_ramia/dev303_vo_07.dev303_vo_07"
                            },
                            "SubPathString": None
                          }
                        }
                      ]]

VOICEMAP_FIND =  [[
                        {
                          "$type": "UAssetAPI.PropertyTypes.Objects.EnumPropertyData, UAssetAPI",
                          "EnumType": None,
                          "InnerType": None,
                          "Name": "VoiceMap",
                          "DuplicationIndex": 0,
                          "IsZero": False,
                          "Value": "EDevilVoiceType::Find"
                        },
                        {
                          "$type": "UAssetAPI.PropertyTypes.Objects.SoftObjectPropertyData, UAssetAPI",
                          "Name": "VoiceMap",
                          "DuplicationIndex": 0,
                          "IsZero": False,
                          "Value": {
                            "$type": "UAssetAPI.PropertyTypes.Objects.FSoftObjectPath, UAssetAPI",
                            "AssetPath": {
                              "$type": "UAssetAPI.PropertyTypes.Objects.FTopLevelAssetPath, UAssetAPI",
                              "PackageName": None,
                              "AssetName": "/Game/Sound/CueSheet/Devil/Devil_vo/dev303_vo_ramia/dev303_vo_10.dev303_vo_10"
                            },
                            "SubPathString": None
                          }
                        }
                      ]]

def getBooleanPropertyVar(name, value):
   return {
          "$type": "UAssetAPI.FieldTypes.FBoolProperty, UAssetAPI",
          "ArrayDim": "TArray",
          "BlueprintReplicationCondition": "COND_None",
          "ByteMask": 1,
          "ByteOffset": 0,
          "ElementSize": 1,
          "FieldMask": 255,
          "FieldSize": 1,
          "Flags": "RF_Public",
          "MetaDataMap": None,
          "Name": name,
          "NativeBool": True,
          "PropertyFlags": "CPF_None",
          "RawValue": None,
          "RepIndex": 0,
          "RepNotifyFunc": "None",
          "SerializedType": "BoolProperty",
          "UsmapPropertyTypeOverrides": {
            "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[UAssetAPI.Unversioned.EPropertyType, UAssetAPI]], System.Private.CoreLib",
            "ClassProperty": "ObjectProperty",
            "MulticastInlineDelegateProperty": "MulticastDelegateProperty",
            "SoftClassProperty": "SoftObjectProperty"
          },
          "Value": value
        }

def getLetBool(assignmentExp = {}, varExp = {}):
   return {
        "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_LetBool, UAssetAPI",
        "AssignmentExpression": assignmentExp,
        "VariableExpression": varExp
    }

def getImportedFunctionCall(stackNode, parameters):
    return {
          "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath, UAssetAPI",
          "StackNode": stackNode,
          "Parameters": parameters
        }

def getLocalVar(name):
   return {
            "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVariable, UAssetAPI",
            "Variable": {
                "$type": "UAssetAPI.Kismet.Bytecode.KismetPropertyPointer, UAssetAPI",
                "New": {
                    "$type": "UAssetAPI.UnrealTypes.FFieldPath, UAssetAPI",
                    "Path": [
                        name
                    ],
                    "ResolvedOwner": 1
                }
            }
        }

def getJumpIfNot(booleanExp, offset):
   return {
        "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_JumpIfNot, UAssetAPI",
        "BooleanExpression": booleanExp,
        "CodeOffset": offset
    }

def getIntConst(value):
   intConst = copy.deepcopy(BYTECODE_EX_INTCONST)
   intConst["Value"] = value
   return intConst

def getBytecodeBoolean(value = True):
    if value:
      return {
                "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_True, UAssetAPI"
              }
    else:
       return {
                "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_False, UAssetAPI"
              }