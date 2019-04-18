# -*- coding: utf-8 -*-

WELCOME_MESSAGE = ("Welcome to that drinking game! ")

START_QUIZ_MESSAGE = ("I've been told to tell you to drink responsibly. Let's begin! Which theme would you like for round ")

SINGLE_PLAYER_MESSAGE = ("Are you sure you want to play by yourself? "
                        "<prosody pitch=\"x-high\">Alexa, this is so sad, play despacito.</prosody> <break time=\"2s\"/>"
                        "<voice name=\"Celine\"><lang xml:lang=\"fr-FR\">Joking!</lang></voice> "
                        "<emphasis level=\"strong\">Last chance though,</emphasis> ")

NEXT_ROUND_MESSAGE = "Okay! Time for round "

LIST_THEMES = ("The themes to choose from are: "
                "General Knowledge, "
                "Game of Thrones, "
                "Harry Potter, "
                "Star Wars "
                "or Capitals.")

EXIT_SKILL_MESSAGE = ("Thank you for playing that drinking game. Hope you have a good {}!!!")

REPROMPT_SPEECH = "Which other state or capital would you like to know about?"

REPROMPT_PLAYERNO = "How many players are playing {}?"

GET_PLAYERNAME = "Who is player "

HELP_MESSAGE = ("These are some of the commands that might help you: "
                "say <emphasis level=\"strong\">repeat</emphasis> for repeating the question, "
                "<emphasis level=\"strong\">new theme</emphasis> for switching the topic, "
                "<emphasis level=\"strong\">quit</emphasis> for exiting the game. "
                "<break time=\"2s\"/> Now go ahead and have some fun!!!")

CORRECT_SPEECHCONS = ['Booya', 'All righty', 'Bam', 'Bazinga', 'Bingo',
                      'Boom', 'Bravo', 'Cha Ching', 'Cheers', 'Dynomite',
                      'Hip hip hooray', 'Hurrah', 'Hurray', 'Huzzah',
                      'Oh dear.  Just kidding.  Hurray', 'Kaboom', 'Kaching',
                      'Oh snap', 'Phew', 'Righto', 'Way to go', 'Well done',
                      'Whee', 'Woo hoo', 'Yay', 'Wowza', 'Yowsa']

WRONG_SPEECHCONS = ['Argh', 'Aw man', 'Blarg', 'Blast', 'Boo', 'Bummer',
                    'Darn', "D'oh", 'Dun dun dun', 'Eek', 'Honk', 'Le sigh',
                    'Mamma mia', 'Oh boy', 'Oh dear', 'Oof', 'Ouch', 'Ruh roh',
                    'Shucks', 'Uh oh', 'Wah wah', 'Whoops a daisy', 'Yikes']

MAX_QUESTIONS = 10

BAD_ANSWER = (
    "I'm sorry. {} is not something I know very much about in this skill.")

FALLBACK_ANSWER = (
    "Sorry. I can't help you with that. {}".format(HELP_MESSAGE))
