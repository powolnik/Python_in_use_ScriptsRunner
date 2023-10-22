import unreal

def getStaticMeshInstanceCount():
  levelActors = unreal.EditorActorSubsystem().get_all_level_actors()

  SMActors = []
  SMActorCounts = []

  for actor in levelActors:
    if (actor.get_class().get_name()) == 'StaticMeshActor':
      SMComponent = actor.static_mesh_component
      SM = SMComponent.static_mesh
      if SM != None:
        SMActors.append(SM.get_name())

  processedActors = []
  for SMActor in SMActors:
    if SMActor not in processedActors and SMActors.count(SMActor) > 50:

      actorCounts = (SMActors.count(SMActor), SMActor)
      SMActorCounts.append(actorCounts)
      processedActors.append(SMActor)
  print (len(SMActorCounts))
  for item in SMActorCounts:
    print(item)