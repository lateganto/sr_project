import time

import config
from utils import ask_question, speak, face_animation, see_letter, letter_to_index, serialize_users


def first_scenario(robot, users_list, current_user):
    repeat = True
    while repeat:
        letter_to_write = ask_question(robot, "What letter do you want to write?")
        print("LETTER: " + letter_to_write)

        attempts = 2
        while letter_to_write != 'a':
            if attempts != 0:
                letter_to_write = ask_question(robot, "What letter?", repeat=True)
                attempts -= 1
            else:
                break

        letter_to_write = "a"

        speak(robot, "Look at my face. This is a" + "hey" + "!").result()
        face_animation(robot)

        time.sleep(2)
        speak(robot, "Try to write it on paper!").result()

        robot.anim.play_animation_trigger("StuckOnEdgeIdle", loop_count=2).result()

        letter = ""
        letter_not_correct = True
        while letter_not_correct:

            response = ask_question(robot, "Done?")
            while not ("yes" in response or "yeah" in response):
                time.sleep(3)
                # robot.anim.play_animation_trigger("StuckOnEdgeIdle", loop_count=2).result()
                response = ask_question(robot, "Done?")

            speak(robot, "Show me the letter!").result()
            time.sleep(1)
            [letter, accuracy] = see_letter(robot)

            # testo è vuoto
            if not letter:
                time.sleep(2)
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "There's nothing on your paper. Come on, try again!").result()
                speak(robot, "Try to write it on paper!").result()
            # todo control if the letters correspond
            elif letter == "aaa":
                letter_not_correct = False
            elif letter != letter_to_write:
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "This is not a" + letter_to_write + ". Come on, try again!").result()
                speak(robot, "Try to write it on paper!").result()
                robot.anim.play_animation_trigger("StuckOnEdgeIdle", loop_count=1).result()


        robot.anim.play_animation_trigger("GreetAfterLongTime")
        speak(robot, "It's correct!").result()

        current_user.sl_progress[letter_to_index(letter_to_write)].append(accuracy)  # in questo caso c'è solo la a

        out = ask_question(robot, "Do you want to continue?")
        if "yes" in out:
            repeat = True
        else:
            repeat = False

    users_list.append(current_user)
    serialize_users(users_list)
    speak(robot, "See you!").result()
    exit()


def third_scenario(robot, users_list, current_user):
    repeat = True

    while repeat:

        letter = ""
        while not letter:
            speak(robot, "Show me the letter!").result()
            time.sleep(1)
            [letter, accuracy] = see_letter(robot)

            if letter == "":
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "There's nothing on your paper. Come on, try again!").result()
            elif not letter.isalpha:
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "This is not a letter. Come on, try again!").result()
                letter = ""
            else:  # letter correct -> aggiorno valutazione
                robot.anim.play_animation_trigger(robot, "GreetAfterLongTime")
                speak(robot, "You wrote a," + letter[0]).result()

        if str(letter).islower():
            current_user.sl_progress[letter_to_index(letter[0])].append(accuracy)  # aggiorna la lettera
        else:
            current_user.cl_progress[letter_to_index(letter[0])].append(accuracy)  # aggiorna la lettera

        out = ask_question(robot, "Do you want to continue?")
        if "yes" in out:
            repeat = True
        else:
            repeat = False

    users_list.append(current_user)
    serialize_users(users_list)
    speak(robot, "See you!").result()
    exit()


def second_scenario():
    print("2")


def fourth_scenario():
    print("4")
