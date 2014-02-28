import game

import pygame
from pygame.locals import *

import random

class HvH1(game.Game):
    """ A local game between two humans. """
    
    def __init__(self, menu_data):

        game.Game.__init__(self, menu_data)

        pygame.display.set_caption("Hex: Human vs. Human (single computer)")

        self.current_font = pygame.font.Font(self.font, 44)
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
        self.text["click"] = (
            self.current_font.render("Click to continue...",
                True, (10, 10, 10)), (50, 530))

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
                    x, y = self.hover
                    if not self.data.get(x, y): # the spot is empty!
                        self.data.move(x, y, self.player)
                        self.switch_players()


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


    def play(self):
        """ The main loop, actually plays the game of Hex. """

        # pick a random starting player for fairness
        self.player = random.randint(1,2)
        self.status = "playing"
        
        while self.status == "playing":

            # updates mouse position/hover
            self.update_mouse()

            # handle window events and players' moves
            self.handle_events()

            # check for win
            result = self.get_victory()
            if result:
                self.status = result
                break

            # render the screen
            self.render()

            # share the processor
            pygame.time.wait(10)

        # show game over stuff if we aren't quitting early
        if self.status not in ["kill", "quit"]:
            self.render_game_over()
            self.wait_for_click()

        return self.status
