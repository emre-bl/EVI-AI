# Mobile Application of EVI-AI

This app aims to send the user audio responses that is extracted from the LLM model which sends caution messages if an obstacle is encountered that can be detected from phone camera.

# Build APK

- Clone the repository
  ```bash
  git clone https://github.com/emre-bl/EVI-AI.git
  ```

- Install dependencies  
  ```bash
  pip install -r requirements.txt
  ```  

- Go to directory  
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
