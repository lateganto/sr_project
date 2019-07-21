import json
import time

import anki_vector
import cv2
import numpy as np
from PIL import Image
from anki_vector.util import degrees

import config
import speech_recognition as sr

from api_google import detect_text


def speak(robot, text):
    robot.behavior.say_text(text, duration_scalar=config.DURATION_SCALAR, use_vector_voice=config.VECTOR_VOICE)


def ask_question(robot, question, repeat=False, phrase_time_limit=3):
    r = sr.Recognizer()
    with sr.Microphone(chunk_size=1024) as source:
        if not repeat:
            robot.behavior.say_text(question, use_vector_voice=False).result()
        else:
            robot.anim.play_animation_trigger("ICantDoThat")
            robot.behavior.say_text("I don't understand!", use_vector_voice=False).result()
            robot.behavior.say_text(question, use_vector_voice=False).result()
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


def serialize_users(users_list, filename):
    with open(filename, "w") as file:
        list_tmp = []
        for user in users_list:
            list_tmp.append(user.toJson())

        json.dump(list_tmp, file, indent=2)
        file.close()


def addJson(name, age):
    users_list = []
    data = {}
    data['name'] = str(name)
    data['age'] = age
    data['progress'] = ""
    users_list.append(data)
    return users_list


def check_number(robot, question, number, val_min, val_max):
    while not str(number).isdigit():
        number = ask_question(robot, "This is not a number." + str(question), False)

    if int(number) < val_min:
        speak(robot, "Are you sure? Too small value!")
        exit()
    elif int(number) > val_max:
        speak(robot, "Are you sure? Too high value!")
        exit()


def face_animation(robot):
    robot.anim.play_animation_trigger("VC_ListeningGetIn")
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

    num_loops = 5
    duration_s = 0.25

    # print("Press CTRL-C to quit (or wait %s seconds to complete)" % int(num_loops * duration_s * len(face_images)))


    for _ in range(num_loops):
        for i in range(0, len(face_images)):
            robot.screen.set_screen_with_image_data(face_images[i], duration_s)
            time.sleep(duration_s)


def see_letter(robot):
    robot.behavior.set_head_angle(degrees(30.0))
    robot.behavior.set_lift_height(0.0)

    time.sleep(1)

    robot.camera.init_camera_feed()
    while not robot.camera.latest_image:
        time.sleep(1.0)

    image = robot.camera.latest_image
    robot.anim.play_animation_trigger("TakeAPictureCapture").result()
    # image.raw_image.show()

    image_tmp = np.asarray(image.raw_image)

    cv2.imwrite("files/tmp.png", image_tmp)
    # robot.behavior.say_text("Hold on..")

    [text, accuracy] = detect_text("files/tmp.png")

    print("TEXT:", text)
    print("ACCURACY", accuracy)

    return [text, accuracy]
