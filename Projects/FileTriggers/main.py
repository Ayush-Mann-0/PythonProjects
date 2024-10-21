def detectTrigger(trig, file):
    lines = fileReader(file)
    for line in lines:
        for t in trig:
            if t == line:
                return True
            else:
                continue
    
    return False


def fileReader(file):
    with open(file) as f:
        return f.read().split("\n")

def example():
    triggers = []

    filePath = input("Enter File Path: ")
    
    while True:
        t = input("Enter Trigger ( Press Enter to complete ): ")
        if t == "":
            break
        else:
            triggers.append(t)
    
    print(detectTrigger(triggers, filePath))

def main():
    example()

main()
