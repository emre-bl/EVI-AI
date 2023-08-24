# EVI-AI
Eyes for the Visually Impaired

YOLO KISMI

1 YOLO local image'lerden çalıştırılacak
2 YOLO local videodan opencv ile frame okuyarak çalıştırılacak
3 YOLO local videodan gstreamer ile frame okuyarak çalıştırılacak

RBG2Depth KISMI

4 RGB2Depth modelleri denenecek en iyisi bulunacak
5 RGB2D modeli local image'lerden çalıştırılacak
6 RGB2D modeli local videodan gstreamer ile frame okuyarak çalıştırılacak

7 YOLO ve RGB2D modeli birlikte çalıştırılacak
8 modellerin çıktıları rapordaki gibi formatlanacak

LLM KISMI

9 örnek çıktılarla prompt denemeleri yapılacak 
10 LLM için OpenAI, Langchain, LLaMA gibi API'lar ve kütüphaneler test edilecek
11 LLMden alınan çıktılar değerlendirilip en uygun çözüm projeye eklenecek


YOLO, RBG2Depth VE LLM kısımları ayrı başlarına istenilen şekilde koşturulabildikten sonra, önce YOLO ve RBG2Depth kısmı onlardan sonra da LLM kısmı ortak çalışacak şekilde birleştirilecek ve raporda bahsedilen arkada çalışacak olan bilgisayar üzerindeki işlemler tamamlanmış olacaktır. 

Bundan sonra LLM'den alınan metin çıktısını telefona göndermek için websocket kurulumu ile basit işleyen bir sistem ayarlanacaktır. Ve istenilen şekilde çalıştığı görüldükten sonra telefonun text-to-speech işlemi kullanılarak Bilgisayardan gönderilen metni işitsel geri dönüş olarak iletme kısmı tamamlanacaktır.

Telefondan bilgisayara görüntü gönderme kısmı için önce kablolu bağlantılarla denemeler yapılıp elimizdeki sistemin çalışabilirliğini test edilecektir. Bütün kurulum tek bir sistem içerisinde çalışabilir hale geldiğinde kablosuz bağlantı ile görüntü gönderimi tamamlanıp sistem optimizasyonlarına başlanılacaktır.

ENG

YOLO PART

1 YOLO will be run from local images 2 YOLO will be run by reading frames from local video with opencv 3 YOLO will be run by reading frames from local video with gstreamer

RBG2Depth PART

4 RGB2Depth models will be tried and the best one will be found 5 RGB2D model will be run from local images 6 RGB2D model will be run by reading frame from local video with gstreamer

7 YOLO and RGB2D model will be run together 8 outputs of the models will be formatted as in the report

LLM PART

9 prompt trials will be done with sample outputs 10 APIs and libraries such as OpenAI, Langchain, LLaMA will be tested for LLM 11 The outputs from LLM will be evaluated and the most appropriate solution will be added to the project

After the YOLO, RBG2Depth and LLM parts can be run separately as desired, first the YOLO and RBG2Depth parts will be combined to work together and then the LLM part will be combined to work together and the operations on the computer that will work in the back mentioned in the report will be completed.

After that, a simple working system will be set up with websocket setup to send the text output from the LLM to the phone. And after it is seen that it works as desired, the part of transmitting the text sent from the computer as auditory feedback will be completed by using the text-to-speech operation of the phone.

For the part of sending images from the phone to the computer, we will first test the operability of the system we have by experimenting with wired connections. When the whole installation becomes operable in a single system, image sending will be completed with wireless connection and system optimisations will be started.
