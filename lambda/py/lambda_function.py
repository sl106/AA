# -*- coding: utf-8 -*-

# IMPORTANT: Please note that this template uses Display Directives,
# Display Interface for your skill should be enabled through the Amazon
# developer console
# See this screen shot - https://alexa.design/enabledisplay

import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
    get_plain_text_content, get_rich_text_content)

from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective, ListTemplate1,
    BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response

from alexa import data, util

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        attr = handler_input.attributes_manager.session_attributes
        attr["status"] = "player number"
        message = data.WELCOME_MESSAGE
        if util.time_of_the_day() == "morning":
            message += "Damn, isn't it a bit early to be drinking? No judgement here though. "
        elif util.time_of_the_day() == "afternoon":
            message += "<prosody pitch=\"x-high\">Now day drinking is something I can get behind. </prosody>"
        elif util.time_of_the_day() == "evening":
            message += "Let's partaaayyyy! "
        else:
            message += "As my good friend, Paul, once said: <voice name=\"Joey\"><lang xml:lang=\"en-US\"> Let's get schwasted! </lang></voice> "
        
        message = message + data.REPROMPT_PLAYERNO.format(util.this_time_of_the_day())

        handler_input.response_builder.speak(message).ask(
            data.REPROMPT_PLAYERNO.format(util.this_time_of_the_day()))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(
            handler_input.request_envelope))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session

        handler_input.response_builder.speak(
            data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        if attr["round_no"] < 3:
            message = "Woah, you only played {} rounds!? Do we have some lightweights here? "
        else:
            message = "Good job! I hope you're all boozed up now! "
        message = message + data.EXIT_SKILL_MESSAGE.format(util.time_of_the_day)
        handler_input.response_builder.speak(message).set_should_end_session(True)
        return handler_input.response_builder.response


class PlayerNumberIntentHandler(AbstractRequestHandler):
    """Handler for providing the number of players playing"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("PlayerNumberIntent")(handler_input) and attr.get("status") == "player number"

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlayerNumberIntentHandler")
        attr = handler_input.attributes_manager.session_attributes

        attr["player_no"] = handler_input.request_envelope.request.intent.slots["player_number"].value
        attr["checked_single_player"] = False
        if int(attr["player_no"]) == 1 and not attr["checked_single_player"]:
            attr["checked_single_player"] = True
            handler_input.response_builder.speak(
                data.SINGLE_PLAYER_MESSAGE + data.REPROMPT_PLAYERNO.format(util.this_time_of_the_day())).ask(data.REPROMPT_PLAYERNO.format(util.this_time_of_the_day()))
        else:
            attr["status"] = "collecting names"
            attr["players_collected"] = 0
            attr["player_names"] = []
                
            handler_input.response_builder.speak(
                data.GET_PLAYERNAME + "1?").ask(data.GET_PLAYERNAME + "1?").set_should_end_session(False)
        return handler_input.response_builder.response


class PlayerNameIntentHandler(AbstractRequestHandler):
    """Handler for collecting the names of the players playing"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("PlayerNameIntent")(handler_input) and attr.get("status") == "collecting names"

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlayerNumberIntentHandler")
        attr = handler_input.attributes_manager.session_attributes

        attr["players_collected"] = int(attr["players_collected"]) + 1
        attr["player_names"].append(handler_input.request_envelope.request.intent.slots["player_name"].value)

        if int(attr["players_collected"]) == int(attr["player_no"]):
            attr["status"] = "picking theme"
            attr["round_no"] = 1
            text = data.START_QUIZ_MESSAGE + str(attr["round_no"]) + "? " + data.LIST_THEMES
            handler_input.response_builder.speak(text).ask(text)
        else:
            current = int(attr["players_collected"])
            current += 1
            current = str(current)
            handler_input.response_builder.speak(data.GET_PLAYERNAME + current + "?").ask(
                data.GET_PLAYERNAME + current + "?")

        return handler_input.response_builder.response


class ThemeOptionIntentHandler(AbstractRequestHandler):
    """Handler to select the theme option for the round"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("ThemeOptionIntent")(handler_input) and attr.get("status") == "picking theme"

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ThemeOptionIntentHandler")
        attr = handler_input.attributes_manager.session_attributes
        attr["status"] = "question"
        attr["current_theme"] = handler_input.request_envelope.request.intent.slots["theme"].value.lower()
        attr["current_qno"] = 1

        playername = util.get_recipient(attr)
        attr["current_player"] = playername

        attr["quiz_item"] = util.get_item(attr)
        question = util.get_question(attr["quiz_item"])
        question_text = playername + ", " + question
        handler_input.response_builder.speak(question_text).ask(
            playername + ", do you have an answer? The question was: " + question)

        return handler_input.response_builder.response


class NewThemeHandler(AbstractRequestHandler):
    """Handler for changing the theme or moving to the next round."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("NewThemeIntent")(handler_input) or
                is_intent_name("AMAZON.StartOverIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NewThemeHandler")
        attr = handler_input.attributes_manager.session_attributes

        attr["status"] = "picking theme"
        attr["round_no"] = attr["round_no"] + 1
        text = data.NEXT_ROUND_MESSAGE + str(attr["round_no"]) + ". " + data.LIST_THEMES
        handler_input.response_builder.speak(text).ask(text)

        return handler_input.response_builder.response


class UnsureAnswerHandler(AbstractRequestHandler):
    """Handler for when the user doesn't give a definitive answer"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("UnsureIntent")(handler_input) and
                attr.get("status") == "question")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In QuizAnswerHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder

        item = attr["quiz_item"]
        speech = "Well that's a shame. The answer was {}".format(item[1])
        task = util.generate_forfeit(attr, attr["current_player"])

        resp = speech + "! " + task

        if attr['current_qno'] < data.MAX_QUESTIONS:
            # Ask another question
            attr["current_qno"] = attr["current_qno"] + 1
            attr["status"] = "question"

            # Generates new player to ask
            playername = util.get_recipient(attr)
            attr["current_player"] = playername

            # Generates new question
            attr["quiz_item"] = util.get_item(attr)
            question = util.get_question(attr["quiz_item"])
            question_text = resp + " Time for the next question! " + playername + ", " + question
            handler_input.response_builder.speak(question_text).ask(
                playername + ", do you have an answer? The question was: " + question)

            return handler_input.response_builder.response
        else:
            # Start new round
            attr["status"] = "picking theme"
            attr["round_no"] = attr["round_no"] + 1
            text = data.NEXT_ROUND_MESSAGE + str(attr["round_no"]) + ". " + data.LIST_THEMES
            handler_input.response_builder.speak(resp + " " + text).ask(text)

            return handler_input.response_builder.response


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if attr["status"] == "question":
            question = util.get_question(attr["quiz_item"])
            response_builder.speak(question).ask(attr["current_player"] + ", <emphasis level=\"strong\"> do you have an answer?  The question was: </emphasis>" + question)
            return response_builder.response
        elif "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)

            return response_builder.response


class QuizAnswerHandler(AbstractRequestHandler):
    """Handler for answering the quiz.

    The ``handle`` method will check if the answer specified is correct,
    by checking if it matches with the corresponding session attribute
    value. According to answer, alexa responds to the user
    with either the next question, next round or a forfeit.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (not is_intent_name("NewThemeIntent")(handler_input) and
                not is_intent_name("AMAZON.CancelIntent")(handler_input) and
                not is_intent_name("AMAZON.StopIntent")(handler_input) and
                not is_intent_name("AMAZON.PauseIntent")(handler_input) and
                not is_intent_name("AMAZON.HelpIntent")(handler_input) and
                not is_intent_name("UnsureIntent")(handler_input) and
                not is_intent_name("AMAZON.FallbackIntent")(handler_input) and
                attr.get("status") == "question")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In QuizAnswerHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder

        item = attr["quiz_item"]
        user_ans = handler_input.request_envelope.request.intent.slots

        if util.check_answer(user_ans, item[1]):
            speech = util.get_speechcon(correct_answer=True)
            task = util.generate_task(attr, attr["current_player"])
        else:
            speech = util.get_speechcon(correct_answer=False) + "! <emphasis level=\"strong\"> The answer was </emphasis>" + item[1]
            task = util.generate_forfeit(attr, attr["current_player"])

        resp = speech + "! " + task

        if attr['current_qno'] < data.MAX_QUESTIONS:
            # Ask another question
            attr["current_qno"] = attr["current_qno"] + 1
            attr["status"] = "question"

            # Generates new player to ask
            playername = util.get_recipient(attr)
            attr["current_player"] = playername

            # Generates new question
            attr["quiz_item"] = util.get_item(attr)
            question = util.get_question(attr["quiz_item"])
            question_text = resp + " Time for the next question! " + playername + ", " + question
            handler_input.response_builder.speak(question_text).ask(playername + ", do you have an answer? The question was: " + question)

            return handler_input.response_builder.response
        else:
            # Start new round
            attr["status"] = "picking theme"
            attr["round_no"] = attr["round_no"] + 1
            text = data.NEXT_ROUND_MESSAGE + str(attr["round_no"]) + ". " + data.LIST_THEMES
            handler_input.response_builder.speak(resp + " " + text).ask(text)

            return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.
     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        if attr["status"] == "question":
            message = "Sorry, I didn't understand that. We'll move on. "

            if attr['current_qno'] < data.MAX_QUESTIONS:
                # Ask another question
                attr["current_qno"] = attr["current_qno"] + 1
                attr["status"] = "question"

                # Generates new player to ask
                playername = util.get_recipient(attr)
                attr["current_player"] = playername

                # Generates new question
                attr["quiz_item"] = util.get_item(attr)
                question = util.get_question(attr["quiz_item"])
                question_text = message + " Time for the next question! " + playername + ", " + question
                handler_input.response_builder.speak(question_text).ask(playername + ", do you have an answer? The question was: " + question)

                return handler_input.response_builder.response
            else:
                # Start new round
                attr["status"] = "picking theme"
                attr["round_no"] = attr["round_no"] + 1
                text = data.NEXT_ROUND_MESSAGE + str(attr["round_no"]) + ". " + data.LIST_THEMES
                handler_input.response_builder.speak(message + " " + text).ask(text)

        else:
            handler_input.response_builder.speak(
                data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)

        return handler_input.response_builder.response




# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


# Exception Handler classes
class CatchInvalidThemeExceptionHandler(AbstractExceptionHandler):
    """Catch any issues with user selecting an invalid theme handler."""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return attr.get("status") == "picking theme"

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        speech = "Sorry, that's not one of the themes available. " + data.LIST_THEMES
        handler_input.response_builder.speak(speech).ask(data.LIST_THEMES)

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NewThemeHandler())
sb.add_request_handler(QuizAnswerHandler())
sb.add_request_handler(UnsureAnswerHandler())
sb.add_request_handler(PlayerNumberIntentHandler())
sb.add_request_handler(PlayerNameIntentHandler())
sb.add_request_handler(ThemeOptionIntentHandler())
sb.add_request_handler(RepeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchInvalidThemeExceptionHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()