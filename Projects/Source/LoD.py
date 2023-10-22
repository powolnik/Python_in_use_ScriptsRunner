#import math

import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general_ue as general_ue
import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.src.set_asset as set_asset
import unreal_engine_scripts.service.log as log

import unreal

# To apply changes in modules
import importlib
importlib.reload(config)
importlib.reload(general_ue)
importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(log)


NO_MIPMAP_HEADER = 'Textures without mipmaps: '

## Find all textures not in Power of two mode. If texture is not standart, lod can't be generated
def find_no_mipmap_textures_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data(package_paths = target_paths,
                                        class_names = [config.CLASS_NAME_TEXTURE], recursive_classes = True,
                                        recursive_paths = is_recursive_search,
                                        include_only_on_disk_assets = only_on_disk_assets,
                                        properties_values = [(config.PROPERTY_MIPMAP_GEN, config.SETTING_NO_MIPMAPS)],
                                        log_path = log.LOG_PATH_NO_MIPMAPS, log_title = 'No Mipmap Textures')

## Find all meshes without lod groups
def find_no_lods_meshes_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data(package_paths = target_paths,
                                      class_names = [config.CLASS_NAME_STATIC_MESH],
                                      recursive_paths = is_recursive_search,
                                      include_only_on_disk_assets = only_on_disk_assets,
                                      properties_values = [(config.PROPERTY_LOD_GROUP, config.SETTING_NO_LOD_GROUP)],
                                      log_path = log.LOG_PATH_NO_LODS, log_title = 'No Lods Static Meshes')

#================================Mipmaps===========================================================

## Sets textures mipmap generation setting to new_value
# @param texture_paths object_paths of texture assets
def set_textures_mipmap_gen_settings_log(texture_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_MIPMAP_GEN, new_value)]
    return set_asset.set_assets_properties_in_object_paths(texture_paths, new_properties_values, is_recursive_search,
                                                           only_on_disk_assets, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                                           search_properties_values, is_disjunction,
                                                           log_path = log.LOG_PATH_SET_PROPERTIES,
                                                           log_title = 'set_textures_mipmap_gen_settings_log')

## Sets textures mipmap generation setting to new_value
# @param dirs_paths paths to dirs with texture assets
def set_textures_mipmap_gen_settings_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_textures_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_textures_mipmap_gen_settings_log(object_paths, new_value,
                                                is_recursive_search, only_on_disk_assets,
                                                search_properties_values, is_disjunction)

## Sets textures with no mipmap gen settings to generate mipmaps new_value. Writing logs.
# @param dirs_paths paths to dirs with texture assets
def set_textures_with_no_mipmap_gen_settings_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                                 is_recursive_search = True, only_on_disk_assets = False,
                                                 search_properties_values = [], is_disjunction = True):
    assets_data = find_no_mipmap_textures_log(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_textures_mipmap_gen_settings_log(object_paths, new_value,
                                                 is_recursive_search, only_on_disk_assets,
                                                 search_properties_values, is_disjunction)

#================================Lod===========================================================

## Sets textures with no mipmap gen settings to generate mipmaps new_value. Writing logs.
# @param dirs_paths paths to dirs with texture assets
def set_meshes_lod_group_log(mesh_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_LOD_GROUP, new_value)]
    return set_asset.set_assets_properties_in_object_paths(mesh_paths, new_properties_values, is_recursive_search,
                                                           only_on_disk_assets, [config.CLASS_NAME_STATIC_MESH],
                                                           search_properties_values, is_disjunction,
                                                           log_path = log.LOG_PATH_SET_PROPERTIES,
                                                           log_title = 'set_meshes_lod_group_log')

def set_meshes_lod_group_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_static_mesh_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_meshes_lod_group_log(object_paths, new_value,
                                     is_recursive_search, only_on_disk_assets,
                                     search_properties_values, is_disjunction)

## Sets lod group to meshes with no lod group in dirs. Writing logs.
def set_meshes_with_no_lods_group_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                                        is_recursive_search = True, only_on_disk_assets = False,
                                        search_properties_values = [], is_disjunction = True):
    assets_data = find_no_lods_meshes_log(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_meshes_lod_group_log(object_paths, new_value,
                                     is_recursive_search, only_on_disk_assets,
                                     search_properties_values, is_disjunction)

def set_mipmaps_n_lod_group_to_no_lods_dirs(dirs_paths,
                                            new_value_mipmaps = config.SETTING_DEFAULT_MIPMAPS,
                                            new_value_lod_group = config.SETTING_DEFAULT_LOD_GROUP,
                                            is_recursive_search = True, only_on_disk_assets = False,
                                            search_properties_values = [], is_disjunction = True):
    assets_data_no_mipmaps = set_textures_with_no_mipmap_gen_settings_dirs(dirs_paths, new_value_mipmaps,
                                                                        is_recursive_search, only_on_disk_assets,
                                                                        search_properties_values, is_disjunction)
    unreal.log('_')
    assets_data_no_lods = set_meshes_with_no_lods_group_dirs(dirs_paths, new_value_lod_group,
                                                            is_recursive_search, only_on_disk_assets,
                                                            search_properties_values, is_disjunction)
    unreal.log('_')
    return assets_data_no_mipmaps, assets_data_no_lods

#========================================================================================

def is_lod_number_ok(number_of_lod):
    if number_of_lod in range(1,9):
        return True
    else:
        return False

def get_lod_count(static_mesh):
    if static_mesh is not None:
        return static_mesh.get_num_lods()
    else:
        unreal.log_error(get_lod_count.__name__ + '(): static_mesh must not be None')
    return 0

def is_input_ok_set_number_of_lod(assets_data, number_of_lod):
    if general_ue.is_not_none_or_empty(assets_data):
        if is_lod_number_ok(number_of_lod):
            return True
        else:
            unreal.log_error(is_input_ok_set_number_of_lod.__name__ + '(): number_of_lod must be in range [1, 8]')
    else:
        unreal.log_error(is_input_ok_set_number_of_lod.__name__ + '(): assets_data must not be None or Empty')
    return False

def get_editor_reduction_setting_for_lod(static_mesh, lod_indx, screen_sizes = None):
    if screen_sizes is None:
        screen_sizes = unreal.EditorStaticMeshLibrary.get_lod_screen_sizes(static_mesh)
    mesh_reduction_settings = unreal.EditorStaticMeshLibrary.get_lod_reduction_settings(static_mesh, lod_indx)
    percent_triangles = mesh_reduction_settings.get_editor_property('percent_triangles')
    editor_reduction_setting = unreal.EditorScriptingMeshReductionSettings(percent_triangles, screen_sizes[lod_indx])
    return editor_reduction_setting

## Set lod count
# @param number_of_lod must be in range [1, 8]
# Error: For 6-8 Lod making wrong mesh sections.This leads to problems with texture maps. Better to use editor functions
def change_number_of_lod(assets_data, new_number_of_lod = 1, auto_compute_lod_screen_size = True):
    if is_input_ok_set_number_of_lod(assets_data, new_number_of_lod):
        static_meshes = get_asset.get_assets_from_assets_data(assets_data)
        for static_mesh in static_meshes:
            lod_count = get_lod_count(static_mesh)
            if is_lod_number_ok(lod_count):
                editor_reduction_settings = []
                screen_sizes = unreal.EditorStaticMeshLibrary.get_lod_screen_sizes(static_mesh)
                # Creates list of reduction settings
                if new_number_of_lod > lod_count:
                    for lod_indx in range(lod_count):
                        editor_reduction_settings.append(get_editor_reduction_setting_for_lod(static_mesh, lod_indx, screen_sizes))
                    last_lod_reduction_settings = get_editor_reduction_setting_for_lod(static_mesh, lod_count - 1, screen_sizes)
                    last_lod_percent_triangles = 0
                    if lod_count != 1:
                        last_lod_percent_triangles = last_lod_reduction_settings.get_editor_property('percent_triangles')
                    else:
                        last_lod_percent_triangles = 0.5
                    screen_size = last_lod_reduction_settings.get_editor_property('screen_size')
                    for lod_indx in range(lod_count, new_number_of_lod):
                        if lod_indx > 1:
                            last_lod_percent_triangles = last_lod_percent_triangles * 0.5
                        new_reduction_setting = unreal.EditorScriptingMeshReductionSettings(last_lod_percent_triangles, screen_size)
                        editor_reduction_settings.append(new_reduction_setting)
                elif new_number_of_lod <= lod_count:
                    for lod_indx in range(new_number_of_lod):
                        editor_reduction_settings.append(get_editor_reduction_setting_for_lod(static_mesh, lod_indx, screen_sizes))

                reduction_options = unreal.EditorScriptingMeshReductionOptions(auto_compute_lod_screen_size = True,
                                                                               reduction_settings = editor_reduction_settings)
                reduction_options.set_editor_property('auto_compute_lod_screen_size', True)
                lods_created = unreal.EditorStaticMeshLibrary.set_lods_with_notification(static_mesh, reduction_options, apply_changes = True)

                '''mesh_reduction_settings = []
                for lod_indx in range(new_number_of_lod):
                    mesh_reduction_settings = unreal.EditorStaticMeshLibrary.get_lod_reduction_settings(static_mesh, lod_indx)
                    unreal.EditorStaticMeshLibrary.set_lod_reduction_settings(static_mesh, lod_indx, mesh_reduction_settings)'''

                unreal.log('Lods_created: ' + str(lods_created))
            else:
                unreal.error_log(change_number_of_lod.__name__ + '(): lod_count is out of bound [1, 8]')

## Changes lod count
# @param number_of_lod must be in range [1, 8]
def change_number_of_lod_in_dirs(dirs_paths, new_number_of_lod = 1,
                                 is_recursive_search = True, only_on_disk_assets = False,
                                 search_properties_values = [], is_disjunction = True, auto_compute_lod_screen_size = True):
    assets_data = get_asset.find_assets_data(package_paths = dirs_paths,
                                             class_names = [config.CLASS_NAME_STATIC_MESH],
                                             recursive_paths = is_recursive_search,
                                             include_only_on_disk_assets = only_on_disk_assets,
                                             properties_values = search_properties_values)
    change_number_of_lod(assets_data, new_number_of_lod, auto_compute_lod_screen_size)