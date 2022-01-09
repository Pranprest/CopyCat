"""
    This script records your mouse and keyboard input for later re-doing them
    -> When you click, it records where you clicked and when you clicked
    -> After recording, you can replay everything that you did during the recording
    -> Its like a TAS thing but for general use I guess?

    ==
        Author: Pranprest
    ==
"""

# TODO: get this working, then try it with the mouse controller, then push it to "main.py"

from pynput import keyboard
import time
# from enum import Enum
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename="log\\logfile_keyboard_test.log", format='%(levelname)s: %(message)s')


def recordInput() -> list[list[tuple, enumerate], keyboard.Key]:
    """
        Records your mouse and keyboard input!
    """
    initial_time = time.time()
    user_input = []

    def on_press(key):
        elapsed_time = round(time.time() - initial_time, 2)
        user_input.append((key, elapsed_time))
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return user_input


def replayKeyboard(InputList: list) -> None:
    keyboard_controller = keyboard.Controller()
    for i in range(len(InputList)):  # Tuple w/ input and time
        key, currtime = InputList[i]
        if (InputList[i - 1] != InputList[-1]):
            # Sleep X ammount of time (interval between last input and current one)
            time.sleep(currtime - InputList[i - 1][1])
        keyboard_controller.press(key)
        keyboard_controller.release(key)


def main() -> None:
    try:
        user_input = recordInput()
        logging.debug(user_input)
        time.sleep(1)
        replayKeyboard(user_input)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
