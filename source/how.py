import game

import pygame
from pygame.locals import *

class How(game.Game):
    """ A local game between two humans. """
    
    def __init__(self, menu_data):
        game.Game.__init__(self, menu_data)

        pygame.display.set_caption("Hex: How to Play")

        self.current_font = pygame.font.Font(self.font, 48)
        self.text = {}
        # render needed text ahead of time
        self.text["click"] = (
            self.current_font.render("Click to continue...",
                True, (10, 10, 10)), (50, 530))

        self.current_font = pygame.font.Font(self.font, 22)


    def render(self):
        """ Renders the playing field. """

        # render the grid
        self.render_grid()

        # renders click text
        image, pos = self.text["click"]
        self.screen.blit(image, pos)

        # update window
        pygame.display.flip()


    def render_background(self):
        """ Renders the background. """
        
        # Empty background for now
        self.screen.fill((240,240,240))
        

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

    def handle_events(self):
        """ Handles events, including moves. """

        for event in pygame.event.get():
            if event.type == QUIT:
                self.status = "kill"
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.status = "quit"

    def play(self):
        """ The main loop, actually plays the game of Hex. """

        self.status = "play"

        self.render_background()
        self.screen.blit(self.current_font.render(
           "The game of Hex is played on a diamond shaped grid, shown below.",
                True, (10, 10, 10)), (10, 10))
        self.screen.blit(self.current_font.render(
            "Each player takes turns claiming hexagons.",
                True, (10, 10, 10)), (10, 34))
        self.screen.blit(self.current_font.render(
            "The goal is to create a chain of hexagons "
            "connecting two opposite sides.",
                True, (10, 10, 10)), (10, 58))
        self.render()
        self.wait_for_click()

        self.render_background()
        self.screen.blit(self.current_font.render(
           "The red player is trying to connect the sides, while the blue player",
                True, (10, 10, 10)), (10, 10))
        self.screen.blit(self.current_font.render(
            "is trying to connect the top and bottom.",
                True, (10, 10, 10)), (10, 34))
        self.screen.blit(self.current_font.render(
            "Try watching a game to see how it works. ",
                True, (10, 10, 10)), (10, 58))
        self.render()
        self.wait_for_click()

        self.player = 1

        for move in [(0,5),(5,5),(1,5),(4,4),(3,6),
                    (5,6),(4,6),(5,7),(4,3),(3,3),
                    (2,1),(2,2),(1,1),(1,2),(0,1),
                    (4,2),(3,2),(5,3),(5,4),(6,5),
                    (6,4),(7,4),(7,5),(8,6),(8,5),
                    (10,5),(9,5),(9,4),(10,6)]:

            x, y = move
            self.data.move(x, y, self.player)
            self.switch_players()

            self.render_background()
            self.render_grid()
            pygame.display.flip()

            self.handle_events()

            if self.status in ["kill", "quit"]:
                return self.status

            pygame.time.delay(400)

        self.render_background()
        self.screen.blit(self.current_font.render(
           "The red player has won this game, because he has formed a chain.",
                True, (10, 10, 10)), (10, 10))
        self.screen.blit(self.current_font.render(
            "A chain can wind around as much as you want, so long as it connects.",
                True, (10, 10, 10)), (10, 34))
        self.screen.blit(self.current_font.render(
            "Give it a try: it's simple to learn, but difficult to master. Have fun!",
                True, (10, 10, 10)), (10, 58))
        self.render()
        self.wait_for_click()
        
        
