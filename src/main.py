"""
    This script records your mouse and keyboard input for later re-doing them
    -> When you click, it records where you clicked and when you clicked
    -> After recording, you can replay everything that you did during it
    -> Its like a TAS thing but for general use I guess?

    ==
        Author: Pranprest
    ==
"""
import logging
from collections import namedtuple
from time import sleep, time
from pynput import keyboard, mouse

logging.basicConfig(
    level=logging.DEBUG, filename="log\\logfile.log", format="%(levelname)s:%(message)s"
)


def recordInput() -> tuple:
    """
    Records your mouse and keyboard input!
    """
    initial_time = time()

    Point = namedtuple("Point", "x y")
    MouseInput = namedtuple("MouseInput", "time button pos")
    KeyboardInput = namedtuple("KeyboardInput", "time button")

    MouseList = []
    KeyboardList = []

    def on_click(x, y, button, pressed):
        if not pressed:
            return
        elapsed_time = round(time() - initial_time, 2)
        MouseList.append(MouseInput(
            pos=Point(x, y), button=button, time=elapsed_time))

    def on_press(key):
        if key == keyboard.Key.esc:
            mouse_listener.stop()
            return False
        elapsed_time = round(time() - initial_time, 2)
        KeyboardList.append(KeyboardInput(button=key, time=elapsed_time))

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Making sure any of the listeners will continue running after this.
    mouse_listener.stop()
    listener.stop()

    return MouseList, KeyboardList


def replayMouse(InputList: list) -> None:
    print("Replaying mouse input...")
    mouse_controller = mouse.Controller()
    for index, curr_input in enumerate(InputList):
        pos, key, curr_time = curr_input
        if InputList[index - 1] != InputList[-1]:
            sleep(curr_time - InputList[index - 1][0])
        mouse_controller.position = pos
        mouse_controller.press(key)
        mouse_controller.release(key)
    return


def replayKeyboard(InputList: list[tuple]) -> None:
    print("Replaying keyboard input...")
    keyboard_controller = keyboard.Controller()
    for index, curr_input in enumerate(InputList):  # Tuple w/ input and time
        curr_time, key = curr_input
        if InputList[index - 1] != InputList[-1]:
            # Sleep for the ammount of time of the interval between last input and current one
            sleep(curr_time - InputList[index - 1][0])
        # TODO: Somehow figure out a way to support any other kind of key other than regular ASCII
        keyboard_controller.press(key)
        keyboard_controller.release(key)
    return


def replayFull(MouseList: list, KeyboardList: list) -> None:
    if not KeyboardList:
        replayMouse(MouseList)
        exit()
    if not MouseList:
        replayKeyboard(KeyboardList)
        exit()

    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    sorted_full_list = sorted(
        [*MouseList, *KeyboardList], key=lambda tup: tup[0])

    for index, curr_input in enumerate(sorted_full_list):
        curr_time = curr_input[0]
        if sorted_full_list[index - 1] != sorted_full_list[-1]:
            sleep(curr_time - sorted_full_list[index - 1][0])
        # FIXME: I can't check directly if the namedtuple is either KeyboardInput or MouseInput
        # FIXME: Really bad readability here.
        if len(curr_input) <= 2:
            keyboard_controller.press(curr_input[1])
            keyboard_controller.release(curr_input[1])
        else:
            mouse_controller.position = curr_input[2]
            mouse_controller.press(curr_input[1])
            mouse_controller.release(curr_input[1])


def main() -> None:
    try:
        mouselist, keyboardlist = recordInput()
        logging.debug(f"{mouselist}, {keyboardlist}")
        replayFull(MouseList=mouselist, KeyboardList=keyboardlist)
        print("Script ran successfully!")
    except Exception as e:
        print("An error ocourred during runtime, check logfiles for more information.")
        logging.error(e)


if __name__ == "__main__":
    main()
