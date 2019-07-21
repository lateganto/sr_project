import random
import threading
import time

import anki_vector
import cv2
import numpy as np
from anki_vector import audio
from anki_vector.events import Events
from anki_vector.user_intent import UserIntentEvent, UserIntent
from anki_vector.util import degrees

import config
import os

from api_google import detect_text
from game import first_scenario, third_scenario, second_scenario, fourth_scenario
from users import acquaintance, load_user_profiles
from utils import ask_question, serialize_users, speak


def first_phase(robot):
    robot.behavior.drive_off_charger()
    robot.behavior.set_head_angle(degrees(30.0))
    robot.behavior.set_lift_height(0.0)
    robot.audio.set_master_volume(audio.RobotVolumeLevel.HIGH)

    current_user = None
    users_list = []

    # file not exists, create it
    if not os.path.exists(config.USERS_PROFILES_FILENAME):
        file = open(config.USERS_PROFILES_FILENAME, 'w')
        file.close()

    # file exists
    # controlla se c'è almeno un altro utente salvato, altrimenti cerca di aggiungerne uno
    if os.stat(config.USERS_PROFILES_FILENAME).st_size == 0:
        current_user = acquaintance(robot)
        # users_list.append(current_user)

    # cerca utente già registrato
    else:
        users_list = load_user_profiles()

        play_animation(robot, "FoundFace")
        out = ask_question(robot, "Hi buddy. Have we met before?", False)
        if "yes" in out or "yeah" in out:
            # print("aia")
            attempts = 2

            while attempts != 0 and current_user is None:
                out = ask_question(robot, "What's your name?", False)
                play_animation(robot, "VC_ListeningGetIn")
                for u in users_list:
                    if u.name == out:
                        print("ti ho trovato!")
                        current_user = u
                if current_user is None:
                    play_animation(robot, "ICantDoThat")
                    speak(robot, "I don't understand")

                attempts -= 1

            # Dopo 3 tentativi probabilmente non lo conosce e cerca di fare conoscenza col bambino
            if current_user is None:
                speak(robot, "Seems that we have never met before!")
                current_user = acquaintance(robot)

        else:
            # todo se il nome del nuovo bambino è già presente
            # faccio conoscenza del nuovo bambino
            current_user = acquaintance(robot)
            # users_list.append(current_user)

    # serialize_users(users_list, config.USERS_PROFILES_FILENAME)

    second_phase(robot, users_list, current_user)


def second_phase(robot, users_list, current_user):
    desire = ask_question(robot, "What do you want to do?", phrase_time_limit=6)

    if "how" in desire and "write" in desire:
        first_scenario(robot, users_list, current_user)
    elif "wrote" in desire:
        third_scenario()
    elif "random" in desire:
        if random.randint(1, 2) == 1:
            second_scenario()
        else:
            fourth_scenario()


def main():
    def on_user_intent(robot, event_type, event, done):
        user_intent = UserIntent(event)
        # print(f"Received {user_intent.intent_event}")
        # print(user_intent.intent_data)

        # The children has to say "Hey Vector! Play a game!"
        if user_intent.intent_event is UserIntentEvent.play_anygame:
            speak(robot, "Ok, let's play")
            first_phase(robot)

        done.set()

    with anki_vector.Robot(serial="005047f2") as robot:
        # robot.behavior.drive_off_charger()
        done = threading.Event()
        robot.events.subscribe(on_user_intent, Events.user_intent, done)

        print(
            '------ Vector is waiting for the voice command "Hey Vector! Play a game!" Press ctrl+c to exit early ------')

        try:
            if not done.wait(timeout=30):
                print('------ Vector never heard a voice command ------')
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    serial = "005047f2"  # "009045e1"
    with anki_vector.robot.AsyncRobot(serial="005047f2") as robot:
        users_list = load_user_profiles()
        current_user = users_list[0]
        second_phase(robot, users_list, current_user)

    # robot.behavior.say_text("Now is the time")
    # robot.behavior.turn_in_place(degrees(3 * 360))

    # greet_future.result()
    # say_future.result()


# with anki_vector.AsyncRobot(serial=serial) as robot:
#     # Start saying text asynchronously
#     say_future = robot.behavior.say_text("Now is the time")
#     # Turn robot, wait for completion
#     turn_future = robot.behavior.turn_in_place(degrees(3 * 360))
#     turn_future.result()
#     # Play animation, wait for completion
#     greet_future = robot.anim.play_animation('anim_turn_left_01')
#     greet_future.result()
#     # Make sure text has been spoken
#     say_future.result()

# main()
