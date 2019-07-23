import time

from utils import ask_question, speak, face_animation, see_letter, letter_to_index, serialize_users


# ********   FIRST SCENARIO (- is child, * is Vector)   ********
# - "Let me see how to write a letter"
# * "Ok, what letter?"
# - "a"
# * Vector shows the animated GIF
#   "Try to write it now!"
#   Waits
# * "Done?"
#     - "Yes" -> Child holds the paper, Vector evaluates it and gives the result updating progress
#     - "No"  -> waits and asks again
# * "Do you want to continue?"
#     - "Yes" -> repeat
#     - "No"  -> game over
def first_scenario(robot, users_list, current_user):
    speak(robot, "Ok")

    repeat = True
    while repeat:
        letter_to_write = ask_question(robot, "What letter do you want to write?")
        print("LETTER: " + letter_to_write)

        # Vector shows and recognizes only the "a". After 2 attempts it shows anyway the letter "a"
        # todo extend with remaining letters
        attempts = 2
        while letter_to_write != 'a':
            if attempts != 0:
                letter_to_write = ask_question(robot, "What letter?", repeat=True)
                attempts -= 1
            else:
                break
        letter_to_write = "a"

        speak(robot, "Look at my face. This is a " + "a" + "!").result()
        face_animation(robot)

        time.sleep(2)
        speak(robot, "Try to write it on paper!").result()

        # Vector shows an animation while waits for the child to complete
        robot.anim.play_animation_trigger("StuckOnEdgeIdle", loop_count=2).result()

        letter = ""
        letter_not_correct = True
        while letter_not_correct:
            response = ""
            while not ("yes" in response or "yeah" in response):
                response = ask_question(robot, "Done?")
                robot.anim.play_animation_trigger("StuckOnEdgeIdle", loop_count=2).result()

            speak(robot, "Show me the letter!").result()
            time.sleep(1)
            [letter, accuracy] = see_letter(robot)

            # empty text
            if not letter:
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "There's nothing on your paper. Come on, try again!").result()
                speak(robot, "Try to write it on paper!").result()
            # control if the letters correspond
            elif letter != letter_to_write:
                robot.anim.play_animation_trigger(robot, "InvalidAnimTrigger")
                speak(robot, "This is not a " + letter_to_write + ". Come on, try again!").result()
                speak(robot, "Try to write it on paper!").result()
                robot.anim.play_animation_trigger("StuckOnEdgeIdle").result()
            # letter correct
            else:
                letter_not_correct = False

        robot.anim.play_animation_trigger("GreetAfterLongTime")
        speak(robot, "It's correct!").result()

        # updates progress with new assessment
        current_user.sl_progress[letter_to_index(letter_to_write)].append(accuracy)

        out = ask_question(robot, "Do you want to continue?")
        if "yes" in out:
            repeat = True
        else:
            repeat = False

    # end of the game, serialize information about users
    users_list.append(current_user)
    serialize_users(users_list)
    speak(robot, "See you!").result()
    exit()


# ********   THIRD SCENARIO (- is child, * is Vector)   ********
#   - "I wrote a letter"
#   * "Show me the letter!"
#   - Child holds the paper
#   * Vector gives the result and updates progress
#   * "Do you want to continue?"
#       - "Yes" -> repeat
#       - "No"  -> game over
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
            # letter correct
            else:
                robot.anim.play_animation_trigger(robot, "GreetAfterLongTime")
                speak(robot, "You wrote a," + letter[0]).result()

        # progress update
        if str(letter).islower():
            current_user.sl_progress[letter_to_index(letter[0])].append(accuracy)
        else:
            current_user.cl_progress[letter_to_index(letter[0])].append(accuracy)

        out = ask_question(robot, "Do you want to continue?")
        if "yes" in out:
            repeat = True
        else:
            repeat = False

    # end of the game, serialize information about users
    users_list.append(current_user)
    serialize_users(users_list)
    speak(robot, "See you!").result()
    exit()


def second_scenario(robot, users_list, current_user):
    print("2")


def fourth_scenario(robot, users_list, current_user):
    print("4")
