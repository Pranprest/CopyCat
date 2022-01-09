"""
    This script records your mouse and keyboard input for later re-doing them
    -> When you click, it records where you clicked and when you clicked
    -> After recording, you can replay everything that you did during the recording
    -> Its like a TAS thing but for general use I guess?

    ==
        Author: Pranprest
    ==
"""
from pynput import mouse, keyboard
from time import sleep, time
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename="..\\log\\logfile.log", format='%(levelname)s:%(message)s')


def recordInput() -> dict[list, list, list]:
    """
        Records your mouse and keyboard input!
    """
    initial_time = time()

    user_input = {
        "keyboard": [],
        "mouse": [],
        # TODO: Implement event timeline
        # "event_timeline": []
    }

    def on_click(x, y, button, pressed):
        elapsed_time = round(time() - initial_time, 2)
        user_input["mouse"].append([(x, y), button, elapsed_time])
        if pressed == keyboard.Key.esc:
            return False

    def on_press(key):
        elapsed_time = round(time() - initial_time, 2)
        user_input["keyboard"].append((key, elapsed_time))
        if key == keyboard.Key.esc:
            return False

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return user_input


def replayMouse(InputList: list) -> None:
    print("Replaying mouse input...")
    raise NotImplementedError()


def replayKeyboard(InputList: list[tuple]) -> None:
    print("Replaying keyboard input...")
    keyboard_controller = keyboard.Controller()
    for i in range(len(InputList)):  # Tuple w/ input and time
        key, currtime = InputList[i]
        if (InputList[i - 1] != InputList[-1]):
            # Sleep for the ammount of time of the interval between last input and current one
            sleep(currtime - InputList[i - 1][1])
        # TODO: Implement "shift", "control", "cmd" keys (not just one input only keys)
        # TODO: Also somehow figure out a way to support weird non-american keyboard keys
        try:
            keyboard_controller.press(key)
            keyboard_controller.release(key)
        except Exception as e:
            print("Unsupported key was pressed, check logfiles for more information")
            logging.error(e)
            exit()


def main() -> None:
    try:
        user_input = recordInput()
        logging.info(user_input)
        print("Script ran successfully!")
    except Exception as e:
        print("An error ocourred during runtime, check logfiles for more information.")
        logging.error(e)


if __name__ == "__main__":
    main()
