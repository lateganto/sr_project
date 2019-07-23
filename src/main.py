import os
import random
import threading
import time

import anki_vector
from anki_vector import audio
from anki_vector.events import Events
from anki_vector.user_intent import UserIntentEvent, UserIntent
from anki_vector.util import degrees

import config
from scenarios import first_scenario, third_scenario, second_scenario, fourth_scenario
from users import acquaintance, load_user_profiles
from utils import speak, serialize_users, ask_question


# first part of acquaintance
def first_phase(robot):
    robot.behavior.set_head_angle(degrees(40.0))
    robot.behavior.set_lift_height(0.0)

    current_user = None  # child who's interacting now with Vector
    users_list = []

    # file not exists, create it
    if not os.path.exists(config.USERS_PROFILES_FILENAME):
        file = open(config.USERS_PROFILES_FILENAME, 'w')
        file.close()

    # check if there are saved users, otherwise try to add a new one
    if os.stat(config.USERS_PROFILES_FILENAME).st_size == 0:
        robot.anim.play_animation_trigger("FistBumpSuccess")
        speak(robot, "Hy, I'm Vector!").result()
        current_user = acquaintance(robot)

    else:
        users_list = load_user_profiles()

        robot.anim.play_animation_trigger("FistBumpSuccess")
        out = ask_question(robot, "Hi buddy. Have we met before?", False)

        if "yes" in out or "yeah" in out:
            attempts = 3
            while attempts != 0 and current_user is None:
                out = ask_question(robot, "What's your name?", False)
                for u in users_list:
                    if u.name == out:
                        robot.anim.play_animation_trigger("GreetAfterLongTime")
                        speak(robot, "Hy" + u.name).result()
                        current_user = u
                        users_list.remove(u)  # remove user from list in order to update his progress

                # Vector doesn't found the user, so tries again
                if current_user is None:
                    robot.anim.play_animation_trigger("ICantDoThat")
                    speak(robot, "I don't understand").result()

                attempts -= 1

            # After three attempts it tries to add a new user
            if current_user is None:
                robot.anim.play_animation_trigger("ICantDoThat")
                speak(robot, "It seems that we have never met before!").result()
                current_user = acquaintance(robot)

        else:
            # new child
            robot.anim.play_animation_trigger("FistBumpSuccess")
            speak(robot, "Hy, I'm Vector!").result()
            current_user = acquaintance(robot)

    # # adds user information to JSON
    # users_list.append(current_user)
    # serialize_users(users_list)

    # starts the game
    second_phase(robot, users_list, current_user)


# TRIGGER COMMANDS TO START SCENARIOS
#   1. Show me how to write a letter?
#   2. I wrote a letter.
#   3-4. Play a random game.
def second_phase(robot, users_list, current_user):
    loop = True

    while loop:
        time.sleep(1)
        intent = ask_question(robot, "What do you want to do?", phrase_time_limit=6)

        if "how" in intent and "write" in intent:
            first_scenario(robot, users_list, current_user)
            loop = False
        elif "wrote" in intent:
            third_scenario(robot, users_list, current_user)
            loop = False
        elif "random" in intent:
            if random.randint(1, 2) == 1:
                second_scenario(robot, users_list, current_user)
            else:
                fourth_scenario(robot, users_list, current_user)
            loop = False
        else:
            robot.anim.play_animation_trigger("InvalidAnimTrigger")
            speak(robot, "I don't understand!").result()


# Here is defined what Vector does when it recognize his trigger command ("Hey Vector! Play a game!")
def on_user_intent(robot, event_type, event, done):
    user_intent = UserIntent(event)

    # check if the trigger command is "Hey Vector! Play a game!"
    if user_intent.intent_event is UserIntentEvent.play_anygame:
        robot.anim.play_animation_trigger("GreetAfterLongTime")
        robot.behavior.say_text("Ok, let's play", use_vector_voice=config.VECTOR_VOICE).result()
    done.set()


if __name__ == "__main__":
    # you need the Async to let Vector talk and play animations together
    with anki_vector.AsyncRobot() as robot:
        robot.audio.set_master_volume(audio.RobotVolumeLevel.HIGH)
        robot.behavior.drive_off_charger()
        done = threading.Event()
        robot.events.subscribe(on_user_intent, Events.user_intent, done)

        print(
            '------ Vector is waiting for the voice command "Hey Vector! Play a game!" Press ctrl+c to exit early ------')

        while True:
            if done.wait(0.2):
                robot.events.unsubscribe(on_user_intent, Events.user_intent)
                break

        print("Start!")

        first_phase(robot)

        # users_list = load_user_profiles()
        # current_user = users_list[0]
        # users_list.remove(current_user)
        # # second_phase(robot, users_list, current_user)
        # third_scenario(robot, users_list, current_user)
