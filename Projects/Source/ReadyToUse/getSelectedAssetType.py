import unreal

selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
for asset in selected_assets:
    name = asset.get_class().get_name()
    print("Asset: ", name)