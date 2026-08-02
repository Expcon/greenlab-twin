# GreenLab Twin

A lightweight laboratory visual perception prototype built with Python and OpenCV.

GreenLab Twin reads a real-time camera stream, detects significant motion through frame differencing, marks moving regions, automatically captures event images, and stores structured metadata in JSON format.

## Features

- Real-time camera preview
- Timestamp overlay
- Frame-difference motion detection
- Motion-region contour filtering
- Bounding-box visualization
- Automatic motion-triggered capture
- Three-second capture cooldown
- Manual screenshot capture
- JSON metadata persistence
- Capture record statistics
- Malformed JSON protection

## How It Works

The motion-detection pipeline is:

```text
Camera frame
    ↓
Grayscale conversion
    ↓
Gaussian blur
    ↓
Difference between adjacent frames
    ↓
Binary thresholding
    ↓
Morphological dilation
    ↓
Contour extraction
    ↓
Area filtering
    ↓
Motion event and automatic capture

The program compares each processed frame with the previous frame. Regions with sufficiently large pixel changes are converted into binary motion masks. Small contours are ignored as noise, while larger regions are marked with red bounding boxes.

Project Structure
greenlab-twin/
├── main.py
├── record_manager.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/
    ├── capture_records.json
    └── captured images

outputs/ contains local runtime data and is excluded from Git version control.

Installation

Clone the repository:

git clone https://github.com/Expcon/greenlab-twin.git
cd greenlab-twin

Install the dependency:

pip install -r requirements.txt
Usage

Run the program:

python main.py

Keyboard controls:

Key	Function
S	Save a manual screenshot
R	Display capture statistics
Q	Exit safely

When significant motion is detected, the system automatically saves an event image. Automatic captures are limited by a three-second cooldown to prevent excessive duplicate records.

Capture Records

Each screenshot is stored with structured metadata:

{
    "file_name": "motion_20260803_011921.jpg",
    "capture_time": "2026-08-03 01:19:21",
    "capture_type": "motion"
}

The capture_type field distinguishes:

manual: manually triggered by the user
motion: automatically triggered by motion detection
Current Parameters
MOTION_AREA_THRESHOLD = 1500
AUTO_CAPTURE_INTERVAL = 3.0
MOTION_AREA_THRESHOLD filters small image changes and camera noise.
AUTO_CAPTURE_INTERVAL controls the minimum interval between automatic captures.
Current Limitations
The current version detects image changes rather than recognizing specific objects.
Slow movement may not produce enough difference between adjacent frames.
Sudden lighting changes or camera movement may cause false detections.
Records are currently stored in a local JSON file.
Future Work
Background-subtraction based motion detection
Adjustable regions of interest
Object detection and classification
Event confidence scoring
Environmental sensor integration
Web-based monitoring dashboard
Digital-twin state visualization
Technology
Python 3.12
OpenCV
JSON
Git and GitHub
Author

Chen Qian
Incoming undergraduate student interested in robotics, artificial intelligence, and embodied intelligent systems.