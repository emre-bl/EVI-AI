import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:async';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
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

  Future<void> runUserScript() async {
    //final uri = Uri.parse('http://127.0.0.1:5000/runscript');
    final uri = Uri.parse('http://10.0.2.2:5000/runscript');
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
        playStartSound();
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

  void playSound() async {
    if (!shouldPlayStartSound) {
      await audioPlayer.play(AssetSource('LLM_output.mp3')); // Your periodic sound file
    }
  }

  void startTimer() {
    timer = Timer.periodic(Duration(seconds: 5), (Timer t) async {
      await audioPlayer.play(AssetSource('LLM_output.mp3'));
    });
  }

  @override
  void dispose() {
    timer?.cancel();
    timer2?.cancel();
    audioPlayer.dispose();
    //cameraController?.dispose();
    super.dispose();
  }

  void startTimerForFrames() {
    const period = Duration(seconds: 20); // Set the period to 20 seconds
    timer2 = Timer.periodic(period, (Timer t) async {
      await captureAndSendFrame(); // Capture and send the frame
    });
  }

  // Method to capture and send frame
  Future<void> captureAndSendFrame() async {
    if (cameraController != null && cameraController!.value.isInitialized) {
      final XFile image = await cameraController!.takePicture(); // Capture a frame

      // Convert image to a byte array
      final bytes = await image.readAsBytes();

      // Prepare for HTTP request
      //final uri = Uri.parse('http://127.0.0.1:5000/runscript'); // Adjust the URL to your server endpoint
      final uri = Uri.parse('http://10.0.2.2:5000/runscript');
      final headers = {'Content-Type': 'application/json'};
      final body = json.encode({'image': base64Encode(bytes)}); // Encode the byte array to a Base64 string

      try {
        final response = await http.post(uri, headers: headers, body: body);
        if (response.statusCode == 200) {
          debugPrint("Frame sent successfully");
        } else {
          debugPrint("Failed to send frame. Server error: ${response.body}");
        }
      } catch (e) {
        debugPrint("Error sending the frame: $e");
      }
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
        child: SizedBox.expand( // This will expand to fill all the available space
          child: Padding(
            padding: const EdgeInsets.all(16.0), // Add some padding around the button
            child: ElevatedButton(
              onPressed: () {
                setState(() {
                  ifStarted = !ifStarted; // Toggle the state
                  if (ifStarted) {// 'Stop' button is pressed
                    // stop the start sound and start the timer
                    runUserScript();
                    stopStartSound(); // Ensure the start sound is stopped before starting the timer
                    startTimer(); // Start the timer for the periodic sound
                    startTimerForFrames(); // Start the timer for capturing and sending frames
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
                minimumSize: Size(double.infinity, double.infinity), // Set the button size to as big as its parent allows
                elevation: 0, // Removes elevation shadow
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.zero), // Removes rounded borders
                // If you want to have no visual difference when the button is pressed:
                tapTargetSize: MaterialTapTargetSize.shrinkWrap, // Removes additional space for the ink splash
              ),
              child: Text(
                ifStarted ? 'Stop' : 'Start',
                style: TextStyle(fontSize: 48),
              ),
            ),
          ),
        ),
      ),

    );
  }
}
