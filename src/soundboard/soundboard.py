"""
this is the main entry point for the soundboard software.

It should be set to run on boot up. It will set some button listeners that will control the whole shebang
"""

"""
the basic plan:
    - we need an object to store the options used. this object needs to be passed to all i/o objects
        - maybe I should use callbacks to notify of the different options?
        - there will be one button that controls the options, with N different options profiles
    - we need some i/o objects
        - button processors to link to inputs (buttons) and take a callback as an option
        - there will be two types of buttons:
            - triggers that will cause sounds to go
            - triggers that will cause options or profiles to change
        - LED proccessor to link to outputs (LEDS). these will be driven by button events
        - sound processor to define the sounds and trigger them

"""
import logging
logging.basicConfig(level=logging.DEBUG)

from ext_interfaces import buttons, leds, oled
from soundboard import profiles, sounds

import os
import random
import time
import toml
import socket

class DiceTower(object):
    """manage everything"""
    # how many sound board items are there?
    SND_BRD_CNT = 6

    # modes
    SINGLE = "single"
    SEQUENTIAL = "sequential"
    RANDOM = "random"

    CFGFILE = "/home/pi/.config/soundboard/soundboard.toml"
    PROFILEDIR = "/home/pi/sounds"
    
    def __init__(self):
        # init all the vars
        self.lgr = logging.getLogger('soundboard')
        self.lgr.info("logger setup complete")
        self.smg = None
        self.profile = None
        self.buttons = {}
        self.leds = []
        self.btn_type_data = None
        self.starts = []
        self.btn_tys = {}

        # load the config
        self.cfg = self.read_cfg()
        
        # load the sounds
        self.load_profile()

        self.load_sound_manager()

        self.load_buttons()

        # load the leds
        self.load_leds()

        # TODO connect to slack
        self.slack_mgr = None
        self.load_slack_api()

        # print some debug data
        self.lgr.debug("self.btn_type_data = {}".format(self.btn_type_data))
        self.lgr.debug("self.btn_tys = {}".format(self.btn_tys))

    def load_profile(self):
        """
        prepare the data structures and actually load the sounds needed
        """
        # load the profile first
        self.profile = profiles.Profile(self.PROFILEDIR)
        self.lgr.info("profile loaded")

        # get a comprehensive list of button types
        cats = self.config["buttons"]
        cats.remove("sb")
        for i in range(6):
            cats.append("sb{}".format(i))

        # for each button type, link the physical buttons
        for cat in cats:
            if cat not in self.profile.sounds:
                self.lgr.info("couldn't load button type {} from config - profile doesn't support it".format(cat))
                continue

            if cat[:2] == "sb":
                i = int(cat[-1])
                buttons = [sorted(self.config["buttons"]["sb"])[i]]
                self.profile.assign_buttons(cat, buttons)
            else:
                self.profile.assign_buttons(cat, self.config["buttons"][cat])

        if self.cfg['SOUNDBOARD'] in self.profile.sounds["sb0"]:
            self.profile.cur_sb = self.cfg['SOUNDBOARD']
        else:
            self.profile.cur_sb = random.choice(list(self.profile.sounds["sb0"].keys()))
            self.update_cfg('SOUNDBOARD', self.profile.cur_sb)

    def read_cfg(self):
        """read the config from file"""
        return toml.load(self.CFGFILE)

    def write_cfg(self):
        """write the config to file"""
        toml.dump(self.CFGFILE)

    def update_cfg(self, key, val):
        """update the config value, effect the change and write the change to file"""
        self.config[key] = val
        self.write_cfg()

    def load_buttons(self):
        """loads all the buttons and assigns functions to them"""
        for b in self.btn_tys:
            self.buttons[b] = buttons.Button(b)
            self.buttons[b].setup_event(self.play_sound)
        
            self.lgr.info("button {} loaded as {}".format(b, self.btn_tys[b]))

    def load_leds(self):
        self.lgr.info("no leds loaded - function not implemented")
   
    def load_sound_manager(self):
        self.smg = sounds.SoundMgr()

        for s_name in sorted(self.profile.crits):
            s = self.profile.crits[s_name]
            self.lgr.info("loading crit sound {}".format(s))
            self.smg.add_sound(s)
            self.btn_type_data["sounds"]["crit"].append(s_name)
        
        for s_name in sorted(self.profile.fails):
            s = self.profile.fails[s_name]
            self.lgr.info("loading fail sound {}".format(s))
            self.smg.add_sound(s)
            self.btn_type_data["sounds"]["fail"].append(s_name)

        for s_name in sorted(self.profile.starts):
            s = self.profile.starts[s_name]
            self.lgr.info("loading startup sound {}".format(s))
            self.smg.add_sound(s)
            self.starts.append(s_name)
        
        for sb_name, sb in self.profile.soundboards.items():
            i = 0
            for s_name in sorted(self.profile.soundboards[sb_name]):
                s = self.profile.soundboards[sb_name][s_name]
                self.lgr.info("loading sound {} into soundboard {}".format(s_name, sb_name))
                self.smg.add_sound(s)
                self.btn_type_data["sounds"]["sb{}".format(i)].append(s_name)
                i += 1

        self.lgr.info("sound manager is now loaded")
        self.lgr.debug("sound manager has sounds: {}".format(self.smg.sounds))

    def load_slack_api(self):
        self.lgr.info("slack manager not loaded - function not implemented")
  
    def play_sound(self, btn_id):
        """dynamically figure out what type of sound to play"""
        ty = self.btn_tys[btn_id]
        last = self.btn_type_data["last"][ty]
        count = self.btn_type_data["count"][ty]
        sound_lib = self.btn_type_data["sounds"][ty]

        # if it's a sb (or SINGLE mode) - play the same files over and over
        mode = self.get_mode(ty)
        if mode == self.SINGLE:
            num = last
        elif mode == self.SEQUENTIAL:
            num = last + 1
            if num == len(count):
                num = 0
        elif mode == self.RANDOM:
            num = random.randrange(len(count))

        self.lgr.info("playing {} sound for btn {}".format(ty, btn_id))
        self.lgr.debug("last was {}, this is {}, {} {}s available".format(
           last, num, count, ty))
            
        self.smg.play_sound(sound_lib[num], self.cfg['mode']['stop'])

    def play_startup(self):
        """play a random start sound"""
        sname = random.choice(self.starts)
        self.smg.play_sound(sname, self.cfg['mode']['stop'])

    def get_mode(self, ty):
        """get the operating mode based on the type"""
        if ty[:2] == "sb":
            return self.SINGLE
        else:
            return self.cfg["mode"][ty]

    def change_sb(self, sb):
        # first get the new soundboard name and sounds
        self.sbnum += 1
        if self.sbnum == len(self.profiles.soundboards):
            self.sbnum = 0

        self.lgr.info("changing soundboard to {}".format(self.profiles.soundboards[self.sbnum])

        for b in self.btn_type_data["last"]:
            self.btn_type_data["last"][b] = self.sbnum

        # second, update the oled
        self.oled.write_screen(sb_deets)

    def main_loop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 31415))
        done = False
        while not done:
            # TODO add a udp socket here to ease debugging
            data, address = s.recvfrom(1024)
            data = data.encode()
            self.lgr.info("msg from {}: {}".format(adress[0], data))
            data = data.split(" ")
            if data[0] == "stop":
                done = True
            elif data[0] == "play":
                pass
            elif data[0] == "mode":
                pass
            elif data[0] == "load":
                if len(data) < 2:
                    self.lgr.info("couldn't load anything - need an arg")
                else:
                    if data[1] in ["proflie", "all"]:
                        self.load_profile()
                    if data[1] in ["sounds", "all"]:
                        self.load_sound_manager()

def entry():
    # init the sound controller
    dt = DiceTower()
    dt.play_startup()
    dt.main_loop()

if __name__ == "__main__":
    entry()
