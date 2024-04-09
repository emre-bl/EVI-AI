import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:async';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:flutter_tts/flutter_tts.dart';

List<CameraDescription> cameras = [];

Future<void> main() async{
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras(); // Get a list of available cameras
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'EVI-AI'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  AudioPlayer audioPlayer = AudioPlayer();
  Timer? timer;
  Timer? timer2;
  bool shouldPlayStartSound = true; // Flag to control start sound playback
  bool ifStarted = false; // Initial state of the button
  bool allowPlayStartSound = true; // Flag to control start sound playback
  CameraController? cameraController;
  int counter = 0;

  // Method to capture and send frame
  Future<void> captureAndSendFrame() async {
    if (!cameraController!.value.isInitialized) {
      debugPrint("Controller is not initialized");
      return;
    }

    try {
      final image = await cameraController!.takePicture();
      final imagePath = image.path;

      // Read the image as bytes
      File imgFile = File(imagePath);
      List<int> imageBytes = await imgFile.readAsBytes();
      String base64Image = base64Encode(imageBytes);

      // Send to Flask server as a POST request
      Uri uri = Uri.parse('http://10.3.64.198:5000/process_image');
      var response = await http.post(
        uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"image": base64Image}),
      );

      if (response.statusCode == 200) {
        debugPrint('Image uploaded successfully.');
      } else {
        debugPrint('Failed to upload image. Status code: ${response.statusCode}. Response body: ${response.body}');
      }
    } catch (e) {
      debugPrint("Error capturing and sending frame (catch): $e");
    }
  }

  // Function to fetch LLM_out from the Flask server
  Future<String> fetchLLMOut() async {
    final response = await http.get(Uri.parse('http://10.3.64.198:5000/get_llm_output'));

    if (response.statusCode == 200) {
      // If the server returns a 200 OK response, parse the JSON
      debugPrint('LLM_out: ${json.decode(response.body)['LLM_out']}');
      return json.decode(response.body)['LLM_out'];
    } else {
      // Response not OK
      throw Exception('Failed to load LLM_out');
    }
  }

  @override
  void initState() {
    super.initState();
    // Initialize camera controller
    cameraController = CameraController(cameras[0], ResolutionPreset.medium);
    cameraController!.initialize().then((_) {
      if (!mounted) return;
      setState(() {}); // When the camera is initialized, rebuild the widget
    });

    audioPlayer.onPlayerComplete.listen((event) {
      if (allowPlayStartSound) { // Only replay start sound if 'Stop' button is not pressed
        Timer(const Duration(seconds: 5), playStartSound); // Wait for 5 seconds before playing the sound again
      }
    });
    playStartSound(); // Play the start sound immediately on app start
  }

  void playStartSound() async {
    if (!ifStarted) {
      await audioPlayer.play(AssetSource('start_sound.mp3'));
    }
  }

  void stopStartSound() {
    audioPlayer.stop(); 
    allowPlayStartSound = false;
  }

  // Play LLM sounf if updated
  void startTimer() {
    timer = Timer.periodic(const Duration(seconds: 5), (Timer t) async {
      FlutterTts flutterTts = FlutterTts();
      String llmOut = await fetchLLMOut();
      flutterTts.setLanguage("en-US");
      String textToSpeech = llmOut.substring(0, llmOut.length - 2);
      int llmCounter = int.parse(llmOut.substring(llmOut.length-1, llmOut.length));
      if (llmCounter > counter) {
        flutterTts.speak(textToSpeech);
        counter += 1;
      }
    });
  }

  @override
  void dispose() {
    timer?.cancel();
    timer2?.cancel();
    audioPlayer.dispose();
    cameraController?.dispose();
    super.dispose();
  }

  // Every 15 seconds, capture and send frame from phone camera
  void startTimerForFrames() {
    const period = Duration(seconds: 15);
    timer2 = Timer.periodic(period, (Timer t) async {
      await captureAndSendFrame();
    });
  }

  // When the app is started play an initial sound
  void playStopSound() async {
    try {
      await audioPlayer.stop(); // Ensure the player is stopped before playing another sound.
      await audioPlayer.release(); // Release the resources used by the player.
      audioPlayer = AudioPlayer(); // Create a new instance of the player.
      await audioPlayer.play(AssetSource('first_out.mp3'));
    } catch (e) {
      debugPrint("Error playing stop sound: $e");
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: SizedBox.expand( // Expand button to fill all the available space
          child: Padding(
            padding: const EdgeInsets.all(16.0), 
            child: ElevatedButton(
              onPressed: () {
                setState(() {
                  ifStarted = !ifStarted; // Toggle the state
                  if (ifStarted) {// 'Stop' button is pressed
                    // stop the start sound and start the timer
                    stopStartSound(); // Ensure the start sound is stopped before starting the timer
                    startTimer(); // Start the timer for the periodic sound
                    startTimerForFrames(); // Start the timer for capturing and sending frames
                    captureAndSendFrame(); // Capture and send the first frame on second 0
                    playStopSound(); // Play the stop sound once when the button is pressed
                  } else {// 'Start' button is pressed
                    // stop the timer and reset to initial state
                    timer?.cancel();
                    timer2?.cancel();
                    shouldPlayStartSound = true;
                    allowPlayStartSound = true;
                    playStartSound(); // play the start sound again
                  }
                });
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, double.infinity),
                elevation: 0,
                shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
              ),
              child: Text(
                ifStarted ? 'Stop' : 'Start',
                style: const TextStyle(fontSize: 48),
              ),
            ),
          ),
        ),
      ),

    );
  }
}
