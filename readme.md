# iPhone Media Convert

A lightweight Python utility suite for organizing and converting media exported from iPhones and other Apple devices.

This project solves two common issues encountered when transferring media from iOS devices to Windows or Linux systems:

1. **HEIC image compatibility problems**
2. **Large MOV video files and codec compatibility issues**

The repository provides two standalone utilities:

* `move_media.py` → Automatically sorts media into Images and Videos folders
* `convert_media.py` → Converts HEIC images to JPG and MOV videos to compressed MKV (H.265)

---

# Features

## Media Organization

The `move_media.py` utility:

* Detects common image and video formats
* Automatically creates:

  * `Images/`
  * `Videos/`
* Moves files into their respective folders
* Works on the current folder or any specified path

Supported image formats:

* JPG / JPEG
* PNG
* GIF
* BMP
* TIFF
* HEIC
* WEBP

Supported video formats:

* MP4
* MOV
* AVI
* MKV
* WMV
* FLV
* WEBM

---

## Media Conversion

The `convert_media.py` utility:

### Image Conversion

* Converts `.HEIC` images to `.JPG`
* Uses Pillow + pillow-heif for HEIC decoding
* Produces widely compatible JPEG output

### Video Conversion

* Converts `.MOV` videos to `.MKV`
* Uses FFmpeg for transcoding
* Encodes video using H.265 / HEVC
* Produces smaller files compared to original MOV recordings
* Improves compatibility for media servers and Linux systems

---

# Why This Project Exists

Modern iPhones use:

* HEIC for images
* MOV containers with HEVC/H.264 video

These formats are efficient but can create workflow issues:

| Problem               | Example                                         |
| --------------------- | ----------------------------------------------- |
| HEIC unsupported      | Some Windows apps cannot preview HEIC           |
| Large video sizes     | iPhone videos consume large storage quickly     |
| Limited compatibility | Some media players dislike MOV containers       |
| Upload issues         | Some websites reject HEIC uploads               |
| Media server issues   | Jellyfin/Plex workflows may require transcoding |

This project automates the cleanup and conversion process.

---

# Project Structure

```text
.
├── convert_media.py
├── move_media.py
├── readme.md
└── .gitignore
```

---

# Requirements

## Python Version

* Python 3.10+

---

## Python Dependencies

Install dependencies using pip:

```bash
pip install Pillow pillow-heif
```

---

## FFmpeg

FFmpeg is required for video conversion.

### Linux

Ubuntu / Debian:

```bash
sudo apt install ffmpeg
```

Arch Linux:

```bash
sudo pacman -S ffmpeg
```

Fedora:

```bash
sudo dnf install ffmpeg
```

---

### Windows

You can install FFmpeg using:

#### Winget

```powershell
winget install Gyan.FFmpeg
```

#### Chocolatey

```powershell
choco install ffmpeg
```

The script also attempts to automatically detect FFmpeg in common Windows installation locations.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/iPhoneMediacovert.git
cd iPhoneMediacovert
```

---

## Create Virtual Environment (Recommended)

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install Pillow pillow-heif
```

---

# Usage

# 1. Organize Media Files

Move all images and videos into separate folders:

```bash
python move_media.py
```

This creates:

```text
Images/
Videos/
```

and automatically moves supported files.

---

## Organize a Specific Folder

```bash
python move_media.py /path/to/media
```

Example:

```bash
python move_media.py ~/Downloads/iPhoneExport
```

---

# 2. Convert Media Files

Convert all supported media inside the current folder:

```bash
python convert_media.py
```

---

## Command Line Arguments

The `convert_media.py` script supports several optional arguments for customization.

### Positional Argument

#### `root`

Root folder containing the `Images/` and `Videos/` directories.

Default:

```text
.
```

Example:

```bash
python convert_media.py ~/Pictures/iPhoneBackup
```

The folder structure must look like:

```text
root/
├── Images/
└── Videos/
```

---

### Optional Arguments

#### `--jpg-quality`

Controls JPEG quality for converted HEIC images.

Default:

```text
95
```

Example:

```bash
python convert_media.py --jpg-quality 85
```

Lower values:

* Smaller file sizes
* Lower image quality

Higher values:

* Better image quality
* Larger file sizes

---

#### `--ffmpeg`

Specify a custom FFmpeg executable path.

Default:

```text
ffmpeg
```

Example:

### Linux

```bash
python convert_media.py --ffmpeg /usr/bin/ffmpeg
```

### Windows

```powershell
python convert_media.py --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"
```

Useful when:

* FFmpeg is not available in PATH
* Multiple FFmpeg versions are installed
* Using portable FFmpeg builds

---

## Full Usage Examples

### Basic Conversion

```bash
python convert_media.py
```

---

### Convert Another Folder

```bash
python convert_media.py ~/Media/iPhoneExport
```

---

### Lower JPEG Quality

```bash
python convert_media.py --jpg-quality 80
```

---

### Custom FFmpeg Binary

```bash
python convert_media.py --ffmpeg /opt/ffmpeg/bin/ffmpeg
```

---

### Combined Example

```bash
python convert_media.py ~/Media/iPhoneExport --jpg-quality 88 --ffmpeg /usr/bin/ffmpeg
```

This command:

* Uses a custom media folder
* Converts HEIC images at quality level 88
* Uses a manually specified FFmpeg binary

---

## Convert Media in Another Folder

```bash
python convert_media.py /path/to/media
```

Example:

```bash
python convert_media.py ~/Pictures/iPhoneBackup
```

---

# Conversion Details

## HEIC → JPG

The script:

1. Opens the HEIC image
2. Decodes it using pillow-heif
3. Converts it to RGB
4. Saves a `.jpg` version

Example:

```text
IMG_0001.HEIC
↓
IMG_0001.jpg
```

---

## MOV → MKV

The script:

1. Uses FFmpeg
2. Re-encodes video to H.265 / HEVC
3. Wraps output inside MKV container

Example:

```text
VID_0001.MOV
↓
VID_0001.mkv
```

Benefits:

* Reduced file size
* Better streaming compatibility
* Easier archival
* Better Linux support

---

# Example Workflow

## Typical iPhone Export Cleanup

### Step 1 — Copy media from iPhone

```text
DCIM/
```

contains:

```text
IMG_1001.HEIC
IMG_1002.HEIC
VID_1003.MOV
VID_1004.MOV
```

---

### Step 2 — Organize media

```bash
python move_media.py ./DCIM
```

Result:

```text
DCIM/
├── Images/
│   ├── IMG_1001.HEIC
│   └── IMG_1002.HEIC
└── Videos/
    ├── VID_1003.MOV
    └── VID_1004.MOV
```

---

### Step 3 — Convert media

```bash
python convert_media.py ./DCIM
```

Result:

```text
IMG_1001.jpg
IMG_1002.jpg
VID_1003.mkv
VID_1004.mkv
```

---

# Error Handling

The project includes:

* FFmpeg availability detection
* Windows-specific FFmpeg path detection
* Interactive FFmpeg installation support
* Import validation for Pillow and pillow-heif
* Safe path handling using `pathlib`

---

# Platform Support

| Platform | Supported |
| -------- | --------- |
| Windows  | Yes       |
| Linux    | Yes       |
| macOS    | Yes       |

---

# Technical Notes

## Libraries Used

### Pillow

Used for:

* Image loading
* JPEG generation
* RGB conversion

---

### pillow-heif

Adds HEIC/HEIF support to Pillow.

---

### FFmpeg

Used for:

* Video transcoding
* H.265 encoding
* Container conversion

---

# Potential Improvements

Future enhancements may include:

* Parallel conversion for faster processing
* GUI interface
* Drag-and-drop support
* Recursive directory scanning
* Metadata preservation
* EXIF transfer
* GPU accelerated encoding
* Progress bars
* File overwrite protection
* Logging system
* Batch presets

---

# Troubleshooting

## FFmpeg Not Found

Install FFmpeg and ensure it is available in PATH.

Verify:

```bash
ffmpeg -version
```

---

## HEIC Conversion Fails

Ensure dependencies are installed correctly:

```bash
pip install --upgrade Pillow pillow-heif
```

---

## Permission Errors

Make sure:

* Files are not open in another application
* You have write permissions to the target directory

---

# Performance Considerations

Video transcoding is CPU intensive.

Factors affecting speed:

* Video resolution
* Video duration
* CPU performance
* H.265 encoding complexity

Large 4K iPhone videos may take significant time to process.

---

# Security Notes

This project:

* Does not upload files anywhere
* Performs all processing locally
* Does not require cloud services
* Does not collect telemetry

---

# License

Add your preferred license here.

Example:

```text
MIT License
```

---

# Contributing

Contributions are welcome.

Potential areas:

* Performance optimization
* Better codec presets
* Recursive scanning
* Cross-platform packaging
* GUI development
* Additional image/video format support

---

# Acknowledgements

* Pillow
* pillow-heif
* FFmpeg

---

# Author

Created for simplifying iPhone media management workflows on desktop systems.
