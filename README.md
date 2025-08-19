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

Önce projemizi yapmak istediğimiz yere gidiyoruz ve terminalde şu komutla yeni bir klasör oluşturuyoruz. Bu klasör, ileride frontend ile bağlamak isterseniz ana klasörünüz olabilir:

```
mkdir project_root
```

Ya da manuel olarak `project_root` adında, veya projenizin adınla bir klasör oluşturabilirsiniz.  

Oluşturduktan sonra terminali kullanarak bu klasörün içine girmemiz gerekiyor; çünkü gerekli komutlar bu klasörün içinde çalıştırılacak:

```
cd project_root
```

Şimdi sanal ortamı oluşturalım:

```
python -m venv venv
```

Aktifleştirmek için:

```
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Aktifleştirdikten sonra artık bu klasörü **Visual Studio Code**’da açabiliriz. Bunun için terminale şu komutu yazıyoruz:
```
code .
```
Bu komut bulunduğumuz klasörü direkt olarak VS Code’da açar. Eğer `code` komutu çalışmazsa, VS Code’u manuel olarak açıp klasörü kendiniz seçebilirsiniz.

---
## 2️⃣ İkinci Adım: Django İndirip Projeyi Oluşturma

Sanal ortamımız aktifken artık ihtiyacımız olan kütüphaneleri kurmaya başlayabiliriz. İlk olarak `Django` ve `djangorestframework` paketlerini indireceğiz.
```
pip install django djangorestframework
```
Kurulum tamamlandıktan sonra yeni bir Django projesi oluşturalım. Bunun için şu komutu yazıyoruz:
```
django-admin startproject backend .
```

Burada `backend` bizim proje adımızdır. Siz isterseniz farklı bir isim verebilirsiniz.  
Sondaki `.` ise projenin direkt olarak bulunduğumuz klasöre kurulmasını sağlar. Eğer `.` koymazsanız, Django otomatik olarak yeni bir klasör açar ve projeyi onun içine kurar.

Artık REST API geliştireceğimiz için projeye **Django REST Framework**’ü tanıtmamız gerekiyor. Bunun için `settings.py` dosyasını açıp `INSTALLED_APPS` listesine `rest_framework` ekliyoruz:

```
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Bu sayede Django, REST Framework’ü tanıyacak ve API geliştirmeye hazır hale geleceğiz 

Projemizi test etmek için şu komutla çalıştırabilirsiniz:
```
python manage.py runserver
```
Eğer tarayıcıda `http://127.0.0.1:8000/` adresine gidince Django’nun hoş geldiniz ekranını görüyorsanız her şey yolunda demektir 🚀

Projeyi test ettikten sonra `Ctrl + C` tuşlarına basarak sunucuyu durdurabilirsiniz.  

Şimdi gerçekten kütüphanelerimiz doğru bir şekilde inmiş mi diye bakalım. Bunun için terminalde şu komutu çalıştırıyoruz:

```
pip list
```
İnmesi gereken kütüphaneler:
```
Package             Version
------------------- -------
asgiref             3.9.1
Django              5.2.5
djangorestframework 3.16.1
pip                 24.0
setuptools          65.5.0
sqlparse            0.5.3
tzdata              2025.2
```


---
## 3️⃣ Migration Mantığı: makemigrations & migrate

Django’da bir model oluşturduğumuzda ya da mevcut bir modele alan eklediğimizde bu değişikliklerin veritabanına yansıması gerekir. İşte bunun için **migration** işlemlerini kullanıyoruz.  

Migration’ı kısaca şöyle düşünebilirsiniz:  

“Django’ya yaptığımız model değişikliklerini kaydet ve veritabanına uygula.”  

Bunun için iki adım vardır:  

### 1. Değişiklikleri hazırlamak
```
python manage.py makemigrations
```

Bu komut, yaptığımız değişiklikler için migration dosyaları oluşturur (yani Django’ya “şu tabloya şu sütunu ekle” gibi talimatları hazırlar).  

### 2. Veritabanına uygulamak
```
python manage.py migrate
```

Bu komut da hazırlanan migration dosyalarını çalıştırır ve değişiklikleri veritabanına uygular.  

💡 Projeye ilk başladığınızda `migrate` komutunu mutlaka çalıştırmanız gerekir çünkü Django, `User` gibi kendi hazır tablolarını da bu aşamada veritabanına ekler.



---
## 4️⃣ User Modelini Anlamak  

Django aslında bize hazır bir **User (kullanıcı) modeli** sunuyor. Yani ekstra olarak sütun tanımlamamıza gerek kalmadan, kullanıcı bilgilerini tutabileceğimiz bir yapı zaten var.  

Bu modeli kullanmak için şu şekilde içe aktarabiliriz:  

```python
from django.contrib.auth.models import User
```
diyerek projeye dahil edebiliriz.

Burada dikkat etmemiz gereken çok önemli bir nokta var:
User modelindeki alanları olduğu gibi kullanmamız gerekir. Yani örneğin first_name alanı, modelde bu şekilde tanımlandığı için firstname ya da isim gibi farklı yazarsak hata alırız.

Django’nun User modeli yalnızca alanlarla sınırlı değil; giriş-çıkış kontrolü, şifre doğrulama gibi birçok hazır metot da içeriyor. Biz bu projede temel alanları ve işlevleri kullanacağız, ama bilmenizde fayda var: Model oldukça kapsamlıdır ve gerektiğinde özelleştirilebilir

