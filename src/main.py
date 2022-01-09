"""
    This script records your mouse and keyboard input for later re-doing them
    -> When you click, it records where you clicked and when you clicked
    -> After recording, you can replay everything that you did during the recording
    -> Its like a TAS thing but for general use I guess?

    ==
        Author: Pranprest
    ==
"""

# WARNING: THIS FILE IS NOT FUNCITIONAL YET, IM TESTING IT

from pynput import mouse, keyboard
from time import sleep
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename="logfile.log", format='%(levelname)s:%(message)s')


def recordInput() -> list[list[tuple, enumerate], keyboard.Key]:
    """
        Records your mouse and keyboard input!
    """
    user_input = []

    def on_click(x, y, button, pressed):
        user_input.append([(x, y), button])
        if pressed == keyboard.Key.esc:
            return False

    def on_press(key):
        user_input.append([key])
        if key == keyboard.Key.esc:
            return False

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return user_input

# Doesn't work yet!!
# def replayMouse(mouseInput: list) -> None:
#     for section in mouseInput:
#         for element in section:
#             if isinstance(element, tuple):
#                 logging.debug(f"{element}, Is a Tuple")
#             elif isinstance(element, Enum):
#                 logging.debug(f"{element}, Is a Enum Object")
#             break


def replayKeyboard(InputList: list) -> None:
    keyboard_controller = keyboard.Controller()
    for i in range(len(InputList)):  # Tuple w/ input and time
        key, currtime = InputList[i]
        if (InputList[i - 1] != InputList[-1]):
            # Sleep X ammount of time (interval between last input and current one)
            sleep(currtime - InputList[i - 1][1])
        keyboard_controller.press(key)
        keyboard_controller.release(key)


def main() -> None:
    try:
        user_input = recordInput()
        logging.debug(user_input)
        sleep(1)
        replayKeyboard(user_input)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
