import time

from common import helper
from plugins.driver.button import drive_button
from plugins.driver.keyboard import *


def main():
    print("卧槽")


if __name__ == "__main__":
    time.sleep(3)
    drive_button(VK_LEFT, 0, True)
    drive_button(VK_LEFT, 1, True)
    drive_button(VK_UP, 1, True)
    time.sleep(3)
    drive_button(VK_LEFT, 2, True)
    drive_button(VK_UP, 2, True)

    time.sleep(3)
    drive_button(VK_X, 0, False)
    time.sleep(3)
    drive_button(VK_C, 0, False)
    time.sleep(3)
    drive_button(VK_X, 1, False)
    helper.sleep(800)
    drive_button(VK_X, 2, False)
    helper.sleep(100)
