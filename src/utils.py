import json
import string
import time

import anki_vector
import cv2
import numpy as np
from PIL import Image
from anki_vector.util import degrees

import config
from api_google import detect_text
import speech_recognition as sr


# used to ask something and get a response
def ask_question(robot, question, repeat=False, phrase_time_limit=3):
    r = sr.Recognizer()
    with sr.Microphone(chunk_size=1024) as source:
        if not repeat:
            robot.anim.play_animation_trigger("LookAtUserEndearingly")
            speak(robot, question).result()
        else:
            robot.anim.play_animation_trigger("ICantDoThat")
            speak(robot, "I don't understand!").result()
            speak(robot, question).result()
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=phrase_time_limit)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        recognized = r.recognize_google(audio)
        print("You said: " + recognized)
        return recognized

    except sr.UnknownValueError:
        return ask_question(robot, question, True)

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Shows an animation. It needs a list of images to show sequentially
def face_animation(robot):
    robot.anim.play_animation_trigger("VC_ListeningGetIn").result()
    robot.behavior.set_head_angle(degrees(30.0)).result()
    robot.behavior.set_lift_height(0.0).result()
    image_settings = []
    face_images = []

    robot.anim.play_animation_trigger("NothingToDoBoredIdle")
    for i in range(0, 11):
        image_settings.append(config.GIF_DIRECTORY + '/small_a/small_a_' + str(i) + '.jpg')

    for image_name in image_settings:
        image = Image.open(image_name)

        image = image.resize((184, 96))
        pixel_bytes = anki_vector.screen.convert_image_to_screen_data(image)

        face_images.append(pixel_bytes)

    num_loops = 3
    duration_s = 0.3

    for _ in range(num_loops):
        for i in range(0, len(face_images)):
            robot.screen.set_screen_with_image_data(face_images[i], duration_s)
            time.sleep(duration_s)


# Using Google Vision API it allows to recognizes text in an image
def see_letter(robot):
    robot.behavior.set_head_angle(degrees(30.0))
    robot.behavior.set_lift_height(0.0)

    time.sleep(1)

    robot.camera.init_camera_feed()
    while not robot.camera.latest_image:
        time.sleep(1.0)

    image = robot.camera.latest_image
    robot.anim.play_animation_trigger("TakeAPictureCapture").result()
    image.raw_image.show()
    # robot.anim.play_animation_trigger("KnowledgeGraphSearching").result()

    image_tmp = np.asarray(image.raw_image)

    cv2.imwrite("files/tmp.png", image_tmp)
    [text, accuracy] = detect_text("files/tmp.png")

    print("TEXT:", text)
    print("ACCURACY", accuracy)

    return [text, accuracy]


# Used to let Vector speak aloud the sentence it has in input
def speak(robot, text):
    return robot.behavior.say_text(text, duration_scalar=config.DURATION_SCALAR, use_vector_voice=config.VECTOR_VOICE)


# Serialize the user to a JSON file
def serialize_users(users_list):
    with open(config.USERS_PROFILES_FILENAME, "w") as file:
        list_tmp = []
        for user in users_list:
            list_tmp.append(user.to_json())

        json.dump(list_tmp, file, indent=2)
        file.close()


def check_age(robot, question, number, val_min, val_max):
    while not str(number).isdigit():
        number = ask_question(robot, "This is not a number." + str(question), False)

    if int(number) < val_min:
        speak(robot, "You are too young to write but you can ask mom something to color! Bye!")
        exit()
    elif int(number) > val_max:
        speak(robot, "I think you have already learned to write! Bye!")
        exit()


def letter_to_index(letter):
    lowercase_alphabet = list(string.ascii_lowercase)
    uppercase_alphabet = list(string.ascii_uppercase)

    if str(letter).islower():
        return lowercase_alphabet.index(letter)
    else:
        return uppercase_alphabet.index(letter)
