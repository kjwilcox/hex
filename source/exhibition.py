import pygame
import glob
import os


class Exhibition():
    def __init__(self, autoload="images"):
        
        self.images = {}

        if autoload:
            self.auto_load(autoload)

    def auto_load(self, directory="images"):
        """ Automatically loads all images in the given subdirectory. """
        images = []

        for ext in ('jpg', 'jpeg', 'png', 'gif', 'bmp'):
            for image in glob.glob(os.path.join(directory, "*." + ext)):
                images.append(image)

        for image in images:
            self.load(image.split('.')[0].split(os.path.sep)[1], image)

    def load(self, name, filename):
        """ Loads an image into the exhibition. """
        self.images[name] = pygame.image.load(filename)

    def image(self, name):
        """ Returns a loaded surface. """
        return self.images[name]

def load_images(directory="images"):
    """ Auto-loads images in given directory and returns a dict. """
    images = Exhibition(directory)
    return images.images

def optimize(images):
    """
    Optimizes a dict of already loaded images.
    Only call after you have created your display surface.
    """

    for key in images:
        images[key] = images[key].convert_alpha()
