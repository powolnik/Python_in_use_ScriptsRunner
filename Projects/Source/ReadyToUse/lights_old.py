import unreal

editor_actor_subsystem = unreal.EditorActorSubsystem()
spot_lights = []
point_lights = []
rect_lights = []
selection = []



def debug():
    all_components = editor_actor_subsystem.get_all_level_actors_components()
    print(len(all_components))


def get_all_components():
    all_components = editor_actor_subsystem.get_all_level_actors_components()
    for component in all_components:

        if (component.get_class().get_name()) == 'PointLightComponent':
            point_lights.append(component)


        if (component.get_class().get_name()) == 'SpotLightComponent':
            spot_lights.append(component)

        if (component.get_class().get_name()) == 'RectLightComponent':
            rect_lights.append(component)



get_all_components()


def analyze_spot_lights():
    static_spot_lights = []
    stationary_spot_lights = []
    movable_spot_lights = []
    for spot_light in spot_lights:
        if spot_light.mobility == unreal.ComponentMobility.STATIC:
            static_spot_lights.append(spot_light)
        elif spot_light.mobility == unreal.ComponentMobility.STATIONARY:
            stationary_spot_lights.append(spot_light)
        elif spot_light.mobility == unreal.ComponentMobility.MOVABLE:
            movable_spot_lights.append(spot_light)
    result = ('\n\nSpotLights: ' + str(len(spot_lights)) +
              '\nSTATIC spotLights: ' + str(len(static_spot_lights)) +
              '\nSTATIONARY spotLights: ' + str(len(stationary_spot_lights)) +
              '\nMOVABLE spotLights: ' + str(len(movable_spot_lights)))
    return result


spots = '\n' + analyze_spot_lights()
print(spots)


def analyze_point_lights():
    static_point_lights = []
    stationary_point_lights = []
    movable_point_lights = []
    for point_light in point_lights:
        if point_light.mobility == unreal.ComponentMobility.STATIC:
            static_point_lights.append(point_light)
        elif point_light.mobility == unreal.ComponentMobility.STATIONARY:
            stationary_point_lights.append(point_light)
        elif point_light.mobility == unreal.ComponentMobility.MOVABLE:
            movable_point_lights.append(point_light)
    result = ('\n\nPointLights: ' + str(len(point_lights)) +
              '\nSTATIC pointLights: ' + str(len(static_point_lights)) +
              '\nSTATIONARY pointLights: ' + str(len(stationary_point_lights)) +
              '\nMOVABLE pointLights: ' + str(len(movable_point_lights)))
    return result


points = analyze_point_lights()
print(points)


def analyze_rect_lights():
    static_rect_lights = []
    stationary_rect_lights = []
    movable_rect_lights = []
    for rect_light in rect_lights:
        if rect_light.mobility == unreal.ComponentMobility.STATIC:
            static_rect_lights.append(rect_light)
        elif rect_light.mobility == unreal.ComponentMobility.STATIONARY:
            stationary_rect_lights.append(rect_light)
        elif rect_light.mobility == unreal.ComponentMobility.MOVABLE:
            movable_rect_lights.append(rect_light)
    result = ('\n\nRectLights: ' + str(len(rect_lights)) +
              '\nSTATIC rectLights: ' + str(len(static_rect_lights)) +
              '\nSTATIONARY rectLights: ' + str(len(stationary_rect_lights)) +
              '\nMOVABLE rectLights: ' + str(len(movable_rect_lights)))
    return result


rects = analyze_rect_lights()
print(rects)

def select_lights(lightType):
    selection = []
    if lightType == 'Spot':
        for spot_light in spot_lights:
            selection.append(spot_light.get_owner())
        editor_actor_subsystem.set_selected_level_actors(selection)

    elif lightType == 'Point':
        for point_light in point_lights:
            selection.append(point_light.get_owner())
        editor_actor_subsystem.set_selected_level_actors(selection)

    elif lightType == 'Rect':
        for rect_light in rect_lights:
            selection.append(rect_light.get_owner())
        editor_actor_subsystem.set_selected_level_actors(selection)

    else:
        print("Invalid light type")
        selection = []
        editor_actor_subsystem.clear_actor_selection_set()

select_lights('Spot')