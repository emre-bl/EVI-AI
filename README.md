# EVI-AI  
## Eyes for the Visually Impaired  

This project aims to assist individuals with visual impairments in their daily activities. It employs an application that uses the mobile phone's camera to identify objects and gauge their distances. The app then leverages a Large Language Model (LLM) to interpret the findings from the YOLO (You Only Look Once) object detection and ZoeDepth perception models. This information is converted into audio commands, guiding users to navigate their environment more effectively.  

## Project Overview

The main components of this project include:  

- A mobile application written in Flutter  
- A YOLO object detection model  
- A ZoeDepth detection model  
- A LAMA LLM model  

## Getting Started  

### Prerequisites
- Python 3  
- Flutter
- Jupyter Notebook

### Installation

- Clone the repository
  ```bash
  git clone https://github.com/emre-bl/EVI-AI.git
  ```

- Install dependencies
  ```bash
  pip install -r requirements.txt
  ```  

- Go to mobile app's directory  
  ```bash
  cd pipeline_scripts/mobile_app
  ```  

- Run the commands below
  ```bash
  flutter clean
  ```  
  ```bash
  flutter pub get
  ```  
  ```bash
  flutter build apk
  ```  
  ```bash
  adb install path/to/your/app-release.apk
  ```  

## Usage

- TODO add structural image and explain

## Contributors

- [Emre Belikırık](https://github.com/emre-bl)
- [Meriç Demirörs](https://github.com/mericdemirors)
- [Zeynep Meriç Aşık](https://github.com/meric2)
