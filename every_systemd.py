from mastodon import Mastodon
import sys
import json
import random


class EverySystemd:
    mastodon = None
    debug_mode = None
    word_max_tries = None
    default_cn = ""

    def __init__(self, debug_mode):
        try:
            settings = json.load(open('settings.json'))
            self.mastodon = Mastodon(
                access_token=settings['mastodon_access_token'],
                api_base_url=settings['mastodon_url'],
                debug_requests=debug_mode
            )
            self.word_max_tries = settings['random_word_max_tries']
            self.debug_mode = debug_mode
            self.word_list = json.load(open('dict.json'))
            self.default_cn = settings["default_cn"]
        except IndexError:
            print("[ERROR] settings.json was not found or didn't contain all needed values. Please check if it is "
                  + "configured properly")
            sys.exit(1)

    def do_shitpost(self):
        word = self.get_random_word()
        cn = self.get_cn(word)
        self.mastodon.status_post(status="systemd-" + word[0] + "d", spoiler_text=cn,
                                  language="En", visibility="unlisted")

    def get_cn(self, word):
        try:
            cn = self.default_cn + ", " + word[1],
        except IndexError:
            cn = self.default_cn
        return cn

    def get_random_word(self):
        random_word = 'None'
        tries = 0
        while random_word == 'None' or tries >= self.word_max_tries or random_word[len(random_word) - 1] == 'd':
            random_word = self.word_list[random.randint(0, len(self.word_list) - 1)]
            tries += 1
        if tries == self.word_max_tries:
            print("[ERROR] Could not come up with a word within " + str(self.word_max_tries) + " attempts.")
            sys.exit(1)
        return random_word


if __name__ == '__main__':
    try:
        debug_mode_input = bool(sys.argv[1])
    except IndexError:
        debug_mode_input = False
    except ValueError:
        print('Expecting attr1 to be of type bool. Something that could not be converted to bool given. \n'
              + 'Running in debug mode for safety')
        debug_mode_input = True
    bot = EverySystemd(debug_mode_input)
    bot.do_shitpost()
