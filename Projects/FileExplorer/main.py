import os

def selectDir(path):
    try:
        selectedDirIndex = int(input("Enter which Directory you want to Open (negative to go up): ")) - 1
        
        if selectedDirIndex < 0:
            path = os.path.abspath(os.path.join(path, "../" * abs(selectedDirIndex)))
        else:
            items = os.listdir(path)
            if 0 <= selectedDirIndex < len(items):
                selected_item = os.path.join(path, items[selectedDirIndex])
                if os.path.isdir(selected_item):
                    path = selected_item
                else:
                    print(f"{items[selectedDirIndex]} is not a directory.")
            else:
                print("Invalid selection.")
        return path
    except (ValueError, IndexError) as e:
        print(f"Error: {e}. Please enter a valid number.")
        return False

def showDirItems(path):
    while True:
        items = os.listdir(path)
        print(f"\nCurrent Directory: {path}\n")
        
        for i, item in enumerate(items):
            print(f"{i + 1}: {item}")

        path = selectDir(path)
        if path is False:
            break

def example():
    defaultPath = os.getcwd()
    showDirItems(defaultPath)

def main():
    example()

main()
