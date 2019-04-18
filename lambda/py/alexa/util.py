"""Utility module to generate text for commonly used responses."""

import random
import six
import requests
import json
import random
import csv
import capitals
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type
import datetime

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


#Game of Thrones
def make_got_question():
  cool_characters = [583,957,148,238,529,1052,27,565,1303,823,339,216,1963,1022,1560,1880,743,1319,16,1346]
  random_no = random.randint(0, len(cool_characters) - 1)
  response = requests.get("https://anapioficeandfire.com/api/characters/" + str(cool_characters[random_no]))
  response = response.text
  response_data = json.loads(response)
  choose_random = random.randint(0, 4)
  x = choose_got_question(choose_random, response_data)
  return x

def choose_got_question(choose_random, response_data):
   x = []
   answer = ""
   if choose_random == 0:
       answer = response_data["playedBy"][0]
       x.append("Who plays " + response_data["name"] + "?")
       x.append(answer)
   elif choose_random == 1:
       try:
           answer = response_data["name"]
           x.append("Which character goes by the following aliases: " + str(response_data["aliases"]) + "?")
           x.append(answer)
       except:
           x = choose_got_question(0, response_data)
   elif choose_random == 2:
       answer = response_data["father"]
       if not answer:
           x = choose_got_question(0, response_data)
       else:
           new_response = requests.get(str(answer))
           new_response = new_response.text
           new_data = json.loads(new_response)
           answer = new_data["name"]
           x.append("Who is the father of " + str(response_data["name"]) + "?")
           x.append(answer)
   elif choose_random == 3:
       answer = response_data["mother"]
       if not answer:
           x = choose_got_question(0, response_data)
       else:
           new_response = requests.get(str(answer))
           new_response = new_response.text
           new_data = json.loads(new_response)
           answer = new_data["name"]
           x.append("Who is the mother of " + str(response_data["name"]) + "?")
           x.append(answer)
   elif choose_random == 4:
       answer = response_data["spouse"]
       if not answer:
           x = choose_got_question(0, response_data)
       else:
           new_response = requests.get(str(answer))
           new_response = new_response.text
           new_data = json.loads(new_response)
           answer = new_data["name"]
           x.append("Who is the spouse of " + str(response_data["name"]) + "?")
           x.append(answer)
   return x


#General Knowledge
def make_genknow_question():
    star_list = []
    api_url = 'https://opentdb.com/api.php?amount=1&type=boolean'
    response = requests.get(api_url)
    if response.status_code == 200:
        result = json.loads(response.content.decode('utf-8'))
    else:
        return None
    if result is not None:
        for x in result['results']:
            del x['category'], x['type'], x['difficulty'], x['incorrect_answers']
            star_list.append(x['question'])
            star_list.append(x['correct_answer'])
    else:
        print('[!] Request Failed')
    star_list[0] = "True or False: " + star_list[0]
    return star_list


#Harry Potter
def make_hp_question():
   cool_characters = ["Harry+Potter","Ronald+Weasley","Hermione+Granger",
   "Gilderoy+Lockhart","Nymphadora+Tonks","Molly+Weasley","George+Weasley",
   "Fred+Weasley","Minerva+McGonagall","Ginevra+Weasley","Dolores+Umbridge","Lucius+Malfoy",
   "Draco+Malfoy","Bellatrix+Lestrange","Luna+Lovegood",
   "Rubeus+Hagrid","Tom+Riddle","Neville+Longbottom","Albus+Dumbledore","Remus+Lupin",
   "Sirius+Black","Severus+Snape"]
   random_no = random.randint(0, len(cool_characters) - 1)
   response = requests.get("https://www.potterapi.com/v1/characters?key=$2a$10$Gxvo43sSziLX6anH7kL.hOg1gRcvbwJ6WLXIyAJ2ih1PhSdTFrzuy&name=" + cool_characters[random_no])
   response = response.text
   response_data = json.loads(response[1:-1])
   choose_random = random.randint(0,4)
   x = choose_hp_question(choose_random, response_data)
   return x

def choose_hp_question(choose_random, response_data):
   x = []
   answer = ""
   if choose_random == 0:
       answer = response_data["house"]
       x.append("Which house is " + response_data["name"] + " in?")
       x.append(answer)
   elif choose_random == 1:
       try:
           patronus = response_data["patronus"]
           x.append("Which character's patronus is " + patronus + "?")
           x.append(response_data["name"])
       except:
           x = choose_hp_question(0, response_data)
   elif choose_random == 2:
       try:
           boggart = response_data["boggart"]
           x.append("Which character's boggart is " + boggart + "?")
           x.append(response_data["name"])
       except:
           x = choose_hp_question(0, response_data)
   elif choose_random == 3:
       try:
           phoenix = response_data["orderOfThePhoenix"]
           x.append("True or false: " + response_data["name"] + " is a member of the Order of the Phoenix?")
           x.append(str(phoenix))
       except:
           x = choose_hp_question(0, response_data)
   elif choose_random == 4:
       try:
           army = response_data["dumbledoresArmy"]
           x.append("True or false: " + response_data["name"] + " is a member of the Dumbledore's army?")
           x.append(str(army))
       except:
           x = choose_hp_question(0, response_data)
   return x


#Star Wars
def make_sw_question():
   cool_characters = [1,2,3,4,5,9,10,11,12,13,14,20,21,22,44,25,32,36,51,79]
   random_no = random.randint(0, len(cool_characters) - 1)
   response = requests.get("https://swapi.co/api/people/"+str(cool_characters[random_no])+"/?format=json")
   response = response.text
   response_data = json.loads(response)
   choose_random = random.randint(0,2)
   x = choose_sw_question(choose_random, response_data)
   return x

def choose_sw_question(choose_random, response_data):
   x = []
   answer = ""
   if choose_random == 0:
       answer = response_data["homeworld"]
       new_response = requests.get(answer)
       new_response = new_response.text
       new_data = json.loads(new_response)
       name = new_data["name"]
       x.append("What planet is the homeworld of " + response_data["name"] + "?")
       x.append(name)
   elif choose_random == 1:
       answer = response_data["species"][0]
       new_response = requests.get(str(answer))
       new_response = new_response.text
       new_data = json.loads(new_response)
       name = new_data["name"]
       x.append("What is the species of " + response_data["name"] + "?")
       x.append(name)
   elif choose_random == 2:
       try:
           answer = response_data["starships"][0]
           new_response = requests.get(str(answer))
           new_response = new_response.text
           new_data = json.loads(new_response)
           name = new_data["name"]
           x.append("What is the ship piloted by " + response_data["name"] + "?")
           x.append(name)
       except:
           x = choose_sw_question(0, response_data)
   return x


def get_item(attr):
    """Get matching data object from slot value."""
    if attr["current_theme"] == "game of thrones" or attr["current_theme"] == "got" or attr["current_theme"] == "a song of ice and fire":
        return make_got_question()
    elif attr["current_theme"] == "general knowledge" or attr["current_theme"] == "general" or attr["current_theme"] == "general questions" or attr["current_theme"] == "anything" or attr["current_theme"] == "whatever":
        return make_genknow_question()
    elif attr["current_theme"] == "harry potter" or attr["current_theme"] == "hp" or attr["current_theme"] == "fantastic beasts" or attr["current_theme"] == "the wizarding world":
        return make_hp_question()
    elif attr["current_theme"] == "capitals" or attr["current_theme"] == "countries" or attr["current_theme"] == "geography" or attr["current_theme"] == "capital cities":
        return capitals.make_capitals_question()
    elif attr["current_theme"] == "star wars":
        return make_sw_question()
    else:
        return ["NO THEME FOUND", "ANSWER"]


def get_question(item):
    if item is not None:
        question = item[0]
    else:
        question = "QUESTION HERE!"

    return question


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


def check_answer(slots, value):
    """Compare slot value to the value provided."""
    for _, slot in six.iteritems(slots):
        if slot.value is not None:
            return slot.value.lower() == value.lower()
    else:
        return False

def get_speechcon(correct_answer):
    """Return speechcon corresponding to the boolean answer correctness."""
    text = ("<say-as interpret-as='interjection'>{} !"
            "</say-as><break strength='strong'/>")
    if correct_answer:
        return text.format(random.choice(data.CORRECT_SPEECHCONS))
    else:
        return text.format(random.choice(data.WRONG_SPEECHCONS))


def get_recipient(attr):
    """Generate the player to ask a question to."""
    return random.choice(attr["player_names"])

def generate_forfeit(attr, player):
    players = attr["player_names"]
    choice = random.uniform(0,1)
    if choice <= 0.45:
        no = random.randint(1,4)
        if no == 1:
                return "{}, drink {} many drink.".format(player, no)
        return "{}, drink {} many drinks.".format(player, no)
    elif choice <= 0.55:
        return "{}, finish your drink.".format(player)
    elif choice <= 0.75:
        if len(players) < 2:
            no = random.randint(1,4)
            if no == 1:
                return "{}, drink {} many drink.".format(player, no)
            return "{}, drink {} many drinks.".format(player, no)
        else :
            newplayer = random.choice(players)
            while newplayer == player:
                newplayer = random.choice(players)
            return "{}, add some of {}'s drink to yours and take a drink.".format(player, newplayer)
    else:
        if len(players) < 2:
            no = random.randint(1,4)
            if no == 1:
                return "{}, drink {} many drink.".format(player, no)
            return "{}, drink {} many drinks.".format(player, no)
        else :
            newplayer = random.choice(players)
            while newplayer == player:
                newplayer = random.choice(players)
            return "{}, come up with a truth or dare for {}.".format(newplayer, player)

def generate_task(attr, player):
    players = attr["player_names"]
    choice = random.uniform(0,1)
    if choice < 0.5:
        if len(players) < 2:
            no = random.randint(1,4)
            if no == 1:
                return "{}, drink {} many drink.".format(player, no)
            return "{}, drink {} many drinks.".format(player, no)
        else:
            newplayer = random.choice(players)
            while newplayer == player:
                newplayer = random.choice(players)
            no = random.randint(1,3)
            if no == 1:
                return "{}, take {} drink.".format(newplayer, no)
            return "{}, take {} drinks!".format(newplayer, no)
    elif choice < 0.75:
        if len(players) < 2:
            return "{}, finish your drink!".format(player)
        else:
            no = random.randint(1,4)
            if no == 1:
                return "{}, give out {} drink.".format(player, no)
            return "{}, give out {} drinks.".format(player, no)
    else:
        if len(players) < 2:
            no = random.randint(1,4)
            if no == 1:
                return "{}, drink {} many drink.".format(player, no)
            return "{}, drink {} many drinks.".format(player, no)
        else:
            newplayer = random.choice(players)
            while newplayer == player:
                newplayer = random.choice(players)
            return "{}, come up with a truth or dare for {}.".format(player, newplayer)


def time_of_the_day():
    current_time = datetime.datetime.now().hour
    int(current_time)
    if current_time < 12:
        return 'morning'
    elif 12 <= current_time < 18:
        return 'afternoon'
    elif 18 <= current_time < 21:
        return 'evening'
    else:
        return 'night'
