# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util import LOG
from twilio.rest import Client
import time


__author__ = 'btotharye'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.



# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class ItemSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ItemSkill, self).__init__(name="ItemSkill")

    @intent_handler(IntentBuilder('BlanketIntent').require('Action').require('Item'))
    def handle_blanket_intent(self, message):
        self.blanket = False
        action = message.data.get('Action')
        item = message.data.get('Item')
        if action:
            if 'blanket' in item:
                self.speak('It seems like you want a blanket, is that correct?', expect_response=True)
                self.set_context('BlanketContext')

    @intent_handler(IntentBuilder('YesBlanketIntent').require("Yes").
                    require('BlanketContext').build())
    def handle_yes_blanket_intent(self, message):
        self.speak('Ok we have a blanket on its way to you.')
        LOG.debug("The enclosure is: {}".format(self.config_core['enclosure'].get('platform', 'git_install')))
        if self.config_core['enclosure'].get('platform', 'git_install') == 'mycroft_mark_1':
            self.enclosure.deactivate_mouth_events()
            self.enclosure.mouth_text("Blanket on its way")
            time.sleep((self.LETTERS_PER_SCREEN + len("Blanket on its way")) * self.SEC_PER_LETTER)
            self.enclosure.activate_mouth_events()
            self.enclosure.mouth_reset()

        '''
        #self.speak('Found room: {}'.format(self.settings['room_number']))
        account_sid = self.settings['account_sid']
        auth_token = self.settings['auth_token']
        from_number = self.settings['from_number']
        to_number = self.settings['to_number']
        client = Client(account_sid, auth_token)
        message = client.messages.create(
             to= to_number,
             from_= from_number,
             body="Room: {} would like a blanket".format(self.settings['room_number']))
        LOGGER.debug("This is the message: {}".format(message))
        '''

    @intent_handler(IntentBuilder('NoBlanketIntent').require('No').build())
    def handle_no_blanket_intent(self, message):
        self.speak('Ok it seems you do not want a blanket')





# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ItemSkill()

