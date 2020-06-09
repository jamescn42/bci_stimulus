# Author: James Chen
# University of Calgary

"""This program will send instructions to Arduino for movement as a backup/emergency"""

# Imports for keyboard monitoring and display
from pynput.keyboard import Key, Listener
import pygame

# Exit condition events
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class RemoteControl:
    """
    Class used to control a Wheelchair externally

    Attributes:
    --------------------
    SCREEN_HEIGHT: int \n
    SCREEN_WIDTH: int

    Methods:
    --------------------
    begin_control()
        Starts pygame screen and sends corresponding information
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Wheelchair Control')

        # Set screen size
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500

        # Create array for button state:[<forwards>, <backwards>, <left>, <right>]
        self._buttons_pressed = [False, False, False, False]

        # Begin pygame screen
        self._screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def __on_press(self, key):
        """
        If button if pressed on keyboard, function will update button_pressed list
        :param key: Key Object from pynput.keyboard library
        :return: Nothing
        """
        if key == Key.up:
            self._buttons_pressed[0] = True
        try:
            if key.char == 'w':
                self._buttons_pressed[0] = True
        except AttributeError:
            pass

        if key == Key.down:
            self._buttons_pressed[1] = True
        try:
            if key.char == 's':
                self._buttons_pressed[1] = True
        except AttributeError:
            pass

        if key == Key.left:
            self._buttons_pressed[2] = True
        try:
            if key.char == 'a':
                self._buttons_pressed[2] = True
        except AttributeError:
            pass

        if key == Key.right:
            self._buttons_pressed[3] = True
        try:
            if key.char == 'd':
                self._buttons_pressed[3] = True
        except AttributeError:
            pass

    def __on_release(self, key):
        """
        When button is released on keyboard, function will update button_pressed list
        :param key: Key Object from pynput.keyboard library
        :return: Nothing
        """
        if key == Key.up:
            self._buttons_pressed[0] = False
        try:
            if key.char == 'w':
                self._buttons_pressed[0] = False
        except AttributeError:
            pass

        if key == Key.down:
            self._buttons_pressed[1] = False
        try:
            if key.char == 's':
                self._buttons_pressed[1] = False
        except AttributeError:
            pass

        if key == Key.left:
            self._buttons_pressed[2] = False
        try:
            if key.char == 'a':
                self._buttons_pressed[2] = False
        except AttributeError:
            pass

        if key == Key.right:
            self._buttons_pressed[3] = False
        try:
            if key.char == 'd':
                self._buttons_pressed[3] = False
        except AttributeError:
            pass

    def begin_control(self):
        """
        Begins the program to send data to the bluetooth module. Starts
        pygame screen and sends corresponding information
        :return: Nothing
        """
        running = True
        clock = pygame.time.Clock()

        # begins main loop for pygame
        while running:
            # Background color
            self._screen.fill((255, 255, 255))

            # Title
            large_font = pygame.font.Font('freesansbold.ttf', 45)
            title = large_font.render('Wheelchair Control', True, (0, 0, 0))
            title_rect = title.get_rect()
            title_rect.center = (250, 50)
            self._screen.blit(title, title_rect)

            # Instructions
            body_font = pygame.font.Font('freesansbold.ttf', 12)
            instructions = body_font.render("Use WASD or Arrows to control device manually", True, (0, 0, 0))
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (250, 475)
            self._screen.blit(instructions, instructions_rect)

            # Exit conditions
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    # if button is esc, exit
                    if event.key == K_ESCAPE:
                        running = False

                if event.type == QUIT:
                    running = False

            # monitor the keyboard for controls
            listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
            listener.start()

            # import button images
            north_arrow_unpressed = pygame.image.load("images/arrows/n_unpressed.png")
            north_east_arrow_unpressed = pygame.image.load("images/arrows/ne_unpressed.png")
            north_west_arrow_unpressed = pygame.image.load("images/arrows/nw_unpressed.png")
            south_arrow_unpressed = pygame.image.load("images/arrows/s_unpressed.png")
            south_east_arrow_unpressed = pygame.image.load("images/arrows/se_unpressed.png")
            south_west_arrow_unpressed = pygame.image.load("images/arrows/sw_unpressed.png")
            west_arrow_unpressed = pygame.image.load("images/arrows/w_unpressed.png")
            east_arrow_unpressed = pygame.image.load("images/arrows/e_unpressed.png")

            north_arrow_pressed = pygame.image.load("images/arrows/n_pressed.png")
            north_east_arrow_pressed = pygame.image.load("images/arrows/ne_pressed.png")
            north_west_arrow_pressed = pygame.image.load("images/arrows/nw_pressed.png")
            south_arrow_pressed = pygame.image.load("images/arrows/s_pressed.png")
            south_east_arrow_pressed = pygame.image.load("images/arrows/se_pressed.png")
            south_west_arrow_pressed = pygame.image.load("images/arrows/sw_pressed.png")
            west_arrow_pressed = pygame.image.load("images/arrows/w_pressed.png")
            east_arrow_pressed = pygame.image.load("images/arrows/e_pressed.png")

            # Draws arrows corresponding to keyboard presses
            # And sends data to arudino though bluetooth
            if self._buttons_pressed == [True, False, False, False]:
                self._screen.blit(north_arrow_pressed, (187, 75))
                self.__send_data('nn')
            else:
                self._screen.blit(north_arrow_unpressed, (187, 75))
            if self._buttons_pressed == [False, True, False, False]:
                self._screen.blit(south_arrow_pressed, (187, 325))
                self.__send_data('ss')
            else:
                self._screen.blit(south_arrow_unpressed, (187, 325))
            if self._buttons_pressed == [False, False, True, False]:
                self._screen.blit(west_arrow_pressed, (24, 200))
                self.__send_data('ww')
            else:
                self._screen.blit(west_arrow_unpressed, (24, 200))
            if self._buttons_pressed == [False, False, False, True]:
                self._screen.blit(east_arrow_pressed, (350, 200))
                self.__send_data('ee')
            else:
                self._screen.blit(east_arrow_unpressed, (350, 200))

            if self._buttons_pressed == [False, True, False, True]:
                self._screen.blit(south_east_arrow_pressed, (350, 325))
                self.__send_data('se')
            else:
                self._screen.blit(south_east_arrow_unpressed, (350, 325))
            if self._buttons_pressed == [False, True, True, False]:
                self._screen.blit(south_west_arrow_pressed, (24, 325))
                self.__send_data('sw')
            else:
                self._screen.blit(south_west_arrow_unpressed, (24, 325))
            if self._buttons_pressed == [True, False, False, True]:
                self._screen.blit(north_east_arrow_pressed, (350, 75))
                self.__send_data('ne')
            else:
                self._screen.blit(north_east_arrow_unpressed, (350, 75))
            if self._buttons_pressed == [True, False, True, False]:
                self._screen.blit(north_west_arrow_pressed, (24, 75))
                self.__send_data('nw')
            else:
                self._screen.blit(north_west_arrow_unpressed, (24, 75))

            # Updates pygame display
            pygame.display.update()

            # set FPS to 60
            clock.tick(60)

        # exit if out of loop
        pygame.quit()

    def __send_data(self, direction):
        # TODO: write this function to send data to Arduino (serial or bluetooth)
        pass


if __name__ == '__main__':
    wheelchair = RemoteControl()
    wheelchair.begin_control()
