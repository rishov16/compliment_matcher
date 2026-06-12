# Compliment Matcher

A Spotify-powered compliment matcher. This repository uses Spotify API credentials stored in a local `.env` file so the app can authenticate without exposing secrets in GitHub.

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your Spotify credentials:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI`

## Run

- Install dependencies
- Start the app per your existing project scripts

## Notes

- Do not commit `.env`
- `.env` is ignored by `.gitignore`
