import os
import importlib.util

projects_path = os.path.join(os.getcwd(), "Projects")
projects = os.listdir(projects_path)

for idx, project in enumerate(projects, start=1):
    print(f"{idx}: {project}")

projectSearch = input("Enter Project Number: ")
print("\n\n")

try:
    projectIndex = int(projectSearch) - 1
    if projectIndex < 0 or projectIndex >= len(projects):
        raise ValueError("Index out of range.")
except ValueError:
    print("Not a Valid Input, Try Again...")
    exit()

selected_project = os.path.join(projects_path, projects[projectIndex])

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

if found and main_file_path:
    module_name = os.path.splitext(os.path.basename(main_file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, main_file_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)

    if hasattr(main_module, 'main'):
        ProjectMain = main_module.main
        ProjectMain()
    else:
        print("No 'Main' found in the specified file.")
else:
    print("No Python file with 'main' in the name was found.")
