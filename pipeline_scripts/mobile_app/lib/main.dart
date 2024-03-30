import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:async';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:flutter_tts/flutter_tts.dart';
//import 'package:path_provider/path_provider.dart';
//import 'package:path/path.dart' as path;

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

  /*Future<void> runUserScript() async {
    final uri = Uri.parse('http://10.5.64.197:5000/runscript');
    try {
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        // Successfully executed the script
        final data = jsonDecode(response.body);
        debugPrint("Script is running ${data['output']}");
        // You can update your UI or state based on the script output
      } else {
        // Handle server errors
        debugPrint("Failed to execute script. Server error: ${response.body}");
      }
    } catch (e) {
      // Handle any errors that occur during the request
      debugPrint("Error making the request: $e");
    }
  }*/

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

      // Send to your Flask server as a POST request
      Uri uri = Uri.parse('http://10.2.141.3:5000/process_image');
      var response = await http.post(
        uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"image": base64Image}),
      );

      if (response.statusCode == 200) {
        debugPrint('Image uploaded successfully. $counter');
        counter += 1;
      } else {
        debugPrint('Failed to upload image. Status code: ${response.statusCode}. Response body: ${response.body}');
      }
    } catch (e) {
      debugPrint("Error capturing and sending frame (catch): $e");
    }
  }

  // Function to fetch LLM_out from the Flask server
  Future<String> fetchLLMOut() async {
    final response = await http.get(Uri.parse('http://10.2.141.3:5000/get_llm_output'));

    if (response.statusCode == 200) {
      // If the server returns a 200 OK response, parse the JSON
      return json.decode(response.body)['LLM_out'];
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception.
      throw Exception('Failed to load LLM_out');
    }
  }

  @override
  void initState() {
    super.initState();
    // Initialize camera controller
    cameraController = CameraController(cameras[0], ResolutionPreset.medium); // Initialize camera controller
    cameraController!.initialize().then((_) {
      if (!mounted) return;
      setState(() {}); // When the camera is initialized, rebuild the widget
    });

    audioPlayer.onPlayerComplete.listen((event) {
      if (allowPlayStartSound) { // Only replay start sound if 'Stop' button is not pressed
        Timer(const Duration(seconds: 5), playStartSound); // Wait for 5 seconds before playing the sound again
        //playStartSound();
      }
    });
    playStartSound(); // Play the start sound immediately on app start
  }

  void playStartSound() async {
    if (!ifStarted) {
      await audioPlayer.play(AssetSource('start_sound.mp3'));
      // Set a Timer to play the sound again after 5 seconds, only if allowed
      /*Timer(const Duration(seconds: 5), () {
        if (allowPlayStartSound) {
          playStartSound();
        }
      });*/
    }
  }

  void stopStartSound() {
    audioPlayer.stop(); 
    allowPlayStartSound = false;
  }

  void playSound() async {
    if (!shouldPlayStartSound) {
      FlutterTts flutterTts = FlutterTts();
      String llmOut = await fetchLLMOut();
      flutterTts.speak(llmOut);
      //await audioPlayer.play(AssetSource('LLM_output.mp3'));
    }
  }

  void startTimer() {
    const dur = Duration(seconds: 20);
    timer = Timer.periodic(dur, (Timer t) async {
      FlutterTts flutterTts = FlutterTts();
      String llmOut = await fetchLLMOut();
      flutterTts.speak(llmOut);
      //await audioPlayer.play(AssetSource('LLM_output.mp3'));
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

  void startTimerForFrames() {
    const period = Duration(seconds: 20);
    timer2 = Timer.periodic(period, (Timer t) async {
      await captureAndSendFrame(); // Capture and send the frame
    });
  }


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
                    //runUserScript();
                    stopStartSound(); // Ensure the start sound is stopped before starting the timer
                    startTimer(); // Start the timer for the periodic sound
                    startTimerForFrames(); // Start the timer for capturing and sending frames
                    playStopSound(); // Play the stop sound once when the button is pressed
                  } else {// 'Start' button is pressed
                    // stop the timer and reset to initial state
                    timer?.cancel();
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
                // If you want to have no visual difference when the button is pressed:
                //tapTargetSize: MaterialTapTargetSize.shrinkWrap, // Removes additional space for the ink splash
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
