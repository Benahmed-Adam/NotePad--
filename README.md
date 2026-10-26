# NotePad--

NotePad-- is a high-quality editor written in Python using `pygame` and `pyvidplayer2`. It is designed to redefine the way you write text.
With NotePad--, writing text has never been this epic.

## Table of Contents

  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [System Compatibility](#system-compatibility)

## Example

[Watch the video](exemple/video1.mp4)

## Features

  - Simple and fast text editing
  - Graphical interface powered by `pygame`
  - Integrated video/audio playback support via `pyvidplayer2`

## Dependencies

### Python (via `requirements.txt`)

  - `pygame`
  - `pyvidplayer2`
  - `imageio[ffmpeg,pyav]`

### System

  - `portaudio` (required for certain audio libraries)
  - `ffmpeg` (must be installed manually)

## Installation

### Step 1 – Clone the repository

```bash
git clone https://github.com/Benahmed-Adam/notepad--.git
cd notepad--
```

### Step 2 – Run the startup script

```bash
python start.py
```

The script automatically detects missing dependencies (usually) and will:

  - Prompt to install `portaudio` if necessary
  - Install the required Python packages

### Step 3 – Enjoy

Experience the incredible writing journey provided by NotePad--.

## Usage

Once `main.py` is launched (either automatically or manually), the text editor will open. All tools and features are accessible directly through the graphical interface.

## Project Structure

```
├── start.py               # Startup and installation script
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── resources/             # Static files (sounds, images, videos)
└── README.md              # Documentation
└── etc...
```

## System Compatibility

It is supposed to work pretty much everywhere...
