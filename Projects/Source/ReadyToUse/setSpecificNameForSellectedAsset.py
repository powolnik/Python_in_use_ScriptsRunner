import unreal

selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
if len(selected_assets) > 0:
  selected_asset = selected_assets[0]
else:
  print("No asset selected!")
  quit()

new_name = "WBP_QuestDisplay" 

unreal.EditorUtilityLibrary.rename_asset(asset=selected_asset, new_name=new_name)

print("Asset renamed to:", new_name)