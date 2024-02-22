"""Utilities for logging and data processing."""

import time
import re
import emojis
from langdetect import detect
import pandas as pd


def process_user_ids(id_list):
    """Clean the user IDs obtained during runs of sample.py.

    Inputs: list of user IDs
    Returns: Cleaned list of user IDs
        - removes duplicates
        - removes AutoModerator
        - removes None values
    """
    no_dupes = list(set(id_list))

    return [user for user in no_dupes if user not in ("None", "AutoModerator")]


def log_to_file(path, message):
    """output logging events to a file"""
    with open(f"{path}", "a") as file:
        file.write(message)


def estimate_time_remaining(task_index, total_tasks, start_time):
    """Estimate the time remaining.
    - Calculates the time per task for all tasks complete so far.
    - Outputs the time per task multiplied by the number of remaining
    tasks.
    """
    elapsed = (time.time() - start_time) / 3600  # convert seconds to hours
    t_per_task = elapsed / (task_index + 1)
    estimate = t_per_task * (total_tasks - task_index)

    return estimate


def remove_urls(comment):
    """Coerce all data to string and remove URLs"""

    pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    word_list = str(comment).split()
    clean_word_list = [re.sub(pattern, "", word) for word in word_list]
    clean = " ".join(clean_word_list)

    print("===================")
    print("Remove Emojis")
    print("output type")
    print(type(clean))
    print(clean)

    return clean


def remove_emojis(comment):
    """Removes emojis from a list of strings."""

    string = str(comment)
    decoded = emojis.decode(string)
    word_list = decoded.split()
    clean_word_list = [re.sub(r":\w+:", "", word) for word in word_list]
    clean = " ".join(clean_word_list)

    print("===================")
    print("Remove Emojis")
    print("output type")
    print(type(clean))
    print(clean)

    return clean


def check_language(comment):
    """Check that strings are English and return them if they are, or NA if
    not."""

    word_list = str(comment).split()
    lang = detect(comment)

    if lang == "en":
        return comment
    else:
        return pd.NA
