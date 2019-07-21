# import json
# # import os
# #
# from anki_vector import AsyncRobot
#
# from users import User
#
# #
# #
# users_list = []
#
# # users = {}
# # users['user1'] = {
# #     'name': 'antonio',
# #     'age': 7
# # }
# # users_list.append(users)
# #
# #
# # users = {}
# # users['user1'] = {
# #     'name': 'franco',
# #     'age': 7
# # }
# # users_list.append(users)
#
# import string
#
# data = {}
# data['name'] = 'antonio'
# data['age'] = 6
# data['school_grade'] = "First"
# capital_letters = {}
# small_letters = {}
# for letter in list(string.ascii_uppercase):
#     capital_letters[letter] = [1, 1, 1]
# for letter in list(string.ascii_lowercase):
#     small_letters[letter] = [0, 0, 0]
# data['capital_letters_results'] = capital_letters
# data['small_letters_results'] = small_letters
# users_list.append(data)
#
# data = {}
# data['name'] = 'giovanni'
# data['age'] = 7
# data['school_grade'] = "Third"
# capital_letters = {}
# small_letters = {}
# for letter in list(string.ascii_uppercase):
#     capital_letters[letter] = [2, 2, 2]
# for letter in list(string.ascii_lowercase):
#     small_letters[letter] = [3, 3, 3]
# data['capital_letters_results'] = capital_letters
# data['small_letters_results'] = small_letters
# users_list.append(data)
#
# # data = {}
# # data['name'] = 'francesco'
# # data['age'] = 5
# # progress = {}
# # progress['never_write'] = False
# # progress['skills'] = 4
# # data['progress'] = progress
# # users_list.append(data)
#
# with open('users.json', 'w') as outfile:
#     json.dump(users_list, outfile, indent=3)
#
# with open('users.json') as infile:
#     data_new = json.load(infile)
#
# users_list = []
# for u in data_new:
#     capital_letters = list(string.ascii_uppercase)
#     small_letters = list(string.ascii_lowercase)
#
#     capital_letters_results = []
#     small_letters_results = []
#     for c_letter, s_letter in zip(capital_letters, small_letters):
#         capital_letters_results. append(u['capital_letters_results'][c_letter])
#         small_letters_results.append(u['small_letters_results'][s_letter])
#
#     user_tmp = User(u['name'], u['age'], u['school_grade'], capital_letters_results, small_letters_results)
#     # user_tmp = User(u['name'], u['age'], u['school_grade'], capital_letters_results, small_letters_results)
#     # users_list.append(user_tmp)

#########################################################################

import anki_vector

serial = "005047f2"  # "009045e1"
with anki_vector.Robot(serial=serial) as robot:
    robot.anim.play_animation_trigger("NothingToDoBoredIdle")
