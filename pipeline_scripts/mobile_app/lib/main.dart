import 'package:flutter/material.dart';
import 'API.dart';

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
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'EVI-AI'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String url = 'http://127.0.0.1:5000/api';
  //int _counter = 0;

  //void _incrementCounter() {
    //setState(() {
      //_counter++;
    //});
  //}

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
                runUser(Uri.parse(url));
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
