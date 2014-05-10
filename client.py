import os
import requests
import urlparse
import time
import logging
import qrtools

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
            with open('cam.png', 'wb+') as image_file:
                image_file.write(resp.content)


def main(controller):
    run = True
    controller.takeoff()
    controller.move(UP)
    controller.move(UP)
    controller.move(UP)
    try:
        while run:
            controller.image()
            if os.path.isfile('cam.png'):
                decoder = qrtools.QR(filename='cam.png')
                if decoder.decode():
                    direction = decoder.data_to_string()
                    if direction.startswith('\xef\xbb\xbf'):
                        direction = direction[3:]
                    logging.warn('Decoded, direction = {}'.format(direction))
                    if direction in ['up', 'down', 'left', 'right', 'front', 'back']:
                        logging.warn('Moving: {}'.format(direction))
                        controller.move(direction)
                    # elif direction in ['clockwise', 'anticlockwise']:
                    #     logging.warn('Rotating: {}'.format(direction))
                    elif direction == 'land':
                        logging.warn('Landing')
                        controller.land()
                    # elif direction == 'takeoff':
                    #     logging.warn('Take Off')
                    #     controller.takeoff()
                else:
                    logging.warn('Unable to decode!')
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        controller.land()


if __name__ == '__main__':

    controller = Controller('http://localhost:3000')
    main(controller)
