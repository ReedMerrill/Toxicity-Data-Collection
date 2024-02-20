"""Utilities for logging and data processing."""

import time
import re
import emojis


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


def clean_comment(comment):
    """Coerce all data to string and remove URLs"""

    string = str(comment)
    clean_comment = re.sub(r"\S*https?:\S*", "", string)

    return clean_comment


def remove_emojis(comment):
    """Removes emojis from a list of strings."""

    decoded = emojis.decode(comment)
    clean = re.sub(r":\w+:", "", decoded)

    return clean
