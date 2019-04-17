
"""Utility module to generate text for commonly used responses."""

import random
import six
import requests
import json
import random
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type

from . import data


def supports_display(handler_input):
    # type: (HandlerInput) -> bool
    """Check if display is supported by the skill."""
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.
                        supported_interfaces, 'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False


def get_bad_answer(item):
    """Return response text for incorrect answer."""
    return "{} {}".format(data.BAD_ANSWER.format(item), data.HELP_MESSAGE)


def get_current_score(score, counter):
    """Return the response text for current quiz score of the user."""
    return data.SCORE.format("current", score, counter)


def get_final_score(score, counter):
    """Return the response text for final quiz score of the user."""
    return data.SCORE.format("final", score, counter)


def __get_attr_for_speech(attr):
    """Helper function to convert attribute name."""
    return attr.lower().replace("_", " ").strip()


def make_got_question():
    cool_characters = [583, 957, 148, 238, 529, 1052, 27, 565, 271]
    random_no = random.randint(0, len(cool_characters) - 2)
    response = requests.get("https://anapioficeandfire.com/api/characters/" + str(cool_characters[random_no]))
    response = response.text
    response_data = json.loads(response)
    choose_random = random.randint(0, 4)
    x = []
    if choose_random == 0:
        answer = response_data["playedBy"]
        if answer != "[]":
            x.append("Who plays " + response_data["name"] + "?")
            x.append(answer)
    elif choose_random == 1:
        answer = response_data["name"]
        if answer != "[]":
            x.append("Which character goes by the following aliases: " + str(response_data["aliases"]) + "?")
            x.append(answer)
    elif choose_random == 2:
        answer = response_data["titles"]
        if answer == "[]":
            answer = "None"
        x.append("What are the titles of " + str(response_data["name"]) + ", if any?")
        x.append(answer)
    elif choose_random == 3:
        answer = response_data["father"]
        if not answer:
            answer = "None"
        else:
            new_response = requests.get(str(answer))
            new_response = new_response.text
            new_data = json.loads(new_response)
            answer = new_data["name"]
        x.append("Who is the father of " + str(response_data["name"]) + ", if any?")
        x.append(answer)
    elif choose_random == 4:
        answer = response_data["mother"]
        if not answer:
            answer = "None"
        else:
            new_response = requests.get(str(answer))
            new_response = new_response.text
            new_data = json.loads(new_response)
            answer = new_data["name"]
        x.append("Who is the mother of " + str(response_data["name"]) + ", if any?")
        x.append(answer)
    return x

def make_genknow_question():
   star_list = []
   api_url = 'https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=boolean'
   response = requests.get(api_url)
   if response.status_code == 200:
       result = json.loads(response.content.decode('utf-8'))
   else:
       return None
   if result is not None:
       for x in result['results']:
           # print(x['name'], x['height'], x['hair_color'])
           del x['category'], x['type'], x['difficulty'], x['incorrect_answers']
           star_list.append(x['question'])
           star_list.append(x['correct_answer'])
   else:
       print('[!] Request Failed')
   return star_list

def make_hp_question():
    return ""

def get_item(attr):
    """Get matching data object from slot value."""
    if attr["current_theme"] == "game of thrones" or attr["current_theme"] == "got" or attr["current_theme"] == "a song of ice and fire":
        return make_got_question()
    elif attr["current_theme"] == "general knowledge":
        return make_genknow_question()
    elif attr["current_theme"] == "harry potter":
        return make_hp_question()
    elif attr["current_theme"] == "star wars":
        return ["STAR WARS", "ANSWER"]
    else:
        return ["NO THEME FOUND", "ANSWER"]


def get_question(item):
    if item is not None:
        question = item[0]
    else:
        question = "QUESTION HERE!"

    return question


def get_answer(attr, item):
    """Return response text for correct answer to the user."""
    if attr.lower() == "abbreviation":
        return ("The {} of {} is "
                "<say-as interpret-as='spell-out'>{}</say-as>. ").format(
            __get_attr_for_speech(attr), item["state"], item["abbreviation"])
    else:
        return "The {} of {} is {}. ".format(
            __get_attr_for_speech(attr), item["state"], item[attr.lower()])


def get_multiple_choice_answers(item, attr, states_list):
    """Return multiple choices for the display to show."""
    answers_list = [item[attr]]
    # Insert the correct answer first

    while len(answers_list) < 3:
        state = random.choice(states_list)

        if not state[attr] in answers_list:
            answers_list.append(state[attr])

    random.shuffle(answers_list)
    return answers_list


def compare_token_or_slots(handler_input, value):
    """Compare value with slots or token,
        for display selected event or voice response for quiz answer."""
    if is_request_type("Display.ElementSelected")(handler_input):
        return handler_input.request_envelope.request.token == value
    else:
        return compare_slots(
            handler_input.request_envelope.request.intent.slots, value)


def get_recipient(attr):
    """Generate the player to ask a question to."""
    return random.choice(attr["player_names"])


def generate_forfeit(attr, player):
    players = attr["player_names"]
    choice = random.uniform(0,1)
    if choice <= 0.45:
        no = random.randint(1,4)
        return "{}, drink {} many drinks.".format(player, no)
    elif choice <= 0.55:
        return "{}, finish your drink.".format(player)
    elif choice <= 0.75:
        if attr["player_no"] < 2:
            no = random.randint(1,4)
            return "{}, drink {} many drinks.".format(player, no)
        else :
            newplayer = random.choice(players)
            while newplayer != player:
                newplayer = random.choice(players)
            return "{}, add some of {}'s drink to yours and take a drink.".format(player, newplayer)
    else:
        if attr["player_no"] < 2:
            no = random.randint(1,4)
            return "{}, drink {} many drinks.".format(player, no)
        else :
            newplayer = random.choice(players)
            while newplayer != player:
                newplayer = random.choice(players)
            return "{}, come up with a truth or dare for {}.".format(newplayer, player)