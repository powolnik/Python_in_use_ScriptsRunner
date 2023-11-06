import unreal

workingPath = "/Game/"

@unreal.uclass()
class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
    pass

editorAssetLib = GetEditorAssetLibrary();

allAssets = editorAssetLib.list_assets(workingPath, True, False)
notUsedAssets = []

if (len(allAssets) > 0):
    for asset in allAssets:
        deps = editorAssetLib.find_package_referencers_for_asset(asset, False)
        if (len(deps) == 0):
            print (">>>%s" % asset)
            notUsedAssets.append(asset)

print (len(notUsedAssets))