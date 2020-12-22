# veems

**An open-source platform for online video.**

The code powering https://veems.tv.
A next generation video sharing platform, with freedom of speech values.

## Contributing

We're actively looking for help with both frontend and backend development.

[Join us on Discord](https://discord.gg/RjCZMtZ) if you're interested in being involved.

[![https://i.imgur.com/Ujf8Ti8.png](https://i.imgur.com/Ujf8Ti8.png)](https://discord.gg/RjCZMtZ)

## Screenshots

A preview of what we're building.

Further design materials can be found [here](https://github.com/VeemsHQ/design).

![https://i.imgur.com/pkrQgzE.png](https://i.imgur.com/pkrQgzE.png)

![https://i.imgur.com/ZMJYNvl.png](https://i.imgur.com/ZMJYNvl.png)

![https://i.imgur.com/VGC6FQj.png](https://i.imgur.com/VGC6FQj.png)

## Feature Roadmap

In order of priority.

1. Uploading, transcoding of content, playlist video packaging ✅.
2. Playback of video content (backend ✅, frontend).
3. User & API authentication.
4. Creation and management of "Channels".
5. Channel Dashboard (basics).
    - Video Management.
    - Channel customisation.
6. Video comments.
7. Video responses.
8. Like/dislike videos.
9. Follow (Subscribe to) a Channel.
10. Related videos suggestions.
11. Video categories pages.
    - Sport
    - Comedy
    - etc
12. Trending videos.
    - Trending algorithm.
    - Trending section on Homepage.
13. User notifications.
    - UI notifications.
    - Email notifications.
14. Sync channel(s) content from YT to Veems automatically.
    - Channel Dashboard, sync configuration.
    - Background sync process.
    - Related user notifications.
15. Monetization.
    - Revenue share from Premium user accounts.
    - Banner ads.
    - Pre-roll video player ads.
    - Video view validation.
16. Embeddable video player.
17. User controlled content hiding. (e.g. Don't show me any cat videos).
18. User Badges (earned by performing actions on the platform).

This section is work-in-progress, more to be added shortly.

## Installation

First install OS dependencies, ffmpeg and ffprobe. You will also need Docker.

Linux:

```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

Mac:

```bash
brew install ffmpeg
```

From within a Python 3.6+ virtualenv (we recommend using [pyenv](https://github.com/pyenv/pyenv) to manage your virtualenvs).

```bash
make install
```

Set of the required environment variables for the application, see `.env.template` for examples. A few of the secrets relating to the hosting provider (ACCESS_KEY_ID, SECRET_ACCESS_KEY) you may need to request values for.

## Running the tests

Start up the supporting docker containers (RabbitMQ, Postgres, Localstack).
Then run the tests.

```bash
make start-deps
make test
```

## Usage

### Running the webserver

```bash
make start-deps
python manage.py migrate --noinput
python manage.py runserver
```

### Running the background [Celery](https://docs.celeryproject.org/en/stable/index.html) workers

```bash
./celeryworker-entrypoint.sh
./celerybeat-entrypoint.sh
```

## Architectural Concepts

- **Upload** -- a raw video file upload into the system
    - **Video** -- a video, which you can view via the website
        - **Video Rendition** -- a version of the Video file at a specific resolution, bitrate, etc. e.g. 1080p
            - **Video Rendition Segment** -- a small chunk of the Video Rendition video file to be served to the video player
            - **Video Rendition Thumbnail** -- a thumbnail at a certain timestamp within the Video Rendition video file
