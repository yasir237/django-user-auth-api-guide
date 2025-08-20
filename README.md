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
## 4️⃣ Simple JWT Kurulumu  

Şimdi kullanıcıların giriş yapabilmesi ve her istekte kim olduklarını kanıtlayabilmesi için bir yöntem eklememiz gerekiyor. Django REST Framework (DRF) ile en çok kullanılan yöntemlerden biri **JWT (JSON Web Token)**. 

Biz bu projede JWT’yi kullanmak için **Simple JWT** kütüphanesini ekleyeceğiz.  

Biz de bu projede JWT için Simple JWT kütüphanesini kullanacağız.
Merak edenler için resmi [dokümantasyonu](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation) da bırakıyorum.
 
Kurmak için terminale şu komutu yazalım:
```bash
pip install djangorestframework-simplejwt
```

### Ayarlar
Kurulumdan sonra `settings.py` dosyamızda birkaç ayar yapmamız gerekiyor.

👉 Önce `REST_FRAMEWORK` kısmına JWT’yi ekliyoruz:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```
👉 Daha sonra `INSTALLED_APPS` içine şunu ekliyoruz:
```python
INSTALLED_APPS = [
    .
    .
    .
    'rest_framework_simplejwt',
]
```

👉 Token sürelerini ayarlamak için en üstte `timedelta` import ediyoruz:
```python
from datetime import timedelta
```
Ardından aşağıdaki ayarları ekleyelim:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'BLACKLIST_AFTER_ROTATION':True,
    'AUTH_HEADER_TYPES':('Bearer',),
    'AUTH_TOKEN_CLASSES':('rest_framework_simplejwt.tokens.AccessToken',),
}
```
* **Access Token** → Kullanıcının giriş anahtarı. Her istekte kim olduğunu kanıtlar ama kısa süre sonra geçersiz olur.
* **Refresh Token** → Access token bittiğinde yeni bir tane almak için kullanılır. Daha uzun ömürlüdür.
* **ACCESS\_TOKEN\_LIFETIME** → Access token’ın geçerlilik süresi.
* **REFRESH\_TOKEN\_LIFETIME** → Refresh token’ın geçerlilik süresi.
* **BLACKLIST\_AFTER\_ROTATION** → Refresh token kullanıldığında eskisini geçersiz yapar.
* **AUTH\_HEADER\_TYPES** → Token’ın başına ne yazacağımız. Genelde `Bearer`.
* **AUTH\_TOKEN\_CLASSES** → Kullanılacak token tipi. Biz `AccessToken` kullanıyoruz.

---

## 5️⃣ Account Uygulaması Oluşturma
Artık kullanıcılarla ilgili işlemleri ayrı bir uygulama içinde yapacağız. Bunun için `account` adında bir app oluşturuyoruz, isterseniz siz `hesap` veya başka bir isim verebilirsiniz

```bash
python manage.py startapp account
```
Oluşturulduktan sonra `settings.py` dosyasında **INSTALLED_APPS** kısmına ekliyoruz:
```bash
INSTALLED_APPS = [
    .
    .
    .
    'account.apps.AccountConfig',
]
```

---
## 6️⃣ Serializers Oluşturma

Django REST Framework’te **serializer**’lar, modellerimizi JSON’a çevirmemizi ve gelen JSON verilerini modele dönüştürmemizi sağlar. Yani kısaca API’nin veri formatını yönetiyorlar.

`account` uygulamamızı oluşturduğumuzda fark edeceğiz ki, `account` adında yeni bir klasör oluştu. Bu klasörün içinde `serializers.py` dosyasını manuel olarak oluşturabilir veya terminalden şu komutları kullanabilirsiniz:
```bash
# Windows
New-Item -Path "account\serializers.py" -ItemType "File"

# Mac/Linux:
touch account/serializers.py
```

İlk olarak kullanacağımız kütüphaneleri tanımlıyoruz:
```bash
from rest_framework import serializers
from django.contrib.auth.models import User
```

* `rest_framework.serializers` sayesinde serializer özelliklerini kullanabileceğiz.
* `User` modeli, Django’nun bize sunduğu hazır kullanıcı modelidir; ekstra sütun tanımlamamıza gerek yok.

⚠️ Önemli: User modelindeki alanları **tam olarak** yazmalıyız. Örneğin `first_name` alanını `firstname` veya `isim` gibi yazarsak hata alırız.

Django’nun User modeli sadece alanlardan ibaret değil; giriş-çıkış, şifre doğrulama gibi birçok hazır metot da içeriyor. Biz bu projede temel alanları ve işlevleri kullanacağız, ama modelin oldukça kapsamlı olduğunu bilmekte fayda var.

Yeni kayıt olmak için gerekli bilgileri belirten bir sınıf oluşturuyoruz:

```python
class SignUpSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False, "min_length": 8},
        }
```
Bu serializer sayesinde kullanıcıdan hangi bilgileri alacağımızı ve her alanın zorunluluklarını belirlemiş oluyoruz.

Aynı `serializers.py` dosyasında, yukarıda tanımladığımız `SignUpSerializer`’ın altında başka bir sınıf oluşturuyoruz: **`UserSerializer`**.

Bu sınıf, kullanıcı kayıt olduktan sonra onun bilgilerini göstermek için kullanılacak. Örnek olarak şöyle tanımlayabiliriz:

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
```

Böylece kullanıcı bilgilerimizi API üzerinden döndürebiliriz.



