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
            instructions_rect.center = (250, 400)
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
            up = pygame.image.load("images/arrows/up.png")
            up_pressed = pygame.image.load("images/arrows/up_pressed.png")
            down = pygame.image.load("images/arrows/down.png")
            down_pressed = pygame.image.load("images/arrows/down_pressed.png")
            left = pygame.image.load("images/arrows/left.png")
            left_pressed = pygame.image.load("images/arrows/left_pressed.png")
            right = pygame.image.load("images/arrows/right.png")
            right_pressed = pygame.image.load("images/arrows/right_pressed.png")

            # Draws arrows corresponding to keyboard presses
            # And sends data to arudino though bluetooth
            if self._buttons_pressed[0]:
                self._screen.blit(up_pressed, (187, 100))
                self.__send_data('f')
            else:
                self._screen.blit(up, (187, 100))
            if self._buttons_pressed[1]:
                self._screen.blit(down_pressed, (187, 275))
                self.__send_data('b')
            else:
                self._screen.blit(down, (187, 275))
            if self._buttons_pressed[2]:
                self._screen.blit(left_pressed, (100, 187))
                self.__send_data('l')
            else:
                self._screen.blit(left, (100, 187))
            if self._buttons_pressed[3]:
                self._screen.blit(right_pressed, (275, 187))
                self.__send_data('r')
            else:
                self._screen.blit(right, (275, 187))

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
