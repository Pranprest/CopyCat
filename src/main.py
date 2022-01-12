"""
    This script records your mouse and keyboard input for later re-doing them
    -> When you click, it records where you clicked and when you clicked
    -> After recording, you can replay everything that you did during it
    -> Its like a TAS thing but for general use I guess?

    ==
        Author: Pranprest
    ==
"""
from collections import namedtuple
from typing import List
from pynput import mouse, keyboard
from time import sleep, time
import logging

import pynput

logging.basicConfig(
    level=logging.DEBUG, filename="log\\logfile.log", format="%(levelname)s:%(message)s"
)


def recordInput() -> tuple:
    """
    Records your mouse and keyboard input!
    """
    initial_time = time()

    Point = namedtuple("Point", "x y")
    MouseInput = namedtuple("MouseInput", "pos button time")
    KeyboardInput = namedtuple("KeyboardInput", "button time")

    MouseList = []
    KeyboardList = []

    def on_click(x, y, button, pressed):
        if not pressed:
            return
        elapsed_time = round(time() - initial_time, 2)
        MouseList.append(MouseInput(
            pos=Point(x, y), button=button, time=elapsed_time))
        print(MouseInput(
            pos=Point(x, y), button=button, time=elapsed_time))

    def on_press(key):
        if key == keyboard.Key.esc:
            mouse_listener.stop()
            return False
        elapsed_time = round(time() - initial_time, 2)
        KeyboardList.append(KeyboardInput(key=key, time=elapsed_time))

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return MouseList, KeyboardList


def replayMouse(InputList: list) -> None:
    print("Replaying mouse input...")
    mouse_controller = mouse.Controller()
    for index, curr_input in enumerate(InputList):
        pos, key, curr_time = curr_input
        if InputList[index - 1] != InputList[-1]:
            sleep(curr_time - InputList[index - 1][2])
        mouse_controller.position = pos
        mouse_controller.press(key)
        mouse_controller.release(key)
    return


def replayKeyboard(InputList: list[tuple]) -> None:
    print("Replaying keyboard input...")
    keyboard_controller = keyboard.Controller()
    for index, curr_input in enumerate(InputList):  # Tuple w/ input and time
        key, curr_time = curr_input
        if InputList[index - 1] != InputList[-1]:
            # Sleep for the ammount of time of the interval between last input and current one
            sleep(curr_time - InputList[index - 1][2])
        # TODO: Somehow figure out a way to support any other kind of key other than regular ASCII
        try:
            keyboard_controller.press(key)
            keyboard_controller.release(key)
        except Exception as e:
            print("Unsupported key was pressed, check logfiles for more information")
            logging.error(e)
            exit()
    return


def main() -> None:
    try:
        mouselist, keyboardlist = recordInput()
        logging.debug(f"{mouselist}, {keyboardlist}")
        replayMouse(mouselist)
        # replayKeyboard(keyboardlist)
    except Exception as e:
        print("An error ocourred during runtime, check logfiles for more information.")
        logging.error(e)


if __name__ == "__main__":
    main()
