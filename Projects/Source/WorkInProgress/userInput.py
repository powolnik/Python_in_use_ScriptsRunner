import unreal

def get_user_input():
  """Prompts the user for input in UE5"""

  # Get the editor subsystem
  editor_subsystem = unreal.EditorUtilityLibrary()

  # Prompt the user for input
  user_input = editor_subsystem.get_editor_user_settings().get_string("MyInput", "Default")

  # Print the user input
  print("User entered:", user_input)

  return user_input

test = get_user_input()
print (test)