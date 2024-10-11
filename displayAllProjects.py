import os
import importlib.util
import subprocess

# Set the path to the "Projects" folder
projects_path = os.path.join(os.getcwd(), "Projects")
projects = os.listdir(projects_path)

# Display list of projects
for idx, project in enumerate(projects, start=1):
    print(f"{idx}: {project}")

# Get user input for project selection
projectSearch = input("Enter Project Number: ")
print("\n\n")

# Try to parse the input and check validity
try:
    projectIndex = int(projectSearch) - 1
    if projectIndex < 0 or projectIndex >= len(projects):
        raise ValueError("Index out of range.")
except ValueError:
    print("Not a Valid Input, Try Again...")
    exit()

# Select the chosen project
selected_project = os.path.join(projects_path, projects[projectIndex])

# Find the 'main' Python file in the project directory
found = False
main_file_path = None
for root, _, files in os.walk(selected_project):
    for file in files:
        if file.endswith(".py") and "main" in file:
            found = True
            main_file_path = os.path.join(root, file)
            break
    if found:
        break

# If 'main' Python file is found, continue
if found and main_file_path:
    module_name = os.path.splitext(os.path.basename(main_file_path))[0]

    # Check for the existence of 'requirements.txt' in the same folder
    requirements_path = os.path.join(os.path.dirname(main_file_path), "requirements.txt")
    if os.path.exists(requirements_path):
        print(f"Installing requirements from {requirements_path}...")
        subprocess.run(["pip", "install", "-r", requirements_path])

    # Load the main Python file as a module and execute it
    spec = importlib.util.spec_from_file_location(module_name, main_file_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)

    # Check if the 'main' function exists in the module and run it
    if hasattr(main_module, 'main'):
        ProjectMain = main_module.main
        ProjectMain()
    else:
        print("No 'main' function found in the specified file.")
else:
    print("No Python file with 'main' in the name was found.")
