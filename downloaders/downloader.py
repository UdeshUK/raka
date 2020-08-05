#!/usr/bin/env python

"""Download reduced YouTube videos.
"""

import os
import sys
import argparse
import json
import pafy

from utility.files import WriteableDir, create_if_not_exist

youtube_video_url = 'https://www.youtube.com/watch?v='


def download(youtube, video_path):
    top_videos = youtube[:50]

    skipped = 0

    for video in top_videos:
        url = youtube_video_url + video['id']
        video_data = pafy.new(url)
        print(video_data)
        streams = video_data.streams
        if len(streams) > 0:
            stream = streams[0]
            print(stream.get_filesize())
            stream.download(video_path + video['id'] + '.mp4')
        else:
            skipped += 1
        break


def run(dataset_dir):
    reduced_path = dataset_dir + '/reduced.json'
    video_path = dataset_dir + '/videos/'

    if not os.access(reduced_path, os.R_OK):
        print("Dataset required from URL extraction is not available on the given directory")
        return

    if not os.path.exists(video_path):
        os.makedirs(video_path)

    with open(reduced_path, 'r') as json_data:
        youtube = json.load(json_data)

    download(youtube, video_path)


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-a', '--apikey', help="YouTube Data API key")
    parser.add_argument('dir', help="Dataset directory",
                        action=WriteableDir, default='.')

    args = parser.parse_args(arguments)

    api_key = args.apikey
    pafy.set_api_key(api_key)

    dataset_dir = args.dir

    run(dataset_dir)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
