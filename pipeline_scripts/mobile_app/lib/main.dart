import 'package:flutter/material.dart';
import 'API.dart';
import 'package:audioplayers/audioplayers.dart';
import 'dart:async';

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
  String url = 'http://127.0.0.1:5000/api';
  AudioPlayer audioPlayer = AudioPlayer();
  Timer? timer;
  bool shouldPlayStartSound = true; // Flag to control start sound playback


  /*Future callPythonScript(Url) async {
    http.Response Response = await http.get(Url);
    return Response.body;
  }*/
  /*Future<void> callPythonScript() async {
    // Replace with the URL of your backend server
    var url = Uri.parse('https://github.com/emre-bl/EVI-AI/blob/main/pipeline_scripts/user.py');

    try {
      var response = await http.post(url);
      if (response.statusCode == 200) {
        print('Script executed successfully');
        // Handle the response data
      } else {
        print('Failed to execute script: ${response.reasonPhrase}');
      }
    } catch (e) {
      print('Error calling the backend server: $e');
    }
  }*/

  @override
  void initState() {
    super.initState();
    playStartSound(); // Play the start sound immediately on app start
  }

  void playStartSound() async {
    await audioPlayer.play(AssetSource('start_sound.mp3')); // Play the start sound
    audioPlayer.onPlayerComplete.listen((event) {
      if (shouldPlayStartSound) {
        playStartSound(); // Replay the sound if the flag is still true
      }
    });
  }

  void playSound() async {
    if (!shouldPlayStartSound) { // Check if we should play the sound
      await audioPlayer.play(AssetSource('output.mp3')); // Your periodic sound file
    }
  }

  void startTimer() {
    shouldPlayStartSound = false; // Stop the start sound loop when the timer starts
    // This function starts the timer when the user presses the start button
    timer = Timer.periodic(Duration(seconds: 5), (Timer t) => playSound());
  }

  @override
  void dispose() {
    timer?.cancel();
    audioPlayer.stop(); // Stop any playing sound
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
                if (shouldPlayStartSound) {
                  // Stop the start sound and prevent it from playing again
                  audioPlayer.stop();
                  shouldPlayStartSound = false;
                  startTimer(); // Start the timer for the periodic sound
                }
                //runUser(Uri.parse(url));
              },
              style: ElevatedButton.styleFrom(
                minimumSize: Size(double.infinity, double.infinity), // Set the button size to as big as its parent allows
                elevation: 0, // Removes elevation shadow
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.zero), // Removes rounded borders
                // If you want to have no visual difference when the button is pressed:
                tapTargetSize: MaterialTapTargetSize.shrinkWrap, // Removes additional space for the ink splash
              ),
              child: Text(
                'Start',
                style: TextStyle(fontSize: 48),
              ),
            ),
          ),
        ),
      ),

    );
  }
}
