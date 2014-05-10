import requests
import urlparse
import pygame
import time
import logging
import traceback

from StringIO import StringIO
from PIL import Image

UP, DOWN, LEFT, RIGHT, FRONT, BACK = ['up', 'down', 'left', 'right', 'front', 'back']
CLOCKWISE, ANTICLOCKWISE = ['clockwise', 'anticlockwise']


class Controller(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def takeoff(self):
        url = urlparse.urljoin(self.base_url, 'takeoff')
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def land(self):
        url = urlparse.urljoin(self.base_url, 'land')
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def stop(self):
        url = urlparse.urljoin(self.base_url, 'stop')
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def move(self, direction):
        url = urlparse.urljoin(self.base_url, 'move/{}'.format(direction))
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def rotate(self, direction):
        url = urlparse.urljoin(self.base_url, 'rotate/{}'.format(direction))
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def navdata(self):
        url = urlparse.urljoin(self.base_url, 'navdata')
        resp = requests.get(url)
        if resp.text == 'success':
            return True
        return False

    def image(self):
        url = urlparse.urljoin(self.base_url, 'image')
        resp = requests.get(url)
        if resp.status_code == 200:
            return Image.open(StringIO(resp.content))
        else:
            return None


def main(controller, screen):
    run = True

    controller.takeoff()

    try:
        while run:
            image = controller.image()
            try:
                mode = image.mode
                size = image.size
                data = image.tostring()
                surface = pygame.image.fromstring(data, size, mode)
            except pygame.error:
                logging.warn('Unable to load image')
                traceback.print_exc()
                time.sleep(1)
                continue
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        controller.land()


if __name__ == '__main__':

    controller = Controller('http://localhost:3000')
    screen = pygame.display.set_mode((480, 320))
    pygame.init()
    main(controller, screen)
