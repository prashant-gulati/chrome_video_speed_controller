# Video Speed Controller

A minimal Chrome extension to control video playback speed on any website.

## Features

- Set playback speed to **0.25×, 0.5×, 0.75×, 1×, 2×, 3×, or 4×**
- Works on all websites with HTML5 video (YouTube, Netflix, Vimeo, etc.)
- Applies to all frames on the page
- Speed persists across page interactions

## Installation

### From Chrome Web Store
Install directly from the [Chrome Web Store](https://chrome.google.com/u/1/webstore/devconsole/6576491c-d856-48ff-8170-a71701eb058b/gnmhkilmfojejdhkagkhmpbkgkenloop/edit/status).

### Load Unpacked (Developer Mode)
1. Clone this repository
2. Open `chrome://extensions` in Chrome
3. Enable **Developer mode** (top-right toggle)
4. Click **Load unpacked** and select this folder

## Usage

1. Navigate to any page with a video
2. Click the extension icon in the toolbar
3. Select a speed — it applies instantly to all videos on the page

## Project Structure

```
chrome_video_speed_controller/
├── manifest.json      # Extension manifest (MV3)
├── content.js         # Content script injected into all pages
├── popup.html         # Extension popup UI
├── popup.js           # Popup logic
├── popup.css          # Popup styles
├── icons/             # Extension icons (16, 48, 128px)
└── generate_icons.py  # Script used to generate icon assets
```
