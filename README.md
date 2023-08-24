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
