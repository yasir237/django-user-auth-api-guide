# Django Kullanıcı Yönetim API Projesi Oluşturma Kılavuzu
Bu proje, Django ve Django REST Framework kullanarak **temel bir kullanıcı yönetim sistemi** oluşturmak isteyenler için hazırlanmış bir kılavuzdur.

Amacımız, kullanıcıların kayıt olabildiği, giriş yapabildiği, profillerini görebildiği ve admin kullanıcıların diğer kullanıcılar üzerinde CRUD işlemleri yapabildiği bir temel yapı oluşturmaktır.

Aynı zamanda hesapların güvenliğini sağlamak için token tabanlı doğrulama yöntemlerini kullanacağız.  
Ek olarak, bir kullanıcı şifresini unuttuğunda e-posta yoluyla şifre sıfırlama işleminin nasıl yapılacağını göstereceğiz.

Projeyi takip ederek kendi API projenizi hızlıca ayağa kaldırabilir ve kullanıcı yönetimi mantığını öğrenebilirsiniz.

---
Bu projede **Python 3.11.9** kullanılacak. Ben **Visual Studio Code** ile göstereceğim ve Python ile gerekli kütüphanelerin kurulu olduğunu varsayıyorum. Başlamadan önce kurulu olduğundan emin olun.

Ben **Windows** üzerinden anlatacağım, ama eğer siz farklı bir işletim sistemi kullanıyorsanız bazı komutlar farklı olabilir. Yine de merak etmeyin, göstermediğim detaylar için ChatGPT hep yanınızda (:

Projeye başlamadan önce bir de **Postman**’ı kullanacağımızı bilmenizde fayda var. Yani API’ye istekler atıp, yaptığımız işlemlerin sonucunu hemen görebileceğiz. Böylece hem mantığı daha iyi anlayacağız hem de testlerimiz hızlı olacak.

İndirmek için buraya tıklayabilirsiniz: [Postman İndir](https://www.postman.com/downloads/)

---

## 1️⃣ İlk Adım: Sanal Ortam Oluşturma

Genelde projelerde çok fazla kütüphane olur ve her kütüphane başka projelere etki edebilir. Bu yüzden biz **sanal ortam** oluşturuyoruz; yani her projeyi izole bir ortamda tutuyoruz. Böylece kütüphaneler karışmaz ve her şey düzenli kalır.

Önce projemizi nerede yapmamızı istediğimiz yere gidiyoruz ve terminalde bu şekide bir komut kullanarak yeni bir klasör oluşturalım, bu klasörde ilerde frontend ile bağlamanız istiyorsanız bu ana klasörde oluşturabilirsiniz ve kolayca oluşturabilirsiniz. yeni bir klasör oluşturmamızı sağlayan komut:
```
mkdir project_root
```
ya da siz manual olarak `project_root` adılı veya sizin seçmek istediğiniz bir isimle bir klaösr oluşturabilirsiniz. Oluşturduktan sonra bu terminali kullanarak bu klasörün içine girmemiz gerek çünkü gerekli komutlar bu klasörün içinde çalıştırmamız gerek. klasörün içinde girmek için bu komutu kullanacağız:
```
cd project_root
```

Şimdi sanal ortamı oluşturalım, oluşturmak için kullanacağımız komut:
``` 
python -m venv venv
```
Aktifleştirmek için
```
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

