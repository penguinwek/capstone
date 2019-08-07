#! /bin/env python3

import ffmpeg
import logging
import subprocess

import numpy as np

from typing import Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_video_size(filename: str) -> Tuple[int, int, str]:
    logger.info('Getting video size for {!r}'.format(filename))
    probe = ffmpeg.probe(filename)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    print(video_info)
    audio_info = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    print(audio_info)
    width = int(video_info['width'])
    height = int(video_info['height'])
    fps = video_info['r_frame_rate']
    return width, height, fps


def start_ffmpeg_process1(in_filename: str) -> subprocess.Popen:
    logger.info('Starting ffmpeg process1')
    args = (
        ffmpeg
        .input(in_filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .compile()
    )
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def start_ffmpeg_process2(out_filename: str, width: int, height: int, fps: str) -> subprocess.Popen:
    logger.info('Starting ffmpeg process2')
    args = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        .output(out_filename, pix_fmt='yuv420p', r=fps)
        .overwrite_output()
        .compile()
    )
    return subprocess.Popen(args, stdin=subprocess.PIPE)


def test():
    in_filename: str = "test/test.mp4"
    out_filename: str = "out/test.mp4"

    width, height, fps = get_video_size(in_filename)
    process1 = start_ffmpeg_process1(in_filename)
    process2 = start_ffmpeg_process2(out_filename, width, height, fps)

    while True:
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )

        # See examples/tensorflow_stream.py:
        # out_frame = deep_dream.process_frame(in_frame)
        out_frame = in_frame

        process2.stdin.write(
            out_frame
            .astype(np.uint8)
            .tobytes()
        )

    logger.info('Waiting for ffmpeg process1')
    process1.wait()

    logger.info('Waiting for ffmpeg process2')
    process2.stdin.close()
    process2.wait()

    logger.info('Done')

if __name__ == "__main__":
    print("Hello, World!")
    test()