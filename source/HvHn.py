import game

import pygame
from pygame.locals import *

import datetime
import random
import urllib
import os

        
def get_computer_name():
    """
    Returns the user-given name for the computer.
    Should work for windows and linux, etc.
    """
    
    comp_name = None
    
    if os.name is 'nt': # windoze
        comp_name = os.getenv('COMPUTERNAME')
    else: # uh, hopefully everything else...
        comp_name = os.getenv('HOSTNAME')
        
    if comp_name is None: # ;-;
        return "UNKNOWN_COMPUTER"
    
    return comp_name

class NetworkError(Exception):
    def __init__(self, value):
        self.value
    def __str__(self):
        return repr(self.value)

class HvHn(game.Game):
    """ A local game between two humans. """
    
    def __init__(self, menu_data):
        game.Game.__init__(self, menu_data)

        pygame.display.set_caption("Hex: Human vs. Human (networked)")

        self.current_font = pygame.font.Font(self.font, 48)
        self.text = {}
        
        # render needed text ahead of time
        self.text["red"] = (
            self.current_font.render("Red player's turn",
                True, (200, 0, 0)), (50, 20))
        self.text["blue"] = (
            self.current_font.render("Blue player's turn",
                True, (0, 0, 200)), (50, 20))
        self.text["hor"] = (
            self.current_font.render("(attempting horizontal chain)",
                True, (200, 10, 10)), (50, 530))
        self.text["vert"] = (
            self.current_font.render("(attempting vertical chain)",
                True, (10, 10, 200)), (50, 530))
        self.text["red_wins"] = (
            self.current_font.render("Red player is victorious!",
                True, (200, 0, 0)), (50, 20))
        self.text["blue_wins"] = (
            self.current_font.render("Blue player is victorious!",
                True, (0, 0, 200)), (50, 20))
        self.text["you_red"] = (
            self.current_font.render("You have been selected as the red player.",
                True, (200, 0, 0)), (50, 20))
        self.text["you_blue"] = (
            self.current_font.render("You have been selected as the blue player.",
                True, (0, 0, 200)), (50, 20))
        self.text["opponents:"] = (
            self.current_font.render("Available Opponents:",
                True, (10, 10, 10)), (150, 10))
        self.text["click"] = (
            self.current_font.render("Click to continue...",
                True, (10, 10, 10)), (50, 530))

        # get a smaller font
        self.current_font = pygame.font.Font(self.font, 40)

    def render_opponents(self):
        """ Renders the list of opponents. Also handles hover. """

        # empty bg
        self.screen.fill((240, 240, 240))

        # title
        image, pos = self.text["opponents:"]
        self.screen.blit(image, pos)

        # opponents
        for opponent in self.opponent_fonts:
            name, ip = self.opponent_fonts[opponent]
            if self.hover == opponent:
                image, pos = name
                image = self.images["menu_hover"]
                pos = (0, pos[1])
                self.screen.blit(image, pos)
            image, pos = name
            self.screen.blit(image, pos)
            image, pos = ip
            self.screen.blit(image, pos)

        pygame.display.flip()

    def render(self):
        """ Renders the playing field. """

        # Empty background for now
        self.screen.fill((240,240,240))

        # render the... grid and text
        self.render_grid()
        self.render_text()

        # update window
        pygame.display.flip()

    def render_text(self):
        """ Renders the appropriate text messages. """

        if self.player is 1:
            image, pos = self.text["red"]
            self.screen.blit(image, pos)
            image, pos = self.text["hor"]
            self.screen.blit(image, pos)
        else: #self.player is 2
            image, pos = self.text["blue"]
            self.screen.blit(image, pos)
            image, pos = self.text["vert"]
            self.screen.blit(image, pos)

    def render_game_over(self):
        """ Renders game over screen. """

        # Empty background for now
        self.screen.fill((240,240,240))

        # figure out who the winner was
        winner = self.status

        # blit appropriate winner message
        if winner is 1:
            image, pos = self.text["red_wins"]
            self.screen.blit(image, pos)
        else: #self.player is 2
            image, pos = self.text["blue_wins"]
            self.screen.blit(image, pos)

        # render the grid
        self.render_grid()

        # render "click to continue" message
        image, pos = self.text["click"]
        self.screen.blit(image, pos)

        # update screen
        pygame.display.flip()

    def handle_events(self):
        """ Handles events, including moves. """

        for event in pygame.event.get():
            if event.type == QUIT:
                self.status = "kill"
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.status = "quit"
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if self.hover: # we clicked on something!
                    pass

    def handle_mouse_hover(self):
        """ Handle hover """

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.hover = None
        
        for key in self.opponent_fonts:
            image, location = self.opponent_fonts[key][0]
            rect = image.get_rect()
            rect = rect.move(0, location[1])
            rect.w = 800 # fill the whole row

            if rect.collidepoint(mouse_x, mouse_y):
                self.hover = key
                return

    def wait_for_click(self):
        """ Waits for a mouse click. Or a keypress..."""

        while True:
            event = pygame.event.poll()
            if event.type == QUIT:
                self.status = "kill"
                break
            if event.type == KEYDOWN:
                break
            if event.type == MOUSEBUTTONUP and event.button == 1:
                break

            # share processor
            pygame.time.wait(10)


    def contact_server(self):
        """ The main loop, actually plays the game of Hex. """

        comp_name = get_computer_name().strip()

        try:
            # tell the server that we are looking to play
            result = urllib.urlopen(
                "http://kwilco.net/match/game.php?" +
                urllib.urlencode( (
                    ('n', comp_name),
                    ('g', 'hex'),
                    ('v', '0.1a')
                    ))).read()
        except:
            raise NetworkError, "failed to contact server"

        if result != "OK":
            raise NetworkError, "server could not handle request"
            
        try:
            raw_opponents = urllib.urlopen(
                "http://kwilco.net/match/game.php?m=2&g=hex&v=0.1a"
                ).readlines()
        except:
            raise NetworkError, "failed to contact server"

        # remove self from listing
        opponents = []
        for opponent in raw_opponents:
            ip = opponent.split(' ')[0]
            name = ' '.join(opponent.split(' ')[1:]).strip()

            if comp_name != name:
                opponents.append((name, ip))
            else:
                print "You are on the list:", comp_name
            
        return opponents

    def play(self):
        """ The main loop, actually plays the game of Hex. """

        print "made it to play"

        self.status = "getting opponents"

        # their first check was reeealy long ago
        last_check = datetime.datetime(2001, 1, 1)
        self.opponent_fonts = {}
        self.opponents_uptodate = False

        while self.status == "getting opponents":

            if datetime.datetime.now() - last_check > \
                       datetime.timedelta(seconds=10):
                last_check = datetime.datetime.now()
                try:
                    #opponents = self.contact_server()
                    opponents = [('kyle', '69.29.172.63'),
                                 ('satan', '66.6.6.66'),
                                 ('jesus', '7.7.7.7'),
                                 ('buddha', '0.0.0.0')]
                    self.opponents = opponents
                    top = 75
                    for name, ip in opponents:
                        self.opponent_fonts[ip] = (
                            (self.current_font.render(name,
                                True, (10, 10, 10)), (50, top)),
                            (self.current_font.render(ip,
                                True, (10, 10, 10)), (400, top)),
                            )
                        top += 50
                except NetworkError, (a, b):
                    print "could not connect to server", a, b
                print "contacted server, opponents:",
                print opponents

            self.handle_events()

            self.handle_mouse_hover()

            self.render_opponents()

            pygame.time.wait(10)

        if self.status in ["quit", "kill"]:
            return self.status



        
