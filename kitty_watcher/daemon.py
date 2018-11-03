# coding: utf-8

import os


def main():
    os.popen(
        'raspivid -t 0 -w 320 -h 240 -o - | '
        'ffmpeg -i - -s 320x240 -f mpegts -codec:v mpeg1video -bf 0 -codec:a mp2 -r 30 http://127.0.0.1:8081/owenliu'
    )


if __name__ == '__main__':
    main()
