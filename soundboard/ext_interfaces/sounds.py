import logging
import pygame
from ext_interfaces import adafruitAmp
import os
import time

logging.info("loading dicetower.sounds")

class SoundMgr(object):
    def __init__(self):
        self.lgr = logging.getLogger('profilemgr')
        pygame.mixer.quit()
        pygame.mixer.pre_init(16000, -16, 1, 512)
        pygame.mixer.init()
        
        # TODO get rid of specific sounds, put everything into one dict
        self.sounds = {}
        # connect to the amp and set the volume
        try:
            self.amp = adafruitAmp.Amp()

            self.amp.set_gain(29)
        except OSError as e:
            self.lgr.info("couldn't find the amp... try connecting it")

    
    def add_sound(self, path):
        s = Sound(len(self.sounds), file=path)
        if s.fname in self.sounds:
            self.lgr.info("{} was previously loaded from {}, replacing with {}".format(s.fname, self.sounds[s.fname].path, s.path))
        self.sounds[s.fname] = pygame.mixer.Sound(path)

    def play_sound(self, fname, stop=False):
        # TODO stop any currently playing sounds
        if stop:
           self.stop_all()
        if fname in self.sounds:
            self.lgr.info("playing file {}".format(fname))
            self.sounds[fname].play()
        else:
            self.lgr.info("couldn't play {}: not in sound lib".format(fname))

    def play_sound_by_num(self, num, stop=False):
        for s in self.sounds:
            if s.num == num:
                self.play_sound(s.fname, stop=stop)

    def stop_all(self):
        pygame.mixer.fadeout(10)

    def clear_all(self):
        self.sounds = {}

class Sound(pygame.mixer.Sound):
    """
    this holds a pygame sound and info about it
    """
    def __init__(self, num, **kwds):
        if 'file' not in kwds:
            raise TypeError("file keyname arg must be provided")
        self.path = kwds.get("file")
        self.fname = os.path.basename(self.path)
        self.num = num
        super().__init__(**kwds)


if __name__ == "__main__":
    s = SoundMgr()
    root = "/home/pi/DiceTower/modes/mario/"
    for p in os.listdir(root + "crits"):
        s.add_sound(os.path.join(root, "crits", p))
        print("loaded new sound {} from {}".format(p, s.sounds[p].path))
    
    for p in os.listdir(root + "fails"):
        s.add_sound(os.path.join(root, "fails", p))
        print("loaded new sound {} from {}".format(p, s.sounds[p].path))

    for p in os.listdir(root + "startup"):
        s.add_sound(os.path.join(root, "startup", p))
        print("loaded new sound {} from {}".format(p, s.sounds[p].path))

    for c in s.sounds:
        s.play_sound(c)
        time.sleep(s.sounds[c].get_length())
