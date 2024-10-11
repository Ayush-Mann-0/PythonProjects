from pynput import keyboard, mouse
import time

class Record:
    def __init__(self):
        self.key_pressed = None
        self.recorded_keys = []
        self.recording = False

    def start_recording(self):
        self.recording = True
        print("Recording Started. Press 'esc' to stop.")

        # Start the keyboard and mouse listeners without blocking
        with keyboard.Listener(on_press=self._keyboard_listener) as keyboard_listener, \
            mouse.Listener(on_click=self._mouse_listener) as mouse_listener:
            keyboard_listener.join()  # This will block the program until ESC is pressed to stop recording.

    def stop_recording(self):
        self.recording = False
        print("Recording Stopped")
        print("Recorded Keys: ", self.recorded_keys)

    def _keyboard_listener(self, key):
        if not self.recording:
            return

        if key == keyboard.Key.esc:
            self.stop_recording()
            return False  # Stop listener

        try:
            self.recorded_keys.append(('key', key.char, time.time()))
            print(f"Key Pressed - {key.char}")
        except AttributeError:
            self.recorded_keys.append(('key', str(key), time.time()))
            print(f"Key Pressed - {key}")

    def _mouse_listener(self, x, y, button, pressed):
        if not self.recording:
            return

        if pressed:
            self.recorded_keys.append(('mouse', x, y, str(button), time.time()))
            print(f"Mouse Clicked - {button} at ({x}, {y})")


class Play:
    def __init__(self, recorded_keys):
        self.recorded_keys = recorded_keys
        self.key_pressed = None
        self.playing = False

    def play(self):
        self.playing = True
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        print("Playing Recorded Keys. Press 'esc' to stop.")
        for event in self.recorded_keys:
            event_type = event[0]

            if event_type == 'key':
                _, key, _ = event
                if key == 'Key.esc':
                    break
                try:
                    keyboard_controller.press(key)
                    keyboard_controller.release(key)
                except:
                    pass
            elif event_type == 'mouse':
                _, x, y, button, _ = event
                mouse_button = getattr(mouse.Button, button.split('.')[1])  # Convert button string to mouse.Button
                mouse_controller.position = (x, y)
                mouse_controller.press(mouse_button)
                mouse_controller.release(mouse_button)


def main():
    record = Record()
    record.start_recording()

    print(f"Recording complete. Starting playback in 2 seconds...")
    time.sleep(2)

    play = Play(record.recorded_keys)
    play.play()

if __name__ == '__main__':
    main()
