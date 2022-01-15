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
import pickle
import os
from collections import namedtuple
from time import sleep, time
from pynput import keyboard, mouse
from pathlib import Path

currosslash = "\\" if (os.name == "nt") else "/"
currfilepath = f"{Path(__file__).parent.absolute()}{currosslash}"
logging.basicConfig(
    level=logging.DEBUG, filename=f"{currfilepath}logfile.log", format="%(levelname)s:%(message)s"
)
del currosslash

# Global namedtuples so that I can pickle them!
Point = namedtuple("Point", "x y")
MouseInput = namedtuple("MouseInput", "time button pos")
KeyboardInput = namedtuple("KeyboardInput", "time button")


def recordInput() -> tuple:
    """
    Records your mouse and keyboard input!
    """
    initial_time = time()

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


def replayInput(MouseList: list, KeyboardList: list) -> None:
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    sorted_full_list = sorted(
        [*MouseList, *KeyboardList], key=lambda tup: tup[0])

    for index, curr_input in enumerate(sorted_full_list):
        curr_time = curr_input[0]
        if sorted_full_list[index - 1] != sorted_full_list[-1]:
            sleep(curr_time - sorted_full_list[index - 1][0])
        # FIXME: I can't check directly if the namedtuple is either KeyboardInput or MouseInput
        try:
            if len(curr_input) <= 2:
                keyboard_controller.press(curr_input[1])
                keyboard_controller.release(curr_input[1])
            else:
                mouse_controller.position = curr_input[2]
                mouse_controller.press(curr_input[1])
                mouse_controller.release(curr_input[1])
        except Exception as e:
            print("Invalid or unsupported input, check logfile for more information")
            logging.error(e)


def importInputs(file_path: Path) -> tuple:
    try:
        with open(f'{file_path}', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print("Error when reading pickle file, is it really a pickle? If so, read logfile for more information.\n")
        logging.error(e)
        exit()


def exportInputs(InputList: tuple) -> None:
    try:
        with open(f"{currfilepath}exportCopyCat-{time()}.pkl", "wb") as f:
            pickle.dump(InputList, f)
    except IOError as e:
        print("Error while writing pickle, check logfile for more information.\n")
        logging.error(e)
        exit()


def main() -> None:
    from pick import pick
    ans_index = pick(
        ["Record mouse and keyboard input", "Get input from file", "Exit program"], "What would you like to do?")[1]

    if ans_index == 0:
        print("Recording inputs, press ESC to stop recording...")
        try:
            mouselist, keyboardlist = recordInput()
        except Exception as e:
            print(
                "An error ocourred during runtime, check logfiles for more information.")
            logging.error(e)
            exit()
        logging.debug(
            f"Mouse Input:{mouselist}\n Keyboard Input:{keyboardlist}")
        answ2_index = pick(
            ["Export your inputs", "Replay inputs right now"], "Would you like to:")[1]
        if (answ2_index == 0):
            exportInputs((mouselist, keyboardlist))
        else:
            replayInput(
                MouseList=mouselist, KeyboardList=keyboardlist)

    if ans_index == 1:
        mouselist, keyboardlist = importInputs(
            input("Paste here the file's full absolute path: "))
        answer = input(
            'Would you like to replay them right now? [y/n] ')
        if answer[0].lower() != 'y':
            exit()
        replayInput(MouseList=mouselist, KeyboardList=keyboardlist)


if __name__ == "__main__":
    main()
