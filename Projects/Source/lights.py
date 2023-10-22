import unreal
from enum import Enum

class MobilityType(Enum):
    STATIC = unreal.ComponentMobility.STATIC
    STATIONARY = unreal.ComponentMobility.STATIONARY
    MOVABLE = unreal.ComponentMobility.MOVABLE

class LightAnalyzer:
    def __init__(self, editor_actor_subsystem):
        self.editor_actor_subsystem = editor_actor_subsystem
        self.spot_lights = []
        self.point_lights = []
        self.rect_lights = []

    def get_all_components(self):
        all_components = self.editor_actor_subsystem.get_all_level_actors_components()
        for component in all_components:
            class_name = component.get_class().get_name()
            if class_name == 'PointLightComponent':
                self.point_lights.append(component)
            elif class_name == 'SpotLightComponent':
                self.spot_lights.append(component)
            elif class_name == 'RectLightComponent':
                self.rect_lights.append(component)

    def analyze_lights(self, light_type):
        static_lights = []
        stationary_lights = []
        movable_lights = []
        light_list = self.spot_lights if light_type == 'Spot' else self.point_lights if light_type == 'Point' else self.rect_lights
        for light in light_list:
            if light.mobility == MobilityType.STATIC:
                static_lights.append(light)
            elif light.mobility == MobilityType.STATIONARY:
                stationary_lights.append(light)
            elif light.mobility == MobilityType.MOVABLE:
                movable_lights.append(light)
        return {
            'Static': len(static_lights),
            'Stationary': len(stationary_lights),
            'Movable': len(movable_lights)
        }

    def select_lights(self, light_type):
        selection = []
        light_list = self.spot_lights if light_type == 'Spot' else self.point_lights if light_type == 'Point' else self.rect_lights
        for light in light_list:
            selection.append(light.get_owner())
        self.editor_actor_subsystem.set_selected_level_actors(selection)

# Initialize the LightAnalyzer
editor_actor_subsystem = unreal.EditorActorSubsystem()
light_analyzer = LightAnalyzer(editor_actor_subsystem)

# Get all components
light_analyzer.get_all_components()

# Analyze and select point lights
point_analysis = light_analyzer.analyze_lights('Point')
light_analyzer.select_lights('Point')

# Analyze and select spot lights
spot_analysis = light_analyzer.analyze_lights('Spot')
light_analyzer.select_lights('Spot')

# Analyze and select rect lights
rect_analysis = light_analyzer.analyze_lights('Rect')
light_analyzer.select_lights('Rect')

print("Point Lights Analysis:", point_analysis)
print("Spot Lights Analysis:", spot_analysis)
print("Rect Lights Analysis:", rect_analysis)
