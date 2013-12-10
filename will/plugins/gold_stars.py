from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class GoldStarPlugin(WillPlugin):

    @respond_to("award (?P<num_stars>\d)+ gold stars? to (?P<user_name>.*)")
    def gold_stars(self, message, num_stars=1, user_name=None):
        stars = self.load("gold_stars", {})
        if user_name in stars:
            stars[user_name] += num_stars
        else:
            stars[user_name] = num_stars

        self.save("gold_stars", stars)

        self.saymessage, ("Awarded %s stars to %s." % (num_stars, user_name))