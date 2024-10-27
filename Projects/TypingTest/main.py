import time
import random

# Sample phrases for typing test
phrases = [
    "Python is an interpreted, high-level programming language.",
    "It is widely used for web development, data analysis, and machine learning.",
    "The language's design philosophy emphasizes code readability.",
    "Python supports multiple programming paradigms.",
    "It has a large standard library and an active community."
]

border = '-+-' * 10

def create_box(phrase):
    print(border)
    print()
    print('Type the following phrase as fast as possible and with accuracy:')
    print()
    print(phrase)
    print()

def main():
    while True:
        # Randomly select a phrase for the typing test
        selected_phrase = random.choice(phrases)
        
        # Display the box with the selected phrase
        create_box(selected_phrase)

        # Wait for the user to press Enter before starting the timer
        input("Press Enter to start the timer...")
        t0 = time.time()
        
        # Get user input
        input_text = input("Start typing: ")
        t1 = time.time()

        # Calculate results
        length_of_input = len(input_text.split())
        accuracy = len(set(input_text.split()) & set(selected_phrase.split())) / len(selected_phrase.split())
        time_taken = t1 - t0
        words_per_minute = (length_of_input / time_taken) * 60 if time_taken > 0 else 0
        
        # Show results
        print(border)
        print('Total words       :', length_of_input)
        print('Time used         :', round(time_taken, 2), 'seconds')
        print('Your accuracy     :', round(accuracy, 3) * 100, '%')
        print('Speed is          :', round(words_per_minute, 2), 'words per minute')
        print(border)
        
        # Retry prompt
        retry = input("Do you want to retry? (yes/no): ").strip().lower()
        if retry != 'yes' or retry != "y":
            print('Thank you, goodbye!')
            time.sleep(1.5)
            break

if __name__ == "__main__":
    main()
