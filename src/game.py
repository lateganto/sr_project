import time

from utils import ask_question, face_animation, speak, see_letter


def first_scenario(robot, users_list, current_user):
    letter = ask_question(robot, "What letter?")

    while letter != 'a':
        letter = ask_question(robot, "What letter?", repeat=True)

    speak(robot, "This is an a!")
    face_animation(robot)

    time.sleep(2)
    speak(robot, "Now, try to write it on paper!")
    robot.anim.play_animation_trigger("StuckOnEdgeIdle").result()
    time.sleep(2)
    robot.anim.play_animation_trigger("StuckOnEdgeIdle").result()

    response = ask_question(robot, "Done?")
    while not ("yes" in response or "yeah" in response):
        time.sleep(2)
        robot.anim.play_animation_trigger(robot, "StuckOnEdgeIdle")
        time.sleep(2)
        response = ask_question(robot, "Done?")

    speak(robot, "Show me the letter!")
    time.sleep(3)
    [letter, accuracy] = see_letter(robot)

    # nel caso in cui il testo è vuoto riprova a leggere
    while not letter:
        time.sleep(3)
        speak(robot, "There's nothing on your paper, try again").result()
        [letter, accuracy] = see_letter(robot)

    # todo control if the letter corresponds

    # update stats
    current_user.cl_progress[0] = accuracy  # in questo caso c'è solo la a


def third_scenario():
    print("3")


def second_scenario():
    print("2")


def fourth_scenario():
    print("4")
