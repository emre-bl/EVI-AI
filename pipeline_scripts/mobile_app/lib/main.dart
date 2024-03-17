import 'package:flutter/material.dart';
//import 'API.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:async';

import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
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
  bool shouldPlayStartSound = true; // Flag to control start sound playback
  bool ifStarted = false; // Initial state of the button
  bool allowPlayStartSound = true; // Flag to control start sound playback

  Future<void> runUserScript() async {
  final uri = Uri.parse('http://127.0.0.1:5000/runscript');
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
    audioPlayer.dispose();
    super.dispose();
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
