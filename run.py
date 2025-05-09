#!/usr/bin/env python3

from time import strptime
import datetime
import shutil
import sys

__author__ = 'jaredchu'

import os
from os.path import expanduser
import random
import help

old_date_format = '%d-%m-%Y'
date_format = '%Y-%m-%d'


def random_file(dir_path):
    if (os.path.isdir(dir_path)):
        for i in range(0, 100):
            new_file_path = dir_path + random.randint(0, 9999).__str__() + '.txt'
            if not os.path.isfile(new_file_path):
                new_file = open(new_file_path, 'w')
                new_file.write('')
                new_file.close()


def random_dir(dir_path):
    if (os.path.isdir(dir_path)):
        for i in range(0, 10):
            new_dir_path = dir_path + random.randint(0, 9999).__str__()
            if not os.path.isdir(new_dir_path):
                os.mkdir(new_dir_path)


def is_archive_dir(path):
    result = False
    dir_name = path
    try:
        dir_name = path.split('/')[-1]
    except Exception as e:
        print((e.__str__()))

    # remove conflict with old version
    result = is_old_archive_dir(path)

    try:
        strptime(dir_name, date_format)
        result = True
    except Exception as e:
        # print('This dir is not archive dir' + e.__str__())
        pass

    return result


def is_old_archive_dir(path):
    result = False
    dir_name = path
    try:
        dir_name = path.split('/')[-1]
    except Exception as e:
        print((e.__str__()))

    try:
        strptime(dir_name, old_date_format)
        result = True
    except Exception as e:
        # print('This dir is not archive dir' + e.__str__())
        pass

    return result


def get_name(path):
    return path.split('/')[-1]


def with_slash(string):
    if (string[-1] == '/'):
        return string
    else:
        return string + '/'


# mem_var
dir_count = 0
file_count = 0

# program var
version = 1.7

# ARGS
file_only = False
folder_only = False
all_type = True
if (sys.argv.__len__() > 1):
    args = sys.argv[1]
    if ('-' in args):
        if ('f' in args):
            file_only = True
            folder_only = False
            all_type = False
        elif ('d' in args):
            file_only = False
            folder_only = True
            all_type = False

show_version = False
for arg in sys.argv:
    if (arg == '--version'):
        show_version = True

is_test = False
for arg in sys.argv:
    if (arg == '--test'):
        is_test = True

is_help = False
for arg in sys.argv:
    if (arg == '--help'):
        is_help = True

set_target = False
target_dir = ''
for index, arg in enumerate(sys.argv):
    if (arg == '--target'):
        set_target = True
        try:
            target_dir = sys.argv[index + 1]
        except Exception as e:
            pass

filter_by_text = False
filter_text = ""
for index, arg in enumerate(sys.argv):
    if (arg == '--contain'):
        filter_by_text = True
        try:
            filter_text = sys.argv[index + 1]
        except Exception as e:
            pass

is_upgrade_folder_name_format = False
for arg in sys.argv:
    if (arg == '--upgrade'):
        is_upgrade_folder_name_format = True


# Test
def test(working_dir_path):
    random_dir(working_dir_path)
    random_file(working_dir_path)


# Upgrade folder name format
# todo: this function is not completed
def upgrade(working_dir_path):
    return
    # childs = os.listdir(working_dir_path)
    # childs_path = [working_dir_path + x for x in childs]
    # for child_path in childs_path:
    #     if is_old_archive_dir(child_path):
    #         new_child_path = working_dir_path + datetime.datetime.now().strftime(date_format)
    #         print("Rename " + child_path + " to " + with_slash(new_child_path))


# Main progarm
def main(working_dir_path):
    print("")
    print("-- Cleanup started --")
    print("")

    childs = os.listdir(working_dir_path)
    childs_path = [working_dir_path + x for x in childs]

    junk_files = [path for path in childs_path if not is_archive_dir(path)]
    new_archive_dir_name = datetime.datetime.now().strftime(date_format)
    new_archive_dir_path = working_dir_path + new_archive_dir_name

    if not junk_files:
        print(("Working directory is empty " + working_dir_path))
        return
    else:
        if not os.path.isdir(new_archive_dir_path):
            print(("Create new directory " + new_archive_dir_path))
            os.mkdir(new_archive_dir_path)
        else:
            print(("Directory " + new_archive_dir_path + " is exits"))
            # Add timestamp to make unique directory name
            timestamp = datetime.datetime.now().strftime("%H%M%S")
            new_archive_dir_name = f"{new_archive_dir_name}_{timestamp}"
            new_archive_dir_path = working_dir_path + new_archive_dir_name
            print(f"Creating new directory {new_archive_dir_path}")
            os.mkdir(new_archive_dir_path)

    def move_junk(src):
        global dir_count
        global file_count

        do_move = False

        # Move command
        if (filter_by_text):
            if (len(filter_text) > 0 and filter_text in get_name(src)):
                do_move = True
        else:
            do_move = True

        if (do_move):
            shutil.move(src, new_archive_dir_path)
            print(("Move " + src + " to " + with_slash(new_archive_dir_path)))

        if (os.path.isdir(src)):
            dir_count += 1
        if (os.path.isfile(src)):
            file_count += 1

    for junk in junk_files:
        if (file_only == True):
            if (os.path.isfile(junk)):
                move_junk(junk)
        elif (folder_only == True):
            if (os.path.isdir(junk)):
                move_junk(junk)
        elif (all_type == True):
            move_junk(junk)

    # print("")
    # print("Complete, moved " + dir_count.__str__() + " folder and " + file_count.__str__() + " file")
    print("")
    print("-- All done! --")
    print("")


if (show_version):
    print(("Current version is " + version.__str__()))
elif (is_test):
    test(with_slash(os.environ['PWD']))
elif (is_help):
    help.get_help()
elif (is_upgrade_folder_name_format):
    upgrade(with_slash(os.environ['PWD']))
else:
    # confirm if wpd is not user's desktop or temp
    confirmed = True

    desktop_dir = expanduser("~") + '/Desktop'
    temp_dir = expanduser("~") + '/Temp'
    if (os.environ['PWD'] != desktop_dir and os.environ['PWD'] != temp_dir):
        response = ''
        while (True):
            response = input("You are perform cleaning a directory outside of Desktop or Temp, are you sure [y/n]: ").lower()
            if (response == 'y' or response == 'n'):
                break
            else:
                print("Please enter y or n")

        if (response == 'y'):
            confirmed = True
        else:
            confirmed = False

    if (confirmed):
        if (set_target == True):
            wdp = ''
            if ('/' == target_dir[0] and os.path.isdir(target_dir)):
                wpd = target_dir
            else:
                wpd = with_slash(os.environ['PWD']) + target_dir
            main(wpd)
        else:
            main(with_slash(os.environ['PWD']))
        pass
    else:
        print("Canceled")
