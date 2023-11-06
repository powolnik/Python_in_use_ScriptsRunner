import unreal

editor_actor_subsystem = unreal.EditorActorSubsystem()
hisms = []

def get_all_components():
    all_components = editor_actor_subsystem.get_all_level_actors_components()
    print(len(all_components))
    substring = "HISM"

    for component in all_components:
        name = component.get_class().get_name()
        if (name == "HierarchicalInstancedStaticMeshComponent"):
            hisms.append(component)

    return 0
get_all_components()
print (len(hisms))

HISM = unreal.HierarchicalInstancedStaticMeshComponent
HISM.