import re

import unreal

import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general_ue as general_ue
import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.src.naming_convention as convention
import unreal_engine_scripts.external.python_library.src.prefix_suffix as prefix_suffix_python

import importlib
importlib.reload(config)
importlib.reload(general_ue)
importlib.reload(get_asset)
importlib.reload(convention)
importlib.reload(prefix_suffix_python)


# \/:*?"<>|+
WINDOWS_RESTRICTED_CHARS = '\\/:*?\"<>|+'
# In the end of file name: space and .

WINDOWS_RESTRICTED_CHARS_END = ' .'
UNIX_RESTRICTED_CHARS = '/\\0'
REGEX_WINDOWS_RESTRICTED_CHARS = '[' + WINDOWS_RESTRICTED_CHARS + ']'
REGEX_WINDOWS_RESTRICTED_CHARS_END = '[' + WINDOWS_RESTRICTED_CHARS_END + ']\\Z'

NO_TEXTURE_TYPE = 'None'


def has_restricted_chars_for_os(str, show_log = False):
    if str != '':
        if re.search(REGEX_WINDOWS_RESTRICTED_CHARS, str) == None:
            if re.search(REGEX_WINDOWS_RESTRICTED_CHARS_END, str) == None:
                return False
            elif show_log:
                unreal.log_error(has_restricted_chars_for_os.__name__ + '(): file name must not end on chars: space or .')
                return True
        elif show_log:
            unreal.log_error(has_restricted_chars_for_os.__name__ + '(): file name must not has chars: \\/:*?"<>|+')
            return True
    else:
        return False

## @return (str) name of asset without prefix and suffix, without extension.
# [Deprecated]
def get_asset_name_without_prefix_suffix_v2(object_path):
    if general_ue.is_not_none_or_empty(object_path):
        file_name_no_extension = unreal.Paths.get_base_filename(object_path)
        # (?<=^[^_]+_).+(?=_[^_]+)
        #regex_pattern = '(?<=^[^_]+_).+(?=_[^_]+)'  # '\\Z'
        regex_pattern = '^[^_]+_(?P<name>.+)(_[^_]+)?\\Z'     # \\Z
        match_object = re.search(regex_pattern, file_name_no_extension)
        if match_object is not None:
            return match_object.group('name')
        else:
            unreal.log(get_asset_name_without_prefix_suffix.__name__ + ': regex did not find any name without prefix or suffix')
            return file_name_no_extension
    else:
        unreal.log_error(get_asset_name_without_prefix_suffix.__name__ + ': object_path must not be None or empty')
        return ''

## @return (str) name of asset without prefix and suffix, without extension.
def get_asset_name_without_prefix_suffix(object_path):
    if general_ue.is_not_none_or_empty(object_path):
        file_name_no_extension = unreal.Paths.get_base_filename(object_path)
        file_name_no_prefix_suffix = file_name_no_extension
        prefix = prefix_suffix_python.get_prefix(file_name_no_extension)
        #unreal.log('prefix'); unreal.log(prefix)
        if prefix in convention.get_AssetsPrefixConventionTable_prefixes():
            file_name_no_prefix_suffix = file_name_no_prefix_suffix[len(prefix):]

        suffix = prefix_suffix_python.get_suffix(file_name_no_extension)
        #unreal.log('suffix'); unreal.log(suffix)
        if suffix in convention.get_TextureTypesCustom_suffixes():
            file_name_no_prefix_suffix = file_name_no_prefix_suffix[:-len(suffix)]
        return file_name_no_prefix_suffix
    else:
        unreal.log_error(get_asset_name_without_prefix_suffix.__name__ + ': object_path must not be None or empty')
        return ''

def get_asset_name_without_prefix_suffix_data(data_asset):
    if data_asset is not None:
        return get_asset_name_without_prefix_suffix(get_asset.get_asset_data_object_path(data_asset))
    else:
        return ''

## @param file_name without extension: T_Texture_Diff
# @return tuple (prefix, suffix)
def get_asset_prefix_suffix_by_name(file_name_no_extension):
    prefix, suffix = '', ''
    if file_name_no_extension != '':
        prefix_regex = prefix_suffix_python.PREFIX_REGEX
        match_object = re.search(prefix_regex, file_name_no_extension)
        if match_object != None:
            prefix = match_object[0]

        suffix_regex = prefix_suffix_python.SUFFIX_REGEX
        match_object = re.search(suffix_regex, file_name_no_extension)
        if match_object != None:
            suffix = match_object[0]
    else:
        unreal.log_error(get_asset_prefix_suffix_by_name.__name__ + '(): file_name is empty. ' + file_name_no_extension)

    return prefix, suffix

def get_asset_prefix_suffix_by_path(object_path):
    return get_asset_prefix_suffix_by_name(get_asset.get_asset_name_no_extension(object_path))

def get_asset_prefix_suffix_by_asset_data(asset_data):
    if asset_data is not None:
        asset_name_no_extension = get_asset.get_asset_name_no_extension_in_data_asset(asset_data)
        return get_asset_prefix_suffix_by_name(asset_name_no_extension)
    else:
        unreal.log(get_asset_prefix_suffix_by_asset_data.__name__ + '(): asset_data must not be None')
        return '', ''


## @param file_name File name without extension, without path
def has_file_name_prefix(file_name,  prefix, has_logs = False):
    if file_name != '':
        if prefix != '':
            prefix_regex = '^' + prefix
            if re.search(prefix_regex, file_name) != None:
                return True
            else:
                return False

        elif has_logs:
            unreal.log(has_file_name_prefix.__name__ + '(): prefix is empty')
    elif has_logs:
        unreal.log_error(has_file_name_prefix.__name__ + '(): file_name is empty. ' + file_name)

## @param file_name File name without extension, without path
def has_file_name_suffix(file_name, suffix, has_logs = False):
    if file_name != '':
        if suffix != '':
            suffix_regex = suffix + '\\Z'
            if re.search(suffix_regex, file_name) != None:
                return True
            else:
                return False

        elif has_logs:
            unreal.log(has_file_name_suffix.__name__ + '(): suffix is empty')
    elif has_logs:
        unreal.log_error(has_file_name_suffix.__name__ + '(): file_name is empty. ' + file_name)

## @param file_name File name without extension, without path
def add_prefix_suffix_in_name(file_name,  prefix = '', suffix = ''):
    if file_name != '':
        if prefix != '' or suffix != '':
            new_name = file_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            if not has_file_name_prefix(new_name, prefix):
                new_name = prefix + new_name
            if not has_file_name_suffix(new_name, suffix):
                new_name = new_name + suffix

            return new_name
        else:
            unreal.log_error(add_prefix_suffix_in_name.__name__ + '(): prefix or suffix are empty. ' + file_name)
    else:
        unreal.log_error(add_prefix_suffix_in_name.__name__ + '(): file_name is empty')

def get_path_with_prefix_suffix(object_path,  prefix = '', suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            new_name = add_prefix_suffix_in_name(new_name, prefix, suffix)

            if new_name != origin_name:
                return get_asset.get_asset_path_with_new_name(object_path, new_name)
            else:
                return object_path

        else:
            unreal.log_error(get_path_with_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_with_prefix_suffix.__name__ + '(): object_path is empty')

## @param file_name File name without extension, without path
def delete_prefix_suffix_in_name(file_name,  prefix = '', suffix = ''):
    if file_name != '':
        if prefix != '' or suffix != '':
            new_name = file_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            if has_file_name_prefix(new_name, prefix):
                new_name = new_name[len(prefix) :]
            if has_file_name_suffix(new_name, suffix):
                new_name = new_name[: len(new_name) - len(suffix)]

            return new_name
        else:
            unreal.log_error(delete_prefix_suffix_in_name.__name__ + '(): prefix or suffix are empty. ' + file_name)
    else:
        unreal.log_error(delete_prefix_suffix_in_name.__name__ + '(): file_name is empty')

## Get name without prefix or suffix
def get_path_without_prefix_suffix(object_path,  prefix = '', suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            new_name = delete_prefix_suffix_in_name(new_name, prefix, suffix)

            if new_name != origin_name:
                return get_asset.get_asset_path_with_new_name(object_path, new_name)
            else:
                return object_path

        else:
            unreal.log_error(get_path_without_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_without_prefix_suffix.__name__ + '(): object_path is empty')



## Get path for replace_prefix_suffix() function
def get_path_replaced_by_prefix_suffix(object_path,  prefix = '', suffix = '',
                                       new_prefix = '', new_suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            new_name = delete_prefix_suffix_in_name(new_name, prefix, suffix)
            new_name = new_prefix + new_name + new_suffix
            return get_asset.get_asset_path_with_new_name(object_path, new_name)

        else:
            unreal.log_error(get_path_replaced_by_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_replaced_by_prefix_suffix.__name__ + '(): object_path is empty')

## Write to console what old and new file name
def log_rename_operation(old_path, new_path):
    unreal.log(general_ue.Name_to_str(old_path) + ' -> ' + general_ue.Name_to_str(new_path))

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def add_prefix_suffix(object_path, prefix = '', suffix = '', is_folder_operation = False,
                      include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            if (not has_restricted_chars_for_os(prefix)) and (not has_restricted_chars_for_os(suffix)):
                new_path = get_path_with_prefix_suffix(object_path, prefix, suffix)
                if new_path != object_path:
                    # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                    if not is_folder_operation:
                        with unreal.ScopedEditorTransaction(add_prefix_suffix.__name__) as ue_transaction:
                            general_ue.rename_asset(object_path, new_path)
                    else:
                        general_ue.rename_asset(object_path, new_path)

                else:
                    unreal.log(add_prefix_suffix.__name__ + '(): asset file already has prefix or suffix. ' + general_ue.Name_to_str(object_path))
            else:
                unreal.log_error(add_prefix_suffix.__name__ + '(): prefix or suffix has restricted chars')
        else:
            unreal.log_error(add_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(add_prefix_suffix.__name__ + '(): object_path is empty')

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def delete_prefix_suffix(object_path, prefix = '', suffix = '', is_folder_operation = False,
                         include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            new_path = get_path_without_prefix_suffix(object_path, prefix, suffix)
            if new_path != object_path:
                # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                if not is_folder_operation:
                    with unreal.ScopedEditorTransaction(delete_prefix_suffix.__name__) as ue_transaction:
                        general_ue.rename_asset(object_path, new_path)
                else:
                    general_ue.rename_asset(object_path, new_path)

            else:
                unreal.log(delete_prefix_suffix.__name__ + '(): asset file already has no prefix or suffix. ' + general_ue.Name_to_str(object_path))
        else:
            unreal.log_error(delete_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(delete_prefix_suffix.__name__ + '(): object_path is empty')

def delete_prefix_suffix_data(asset_data, prefix = '', suffix = '', is_folder_operation = False,
                         include_only_on_disk_assets = False):
    delete_prefix_suffix(asset_data.get_editor_property('object_path'), prefix, suffix, is_folder_operation,
                         include_only_on_disk_assets)

def delete_prefix_suffix_datas(assets_data, prefix = '', suffix = '', is_folder_operation = False,
                               include_only_on_disk_assets = False):
    for asset_data in assets_data:
        delete_prefix_suffix(asset_data.get_editor_property('object_path'), prefix, suffix, is_folder_operation,
                             include_only_on_disk_assets)

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def replace_prefix_suffix(object_path, prefix = '', suffix = '', new_prefix = '', new_suffix = '',
                          is_folder_operation = False, include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            if (not has_restricted_chars_for_os(prefix)) and (not has_restricted_chars_for_os(suffix)) and (
                not has_restricted_chars_for_os(new_prefix)) and (not has_restricted_chars_for_os(new_suffix)):

                new_path = get_path_replaced_by_prefix_suffix(object_path, prefix, suffix, new_prefix, new_suffix)
                if new_path != object_path:
                    # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                    if not is_folder_operation:
                        with unreal.ScopedEditorTransaction(replace_prefix_suffix.__name__) as ue_transaction:
                            general_ue.rename_asset(object_path, new_path)
                    else:
                        general_ue.rename_asset(object_path, new_path)

                else:
                    unreal.log(replace_prefix_suffix.__name__ + '(): asset file already has no prefix or suffix. ' + general_ue.Name_to_str(object_path))
            else:
                unreal.log_error(replace_prefix_suffix.__name__ + '(): prefix, suffix, new_prefix or new_suffix has restricted chars')
        else:
            unreal.log_error(replace_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(replace_prefix_suffix.__name__ + '(): object_path is empty')

def replace_prefix_suffix_assets_data(assets_data, prefix = '', suffix = '', new_prefix = '', new_suffix = ''):
    if general_ue.is_not_none_or_empty(assets_data):
        objects_paths = get_asset.get_objects_paths_from_assets_data(assets_data)
        for object_path in objects_paths:
            replace_prefix_suffix(object_path, prefix, suffix, new_prefix, new_suffix)
    else:
        unreal.log_error(replace_prefix_suffix_assets_data.__name__ + '(): assets_data must not be Empty or None')

def replace_prefix_suffix_asset_data(asset_data, prefix = '', suffix = '', new_prefix = '', new_suffix = ''):
    replace_prefix_suffix_assets_data([asset_data], prefix, suffix, new_prefix, new_suffix)


def add_prefix_suffix_dirs(folder_paths, prefix = '', suffix = '',
                             recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(add_prefix_suffix_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = add_prefix_suffix_dirs.__name__ + config.IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                add_prefix_suffix(object_path, prefix, suffix, True, include_only_on_disk_assets)

                slow_task.enter_progress_frame(1)


## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def delete_prefix_suffix_dirs(folder_paths, prefix = '', suffix = '',
                                recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(delete_prefix_suffix_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = delete_prefix_suffix_dirs.__name__ + config.IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                delete_prefix_suffix(object_path, prefix, suffix, True, include_only_on_disk_assets)

                slow_task.enter_progress_frame(1)

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def replace_prefix_suffix_dirs(folder_paths, prefix = '', suffix = '', new_prefix = '', new_suffix = '',
                                 recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(replace_prefix_suffix_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = replace_prefix_suffix_dirs.__name__ + config.IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                replace_prefix_suffix(object_path, prefix, suffix, new_prefix, new_suffix, True, include_only_on_disk_assets)

                slow_task.enter_progress_frame(1)


def delete_glb_texture_prefix(object_path):
    new_name = get_asset.get_asset_name_no_extension(object_path)
    # regex: ^\d+_
    match_object = re.search('^\\d+_', new_name)
    if match_object:
        new_name = new_name[len(match_object[0]) :]
        new_path = get_asset.get_asset_path_with_new_name(object_path, new_name)
        general_ue.rename_asset(object_path, new_path)
        return True
    else:
        unreal.log_error(delete_glb_texture_prefix.__name__ + '(): There is no glb texture prefix in: ' + general_ue.Name_to_str(object_path))
        return False

## delete indexes in names of imported glb textures
def delete_glb_texture_prefix_in_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
    unreal.log(delete_glb_texture_prefix_in_dirs.__name__ + ' Started')
    with unreal.ScopedEditorTransaction(delete_glb_texture_prefix_in_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(dir_paths, recursive, include_only_on_disk_assets)
        if general_ue.is_not_none_or_empty(assets_data):
            progress_bar_text = delete_glb_texture_prefix_in_dirs.__name__ + config.IS_WORKING_TEXT
            with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
                slow_task.make_dialog(True)

                for asset_data in assets_data:
                    if slow_task.should_cancel():
                        break
                    object_path = asset_data.get_editor_property('object_path')
                    delete_glb_texture_prefix(object_path)

                    slow_task.enter_progress_frame(1)

    unreal.log('_')

def delete_glb_texture_prefix_in_dir(dir_path, recursive = False, include_only_on_disk_assets = False):
    delete_glb_texture_prefix_in_dirs([dir_path], recursive, include_only_on_disk_assets)


## Reads prefix and suffix of texture asset and returns type of texture by convention
# Converts all text to lower case
def get_texture_type_by_prefix_suffix(object_path):
    prefix = get_asset_prefix_suffix_by_path(object_path)
    suffix = prefix[1]
    prefix = prefix[0]

    texture_types = convention.TextureTypesCustom
    texture_types_keys = list(convention.TextureTypesCustom.keys())
    is_type_found = False
    type_indx = 0
    key = ''
    while (not is_type_found) and type_indx < len(texture_types_keys):
        key = texture_types_keys[type_indx]
        if texture_types[key][0].casefold() == prefix.casefold():     # check prefix
            is_suffix_found = False
            suffix_indx = 0
            while (not is_suffix_found) and suffix_indx < len(texture_types[key][1]):
                if texture_types[key][1][suffix_indx].casefold() == suffix.casefold():    # check suffix in suffix list
                    is_type_found = True
                    is_suffix_found = True
                else:
                    suffix_indx +=1
        type_indx += 1

    if not is_type_found:
        key = NO_TEXTURE_TYPE
    return key

def get_texture_type_by_prefix_suffix_in_data(asset_data):
    object_path = asset_data.get_editor_property('object_path')
    return get_texture_type_by_prefix_suffix(object_path)


## Correct prefix by unreal engine asset type (Texture, Material, Static Mesh).
# Adds prefix, if there is no prefix
def correct_prefix_by_uclass(object_path, asset_data = None,
                          include_only_on_disk_assets = False):
    if asset_data == None:
        asset_data = get_asset.get_asset_data_by_object_path(object_path, include_only_on_disk_assets)

    if asset_data != None:
        asset_class = general_ue.Name_to_str(asset_data.get_editor_property('asset_class'))
        prefix_for_class = convention.AssetsPrefixConventionTable[asset_class]
        #unreal.log('prefix_for_class');   unreal.log(prefix_for_class)
        if prefix_for_class != None and prefix_for_class != '':
            # If function was called by correct_prefix_by_uclass_dirs, it has one transaction with all assets in folder
            with unreal.ScopedEditorTransaction(correct_prefix_by_uclass.__name__) as ue_transaction:
                add_prefix_suffix(object_path, prefix = prefix_for_class, is_folder_operation = False,
                                    include_only_on_disk_assets = include_only_on_disk_assets)

        else:
            unreal.log_error(correct_prefix_by_uclass.__name__ + '(): Did not find prefix for asset class - ' + asset_class)
    else:
        unreal.log_error(correct_prefix_by_uclass.__name__ + '(): Did not find asset_data from object_path')

## Correct prefix by unreal engine asset type (Texture, Material, Static Mesh).
# Adds prefix, if there is no prefix
def correct_prefix_by_uclass_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(correct_prefix_by_uclass_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(dir_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = correct_prefix_by_uclass_dirs.__name__ + config.IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                correct_prefix_by_uclass(object_path, asset_data, include_only_on_disk_assets)

                slow_task.enter_progress_frame(1)


## Rename texture asset suffix to default variation.
# Default variation is zero in list of TextureTypesCustom suffixes
# F.e. From _BaseColor to _Diff
def standardize_texture_suffix_asset_data(texture_asset_data):
    if texture_asset_data is not None:
        texture_type = get_texture_type_by_prefix_suffix_in_data(texture_asset_data)
        if texture_type != NO_TEXTURE_TYPE:
            texture_name_no_extension = get_asset.get_asset_name_no_extension_in_data_asset(texture_asset_data)
            prefix, suffix = get_asset_prefix_suffix_by_name(texture_name_no_extension)
            standard_suffix = convention.get_TextureTypesCustom_standard_suffix(texture_type)
            if suffix != standard_suffix:
                replace_prefix_suffix_asset_data(texture_asset_data, prefix = '', suffix = suffix,
                                                 new_prefix = '', new_suffix = standard_suffix)
        else:
            unreal.log_error(standardize_texture_suffix_asset_data.__name__ + '(): did not find texture type')
    else:
        unreal.log_error(standardize_texture_suffix_asset_data.__name__ + '(): no asset_data in input')

## Rename texture asset suffix to default variation.
# Default variation is zero in list of TextureTypesCustom suffixes
# F.e. From _BaseColor to _Diff
def standardize_texture_suffix_assets_data(textures_assets_data):
    if general_ue.is_not_none_or_empty(textures_assets_data):
        progress_bar_text = standardize_texture_suffix_assets_data.__name__ + config.IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(textures_assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in textures_assets_data:
                if slow_task.should_cancel():
                    break
                standardize_texture_suffix_asset_data(asset_data)

                slow_task.enter_progress_frame(1)
    else:
        unreal.log(standardize_texture_suffix_assets_data.__name__ + '(): no assets_data in input')

## Rename texture asset suffix to default variation.
# Default variation is zero in list of TextureTypesCustom suffixes
# F.e. From _BaseColor to _Diff
def standardize_texture_suffix_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
     with unreal.ScopedEditorTransaction(correct_prefix_by_uclass_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_textures_data_by_dirs(dir_paths, recursive, include_only_on_disk_assets)
        standardize_texture_suffix_assets_data(assets_data)

def correct_n_standardize_texture_suffix_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
    correct_prefix_by_uclass_dirs(dir_paths, recursive, include_only_on_disk_assets)
    standardize_texture_suffix_dirs(dir_paths, recursive, include_only_on_disk_assets)