import json
import string
import time

import config
from utils import speak, check_age, ask_question


class User:
    def __init__(self, name, age, school_grade, cl_progress, sl_progress):
        self.name = name
        self.age = age
        self.school_grade = school_grade
        self.cl_progress = cl_progress
        self.sl_progress = sl_progress

    def to_json(self):
        data = {}
        data['name'] = str(self.name)
        data['age'] = str(self.age)
        data['school_grade'] = str(self.school_grade)

        capital_letters = {}
        small_letters = {}
        for letter, letter_assessments in zip(list(string.ascii_uppercase), self.cl_progress):
            capital_letters[letter] = letter_assessments
        for letter, letter_assessments in zip(list(string.ascii_lowercase), self.sl_progress):
            small_letters[letter] = letter_assessments

        data['capital_letters_results'] = capital_letters
        data['small_letters_results'] = small_letters

        return data


def acquaintance(robot):
    name = ask_question(robot, "What's your name?", False)
    robot.anim.play_animation_trigger("GreetAfterLongTime")
    speak(robot, "Hy," + name + ". Nice to meet you!").result()
    time.sleep(1)

    age = ask_question(robot, "How old are you?", False)
    check_age(robot, "How old are you?", age, 5, 8)
    speak(robot, "You are" + age + "years old").result()
    time.sleep(1)

    school_grade = ask_question(robot, "What grade are you in?", False)
    while not ("first" in school_grade or "second" in school_grade or "third" in school_grade):
        school_grade = ask_question(robot, "What grade are you in?", True)
    robot.anim.play_animation_trigger("FistBumpSuccess")

    letters_len = len(list(string.ascii_lowercase))
    capital_letter_results = [[] for i in range(letters_len)]
    small_letter_results = [[] for i in range(letters_len)]
    return User(name, age, school_grade, capital_letter_results, small_letter_results)


def load_user_profiles():
    users_list = []
    with open(config.USERS_PROFILES_FILENAME, 'r') as file:
        # salvo tutti gli utenti in users_list
        users = json.load(file)
        for u in users:
            capital_letters = list(string.ascii_uppercase)
            small_letters = list(string.ascii_lowercase)

            capital_letters_results = []
            small_letters_results = []
            for c_letter, s_letter in zip(capital_letters, small_letters):
                capital_letters_results.append(u['capital_letters_results'][c_letter])
                small_letters_results.append(u['small_letters_results'][s_letter])

            user_tmp = User(u['name'], u['age'], u['school_grade'], capital_letters_results, small_letters_results)
            users_list.append(user_tmp)

    return users_list
