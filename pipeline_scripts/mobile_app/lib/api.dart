import 'package:http/http.dart' as http;


Future runUser(url) async {
    http.Response response = await http.get(url);
    return response.body;
}