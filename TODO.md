# Legend:
* 🎫 --> must be added to project
* 💡 --> will be discussed
* 📏 --> tests needed for improvement
* ✅ --> done
* ❌ --> not done

# YOLO-SIDE
- new YOLO models for different speed/precision can be added from: https://docs.ultralytics.com/models/yolov8/#key-features 💡
- different verbose types(drawing bounding boxes or showing available ways) can be added 💡

# LLM-SIDE
- Local LLM testing must done 🎫
- LLM prompts should be tried and improved if needed 📏

# DEPTH-MODELS-SIDE
- best pretrained models on telegram must be selected (one for city and one for indoor cases) 🎫
- inference code for both models must be created 🎫
- 2 depth models(one for cityscapes one for indoors) should be included in app, model selection will be left to user. 📏

# RTSP-SIDE
- images can be sent as json objects 💡
- additional information(original image size, YOLO version, DEPTH model type etc.) about pipeline usage must be sent also 🎫
- images can sent in base64 💡
- problem with already open connections must be solved 🎫

# ENTIRE CODE
- temporary function importing must be added for image receiving functions 🎫
- functions must be imported from their relative path to user.py and server.py 🎫
- whole pipeline must be merged together 🎫
- text-to-speech can be better, maybe it will work better in phone 💡
- whole code should be able to controlled via yaml file 💡

# USER-SIDE-PIPELINE
- 1-) capture the frame from camera ✅
- 2-) send the captured frame to server ✅
- 3-) wait for servers response ✅
- 4-) give audio feedback to user in all languages❌

# APP-SIDE-PIPELINE
- 1-) wait for images from user ✅
- 2-) send image to YOLO ✅
- 3-) send image to DEPTHMODEL ❌
- 4-) merge YOLO and DEPTHMODEL output ❌
- 5-) concatanate merged output string with ready LLM prompt ❌
- 6-) send new prompt to LLM API ❌
- 7-) return the answer of LLM to image_sender ❌