import os
import sys
import logging
import toml


class CrapProfileDir(Exception):
    pass

class Profile():
    """
    this class represents the file side of the sound manager
    """
    REQ_SUBS = ["crit",
                "fail",
                "startup",
                "soundboard"]

    REQ_TOML = ["rgb.toml"]

    def __init__(self, dirname):
        """
        The main data variable here is self.sounds, which is a multilayered dict with the following structure
            cat - top level, the sound type (crit, fail, start, soundboard)
            subcat - applicable for soundboard only, this is the specific soundboard. for everything else, an empty string is used
            data_key - the 3rd level has a key for each type of info required:
                last_played - <int>, which is the last played sound
                sounds - <list, pygame.mixer.Sound>, sounds for the cat/subcat
                mode - <str>, what mode the sound is operating in
                buttons - <list, int>, which buttons are associated with this 
        """
        self.lgr = logging.getLogger('profilemgr')
        self.name =  ""
        self.dir = os.path.abspath(dirname)
        self.sounds = {}
        self.cur_sb = ""
        self.rgbs = []
        
        self.load()

    def load(self):
        """
        load the data into the main data storage variable
        """
        # set the dir and name
        self.name = os.path.basename(self.dir)
        self.lgr.info('loading profile {} from {}'.format(self.name, self.dir))

        #validate that we have the appropriate subdirs
        ls = os.listdir(self.dir)
        for sub in self.REQ_SUBS:
            if sub not in ls:
                raise CrapProfileDir("{} doesn't exist".format(os.path.join(self.dir, sub)))
        
        if not len(os.listdir(os.path.join(self.dir, 'soundboard'))) > 0:
            raise CrapProfileDir("no soundboard sub directories")

        # setup some of the var
        self.load_cats()

        # actually load the file names
        for d in ['crit', 'fail', 'startup']:
            self.setup_db(d, self.loadwavnames(os.path.join(self.dir,d)))
        
        for i in range(6):
            d = "sb{}".format(i)
            for sub in os.listdir(os.path.join(self.dir, 'soundboard')):
                self.setup_db(d, self.loadwavnames(os.path.join(self.dir,d,sub)), sub)
        
        # load the rgb conf file
        self.rgbs = self.loadrgbconf(os.path.join(self.dir,'rgbs.conf'))
    
    def setup_db(self, cat, sounds, subcat=""):
        if cat not in self.sounds:
            self.sounds[cat] = {}

        self.sounds[cat][subcat] = {}
        self.sounds[cat][subcat]["sounds"] = sounds
        self.sounds[cat][subcat]["last"] = len(sounds)
        self.sounds[cat][subcat]["mode"] = None
        self.sounds[cat][subcat]["buttons"] = []

    def assign_buttons(self, cat, buttons)
        for sub in self.sounds[cat]:
            self.sounds[cat][sub]["buttons"] = buttons

    def loadwavnames(self, dirname):
        # get the wav files in the dir
        ls = sorted(os.listdir(dirname))
        sounds = []

        for f in ls:
            if f[-3:].lower() != 'wav':
                continue

            sounds.append(f)
            self.lgr.info("found {} to load in profile".format(self.getfname(f)))

        return sounds

    def loadrgbconf(self, fname):
        """load the conf file that defines the RGB colours"""
        pass
        self.lgr.info("can't load conf - function not implemented")

    def getfname(self, cat, wav, subcat=""):
        """turn a cat and wav into a file name"""
        return os.path.join(cat, subcat, wav)

if __name__ == "__main__":
    p = Profile(sys.argv[1])
    print(p.sounds)
