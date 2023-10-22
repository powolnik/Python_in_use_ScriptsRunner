import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
# Folder, that stores unreal_engine_scripts package
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_engine_scripts.service.general_ue as general_ue

# To apply changes in modules
import importlib
importlib.reload(general_ue)


## https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/AssetNaming/
AssetsPrefixConventionTable = {
    ##general
    'HDRI' :                    'HDR_',
    'Material' :	            'M_',
    'MaterialInstanceConstant':	'MI_',
    'PhysicsAsset':	            'PHYS_',
    'PhysicsMaterial':	        'PM_',
    'PostProcessMaterial':      'PPM_',
    'SkeletalMesh':	            'SK_',
    'StaticMesh':	            'SM_',
    'Texture':	                'T_',
    'Texture2D':	            'T_',
    'OCIOProfile':	            'OCIO_',

    ##Blueprints
    'ActorComponent':	    'AC_',
    'AnimationBlueprint':   'ABP_',
    'BlueprintInterface':	'BI_',
    'Blueprint':	        'BP_',
    'CurveTable':	        'CT_',
    'DataTable':	        'DT_',
    'Enum':	                'E_',
    'Structure':	        'F_',
    'WidgetBlueprint':	    'WBP_',

    ##Particle Effects
    'ParticleSystem':   'PS_',
    'NiagaraEmitter':	'FXE_',
    'NiagaraSystem':	'FXS_',
    'NiagaraFunction':	'FXF_',

    ##Skeletal Mesh Animations
    'Rig':	                'Rig_',
    'Skeleton':	            'SKEL_',
    'Montages':	            'AM_',
    'Animation Sequence':   'AS_',
    'Blend Space':	        'BS_',

    ##ICVFX
    'NDisplayConfiguration':    'NDC_',

    ##Animation
    'LevelSequence':	'LS_',
    'SequencerEdits':	'EDIT_',

    ##Media
    'MediaSource':	    'MS_',
    'MediaOutput':	    'MO_',
    'MediaPlayer':	    'MP_',
    'MediaProfile':	    'MPR_',

    ##Other
    'LevelSnapshots':	    'SNAP_',
    'RemoteControlPreset':  'RCP_'
}

TextureTypesConvention = {
    ## Convention Unreal Engine Types
    'General':              ('T_', ''),
    'BaseColor':	        ('T_', '_BC'),
    'AmbientOcclusion':    ('T_', '_AO'),
    'Roughness':	        ('T_', '_R'),
    'Specular':	            ('T_', '_S'),
    'Metallic':	            ('T_', '_M'),
    'Normal':	            ('T_', '_N'),
    'Emissive':	            ('T_', '_E'),
    'Mask':	                ('T_', '_Mask'),
    'FlowMap':	            ('T_', '_F'),
    'Height':	            ('T_', '_H'),
    'Displacement':	        ('T_', '_D'),
    'LightMap':	        ('T_', '_L'),
    'Alpha/Opacity':	    ('T_', '_A'),
    'Packed':	            ('T_', '_*'),
    'TextureCube':	        ('TC_', ''),
    'MediaTexture':	    ('MT_', ''),
    'RenderTarget':	    ('RT_', ''),
    'CubeRenderTarget':	('RTC_', ''),
    'TextureLightProfile':	('TLP_', ''),
}

# https://help.poliigon.com/en/articles/1712652-what-are-the-different-texture-maps-for
# https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/AssetNaming/
# https://unrealcommunity.wiki/assets-naming-convention-qqp2b5m1
# https://www.unrealdirective.com/resource/asset-naming-conventions
# https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2

## Maybe Upper case is not important in prefix search
# May Differ from Convention variant. Added more types.
# All checks for suffix are case insensitive
# Standard default suffix for texture is in zero position in list. F.e. for BaseColor it is _Diff
TextureTypesCustom = {
    ## general Simple Types
    #'General':              ('T_', ['']),
    'BaseColor':	        ('T_', ['_Diff', '', '_BC', '_BaseColor', '_Diffuse', '_Base_Color', '_Color', '_Base']),
    'Albedo':	            ('T_', ['_Albedo', '_ALB']),
    'AmbientOcclusion':     ('T_', ['_AO', '_AmbientOcclusion', '_Ambient', '_Occlusion', '_Occl', '_Occ', '_Occlus']),
    'Roughness':	        ('T_', ['_Rough', '_R', '_Roughness', '_Roughn']),
    'Gloss':	            ('T_', ['_Gloss', '_G', '_Glossiness'] ),
    'Specular':	            ('T_', ['_Spec', '_S', '_Specular', '_Reflection', '_Reflect', '_Refl']),
    'Metallic':	            ('T_', ['_Metal', '_M', '_Metallic', '_Metalness']),
    'Normal':	            ('T_', ['_Normal', '_N', '_Norm']),
    'Height':	            ('T_', ['_Height', '_H']),
    'Bump':	                ('T_', ['_Bump', '_B']),
    'Displacement':	        ('T_', ['_Displace', '_D', '_Displacement', '_Disp', '_Displ', '_Displac']),
    'Emissive':	            ('T_', ['_Emissive', '_E', '_Emis', '_Emiss', '_Illumination', '_Illum', '_Illumin']),
    'Alpha/Opacity':	    ('T_', ['_Opacity', '_A', '_Alpha', '_Opac']),
    'OpacityMask':	        ('T_', ['_OpacityMask', '_Mask', '_OpacMask']),
    'LightMap':	            ('T_', ['_LightMap', '_L', '_Light']),

    ## Combo, Mix Types
    'OcclusionRoughnessMetallic':     ('T_', ['_MetalRough', '_ORM', '_RoughnessMetallic', '_RoughnMetal', '_RoughMetal',
                                               '_MetallicRoughness', '_MetalRoughn', '_MetalRoughness'
                                               '_occlusionRoughnessMetallic', '_occlusionRoughnessMetal', '_occlRoughnMetal']),
    'SpecularGlossiness':              ('T_', ['_SpecGloss', '_SpecularGlossiness', '_SpecularGloss', '_SpecGlossiness']),

    ## Unique Types
    'Convex/Concave':	    ('T_', ['_ConvexConcave', '_ConvConc', '_Convex', '_Conv', '_Concave', '_Conc']),
    'FUZZ':                 ('T_', ['_Fuzz']),

    ## Rare Types
    'FlowMap':	            ('T_', ['_F']),
    'Packed':	            ('T_', ['_*']),
    'TextureCube':	        ('TC_', ['']),
    'MediaTexture':	        ('MT_', ['']),
    'RenderTarget':	        ('RT_', ['']),
    'CubeRenderTarget':	    ('RTC_', ['']),
    'TextureLightProfile':	('TLP_', [''])

    ## By Channel
}

## Common suffix find in downloaded gltf textures files
GLTF_SuffixConvention = {
    'BaseColor':                    '_baseColor',
    'Normal':                       '_normal',
    'OcclusionRoughnessMetallic':   '_metallicRoughness',
    'Emissive':                     '_emissive'
}

## Finds in TextureTypesCustom prefix by texture_type
# @param texture_type (str) key to dictionary TextureTypesCustom
# @return tuple (prefix, [suffixes]). Returns None if key texture_type not found
def get_TextureTypesCustom_prefix_suffix_list(texture_type):
    prefix_suffix_list = None
    if general_ue.is_not_none_or_empty(texture_type):
        prefix_suffix_list = TextureTypesCustom.get(texture_type)
    else:
        unreal.log(get_TextureTypesCustom_prefix_suffix_list.__name__ + '(): texture_type must not be None or Empty')

    return prefix_suffix_list

## Finds in TextureTypesCustom prefix by texture_type
# @param texture_type (str) key to dictionary TextureTypesCustom
# @return tuple (prefix, [suffixes]). Returns None if key texture_type not found
def get_TextureTypesCustom_prefix(texture_type):
    prefix_suffix_list = get_TextureTypesCustom_prefix_suffix_list(texture_type)
    if prefix_suffix_list is not None:
        return get_TextureTypesCustom_prefix_suffix_list(texture_type)[0]
    else:
        return None

## Finds in TextureTypesCustom suffix by texture_type
# @param texture_type (str) key to dictionary TextureTypesCustom
# @return tuple (prefix, [suffixes]). Returns None if key texture_type not found
def get_TextureTypesCustom_suffix_list(texture_type):
    prefix_suffix_list = get_TextureTypesCustom_prefix_suffix_list(texture_type)
    if prefix_suffix_list is not None:
        return get_TextureTypesCustom_prefix_suffix_list(texture_type)[1]
    else:
        return None

## Finds in TextureTypesCustom standard suffix by texture_type
# @param texture_type (str) key to dictionary TextureTypesCustom
# @return tuple (prefix, [suffixes]). Returns None if key texture_type not found
def get_TextureTypesCustom_standard_suffix(texture_type):
    suffix_list = get_TextureTypesCustom_suffix_list(texture_type)
    if suffix_list is not None:
        return get_TextureTypesCustom_prefix_suffix_list(texture_type)[1][0]
    else:
        return None

## All conventional prefixes of Unreal Engine
assets_prefix_convention_table_prefixes = set()
## All custom texture suffixes
texture_types_custom_suffixes = set()

def set_AssetsPrefixConventionTable_prefixes():
    if len(assets_prefix_convention_table_prefixes) == 0:
        for key in AssetsPrefixConventionTable:
            prefix = AssetsPrefixConventionTable[key]
            assets_prefix_convention_table_prefixes.add(prefix)

def get_AssetsPrefixConventionTable_prefixes():
    set_AssetsPrefixConventionTable_prefixes()
    return assets_prefix_convention_table_prefixes

def set_TextureTypesCustom_suffixes():
    if len(texture_types_custom_suffixes) == 0:
        for key in TextureTypesCustom:
            suffix_list = TextureTypesCustom[key][1]
            for suffix in suffix_list:
                texture_types_custom_suffixes.add(suffix)

def get_TextureTypesCustom_suffixes():
    set_TextureTypesCustom_suffixes()
    return texture_types_custom_suffixes
