from .rules import RULES

class SuggestionService:

    @staticmethod
    def suggest(message):

        text = message.lower()

        for keyword, reply in RULES.items():

            if keyword in text:

                return reply

        return "Thank you for contacting us."