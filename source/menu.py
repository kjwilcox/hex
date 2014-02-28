import pygame
from pygame.locals import *

import jukebox
import exhibition
import collision

# game classes
import HvH1
import HvHn
# NYI
#import HvC
import how


class Menu():
    """ The main menu class for the Hex program. """

    def __init__(self):

        print "initializing program"
        pygame.display.init()

        print "pre-rendering fonts"
        pygame.font.init()
        self.font = "DejaVuSans.ttf"
        self.current_font = pygame.font.Font(self.font, 40)
        self.menu_text = {}
        self.menu_text["HvH1"] = (
            self.current_font.render("Human vs. Human (same computer)",
                True, (0,10,0)), (40, 200))
        self.menu_text["HvHn"] = (
            self.current_font.render("Human vs. Human (networked)",
                True, (0,10,0)), (40, 260))
        self.menu_text["HvC"] = (
            self.current_font.render("Human vs. Computer",
                True, (0,10,0)), (40, 320))
        self.menu_text["how"] = (
            self.current_font.render("How to play",
                True, (0,10,0)), (40, 380))
        self.menu_text["music"] = (
            self.current_font.render("Toggle music",
                True, (0,10,0)), (40, 440))
        self.menu_text["exit"] = (
            self.current_font.render("Exit Game",
                True, (0,10,0)), (40, 500))

        print "precalculating collision grid"
        self.collision = collision.generate_collision_grid()

        print "loading resources"
        self.images = exhibition.load_images()
        self.sounds = jukebox.Jukebox()

        pygame.display.set_caption("Hex")
        pygame.display.set_icon(self.images["icon"])

        print "opening window"
        self.screen = pygame.display.set_mode((800, 600))

        print "optimizing images"
        exhibition.optimize(self.images)

        print "ready!"

        # start the music
        if self.sounds.music != []:
            self.sounds.play_music()

    def __del__(self):
        """ Stuff to do when we are totally done. """

        self.sounds.stop_music()

        # finished with pygame, make sure the window gets closed
        pygame.quit()


    def main_loop(self):
        """ The main loop of the program. This actually runs the menu."""

        self.choice = None
        self.hover = None
        self.mouse = (0, 0)

        while self.choice != "exit":

            # update mouse info
            self.handle_mouse_hover()
            
            # do the event processing
            self.handle_events()

            # render menu screen
            self.render()

            # user has clicked something, do it!
            if self.choice not in [None, "exit"]:
                self.do_choice()

            # share the processor a little bit
            pygame.time.wait(10)


    def do_choice(self):
        """ Executes the player's choice. """

        # pack up data to pass to the game
        self.data = {"images": self.images, "sounds": self.sounds,
                "font": self.font, "screen": self.screen,
                "collision": self.collision}

        # create and play a game
        if self.choice == "HvH1":
            result = HvH1.HvH1(self.data).play()
        elif self.choice == "HvHn":
            #result = HvHn.HvHn(self.data).play()
            result = None
        elif self.choice == "HvC":
            result = None
        elif self.choice == "how":
            result = how.How(self.data).play()
        elif self.choice == "music":
            result = None
            if self.sounds.music_playing:
                self.sounds.stop_music()
                print "music stopped"
            elif self.sounds.music != []:
                self.sounds.play_music()
                
        else:
            raise NotImplementedError, "unknown choice!"

        # handle quit requests from a game
        if result == "kill":
            self.choice = "exit"
        else:
            self.choice = None


    def handle_events(self):
        """ Takes care of system events and mouse. """

        for event in pygame.event.get():
            if event.type == QUIT:
                self.choice = "exit"
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.choice = "exit"
            if event.type == MOUSEBUTTONUP and event.button == 1:
                self.choice = self.hover

        
    def handle_mouse_hover(self):
        """ Determines what the mouse is hovering over. """
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.hover = None
        
        for key in self.menu_text:
            image, location = self.menu_text[key]
            rect = image.get_rect()
            rect = rect.move(0, location[1])
            rect.w = 800 # fill the whole row

            if rect.collidepoint(mouse_x, mouse_y):
                self.hover = key
                return


    def render(self):
        """ Renders the main menu. """

        # Empty background for now
        self.screen.fill((240,240,240))

        # pretty hex logo
        rect = self.images["logo"].get_rect(center=(400,105))
        self.screen.blit(self.images["logo"], rect)

        # highlight the menu item
        if self.hover:
            image, pos = self.menu_text[self.hover]
            pos = (0, pos[1]-10) # magic number offset, looks better
            self.screen.blit(self.images["menu_hover"], pos)
            
        # cute hack for easy menu placement
        for image, location in self.menu_text.itervalues():
            self.screen.blit(image, location)

        #update screen
        pygame.display.flip()
