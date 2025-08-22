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



---


## 7️⃣ Views Dosyasını Hazırlama

`views.py` dosyasında kullanıcı kayıt ve giriş işlemlerini kontrol edeceğiz. Bunun için bazı kütüphanelere ihtiyacımız var:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer
```

Açıklama:

* `api_view` → Bir fonksiyonun API endpoint’i olarak çalışmasını sağlar.
* `Response` → API’den JSON cevap döndürmek için kullanılır.
* `User` → Django’nun hazır kullanıcı modeli.
* `make_password` → Kullanıcı şifresini güvenli bir şekilde hash’lemek için.
* `status` → HTTP durum kodlarını kullanmamıza yarar (örn. 200, 400, 404).
* `SignUpSerializer` → Kullanıcı kayıt verilerini doğrulamak ve JSON formatına çevirmek için.


### Register View

Bu endpoint, yeni kullanıcı kaydı için kullanılıyor. İşleyişi şöyle:

1. Önce gelen veriler **SignUpSerializer** ile doğrulanıyor.
2. Eğer veri hatalıysa hemen hata döndürülüyor.
3. Email zaten kullanılmışsa uyarı mesajı gönderiliyor.
4. Tüm kontroller geçerse kullanıcı oluşturuluyor ve başarı mesajı döndürülüyor.

```python
@api_view(["POST"])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if not user.is_valid():
        return Response(user.errors)
    
    if User.objects.filter(username=data["email"]).exists():
        return Response({'details': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=data['email'],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=make_password(data["password"]),
    )

    return Response({'details': 'Your account registered successfully!'}, status=status.HTTP_201_CREATED)
```

Böylece hem kod daha sade hem de okunması daha kolay hale geliyor.

---
## 8️⃣ URL’leri Düzenleme
Şimdiye kadar `views.py` içinde endpointimizi yazdık ama bu endpoint’in bir adresi (yolu) yok. Kullanıcıların `http://localhost:8000/register/` gibi bir adrese giderek backend’e ulaşabilmesi için `urls.py` dosyasını hazırlamamız gerekiyor.

📌 Burada önemli nokta şu:
Django’da genelde iki katmanlı bir URL yapısı kullanıyoruz:

1. **Proje düzeyi urls.py** → (backend klasörünün içindeki `urls.py`)
2. **App düzeyi urls.py** → (bizim `account` uygulamamızın içinde yeni açacağımız `urls.py`)

Bu şekilde her uygulamanın kendi `urls.py` dosyası oluyor, projeyi daha düzenli hale getiriyor.



### Adım 1: `account` uygulamasında urls.py oluştur

Manuel olarak dosya açabilirsin ya da terminalden şu şekilde:

```bash
# Windows
New-Item -Path "account\urls.py" -ItemType "File"

# Mac/Linux
touch account/urls.py
```



### Adım 2: İçine URL tanımla

`account/urls.py` dosyası içine şunu yazıyoruz:

```python
from django.urls import path
from .views import register

urlpatterns = [
    path("register/", register, name="register"),
]
```

Burada şunu yaptık:

* `register/` adresine istek gelirse bizim `views.py` içindeki `register` fonksiyonunu çalıştır.
* `name="register"` diyerek bu endpoint’e isim verdik (ileride redirect ya da reverse kullanırken işimize yarar).

 

### Adım 3: Proje urls.py’ye dahil et

Son olarak proje düzeyindeki `backend/urls.py` dosyasına gidip `account` app’imizin URL’lerini dahil etmeliyiz:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("account.urls")),  # 👈 account app’in urls.py’sini dahil ettik
]
```

Artık `http://127.0.0.1:8000/api/account/register/` adresine `POST` isteği atarak yeni kullanıcı kaydı yapılabilir 🎉

---

## 9️⃣ Superuser (Yönetici Hesabı) Oluşturma

Django’nun bize sunduğu en güzel özelliklerden biri de **admin paneli**. Burada kullanıcıları, verileri ve modelleri yönetebiliriz. Ama bunun için önce bir yönetici hesabı (superuser) oluşturmamız gerekiyor.

Bunun için terminalde şu komutu çalıştırıyoruz:

```bash
python manage.py createsuperuser
```

Komutu verdikten sonra bizden birkaç bilgi isteyecek:

* **Username (kullanıcı adı)**
* **Email address (e-posta)**
* **Password (şifre)**

Şifreyi yazarken terminalde görünmeyecek ama endişelenme, normal bir davranış ✅

Hesabı oluşturduktan sonra artık `http://127.0.0.1:8000/admin/` adresine gidip giriş yapabilirsin.

---
## 🔟 Postman ile `register` Endpoint’ine İstek Gönderme
Önce bizim sunucu çalıştırmamız gerekiyor bu yüzden aşağıdaki komutu kullanarak django sunucusunu çalıştıralım:
```bash
python manage.py runserver
```
Eğer runserver komutunu çalıştırmazsanız Postman isteği hata dönecektir.

Artık zaten endpoint hazır, sıra test etmekte. Deponun başında dediğimiz gibi **Postman** kullanacağız.
Önce bizim metod `POST` olacak ve URL → `http://127.0.0.1:8000/api/account/register/` olacaktır. yeni kaydın bilgileri göndermemiz gerekiyor o yüzden Body → raw → JSON seçerek aşağıdaki bilgileri örnek olarak ekleyelim
```json
{
    "first_name": "Yasir",
    "last_name": "Alrawi",
    "email": "yasiralrawi@example.com",
    "password": "Django123"
}
```

NOT: **Authorization:** Hiçbir şey eklemeyin. Daha önce eklediyseniz silin.

İsteği göndermek için **Send** butonuna tıklayarak göndeririz. Ve sonuç olarak bunu görmemiz gerek:
```json
{
    "details": "Your account registered successfully!"
}
```
* Aynı e-mail varsa:
```json
{
    "details": "This email already exists!"
}
```
> Bu adım sayesinde yeni kullanıcı kayıtlarını hızlıca test edebilirsiniz.

<img width="1144" height="775" alt="Postmen Çıktısı" src="https://github.com/user-attachments/assets/5f60cdd6-a7b7-482b-83ff-ff1a3243e12c" />

1. Method olarak **POST** seçiyoruz.
2. URL kısmına `http://127.0.0.1:8000/api/account/register/` yazıyoruz.
3. **Body → raw → JSON** seçeneğini işaretliyoruz.
4. Yeni kullanıcı bilgilerimizi JSON formatında yazıyoruz.
5. **Send butonuna** tıklıyoruz.
6. Başarılı olduğunda `201 Created` durum kodunu görmemiz gerekiyor (bu, yeni kayıt oluşturuldu demektir ✅).
7. `views` dosyasında biz başarı mesajı olarak ayarladığımız için bize "Your account resgistered successfully!" döndürmesi gerek.
---


## 1️⃣1️⃣ JWT Token Almak

Şimdi kullanıcıların giriş yaptıktan sonra her istekte kim olduklarını kanıtlaması için token kullanacağız. Django REST Framework ve Simple JWT sayesinde bunu çok kolay yapabiliyoruz.


### Adım 1: Token Endpoint’i Eklemek

Proje düzeyindeki `urls.py` dosyasına aşağıdaki kütüphaneyi ve satırı ekliyoruz:
```python
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # diğer pathler...
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
```

Bu endpoint, kullanıcının **username ve password** bilgilerini alacak ve başarılıysa ona **access token** ve **refresh token** verecek.

### Adım 2: Postman ile Token Alma


<img width="1144" height="775" alt="Postmen Çıktısı" src="https://github.com/user-attachments/assets/901fea35-5aee-4288-ac80-845d92f8eef5" />


1. Postman’i aç ve yeni bir `POST` isteği oluştur.
2. URL olarak:

   ```
   http://127.0.0.1:8000/api/token/
   ```
3. Body → raw → JSON seç.
4. Aşağıdaki örnek veriyi ekle:

```json
{
    "username": "yasiralrawi@example.com",
    "password": "Django123"
}
```

5. **Send** butonuna bas.
6. Başarılı olursa durum olarak `200 OK` göstermesi gerek.
7. Başarılı olursa sonuç olarak iki token dönecek:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTg3NjAyMywiaWF0IjoxNzU1Nzg5NjIzLCJqdGkiOiI1NzQ0YzE2NThlYTc0YzM1YjM2Y2MxOWU3YjU2YzAxYSIsInVzZXJfaWQiOiIzIn0.MDsAkoq4htOu3WjOMh3sRx2_T-V8Xob0dkkLFOV1-8Q",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MDg1NjIzLCJpYXQiOjE3NTU3ODk2MjMsImp0aSI6IjY1MzFiODliYTU3ODQ1YjY4MTk1ZWZkMWI5OGQxMDIyIiwidXNlcl9pZCI6IjMifQ.6Rv5kqLRVvBue15J7w-0xtyMAq3_bhPh7Eiv4ThHE1s"
}
```

* **Access Token:** API isteğinde kullanıcıyı tanımak için kullanılır.
* **Refresh Token:** Access token süresi dolduğunda yenisini almak için kullanılır.

> Bu adım sayesinde artık kullanıcı giriş yaptıktan sonra her isteğini güvenli bir şekilde doğrulayabiliriz.


---
## 1️⃣2️⃣ Kullanıcı Bilgilerini Görüntüleme (IsAuthenticated)

Şimdi kullanıcı kendi bilgilerini Görüntülemek için tokenleri kullanmamız gerek, her seferinde giriş yapmak yerine onun aldığı tokeni kullanacağız. Bunu yapmak için `IsAuthenticated` ekleyeceğiz.


### Adım 1: Views.py Dosyasında Yeni Metot

Önce gerekli kütüphaneleri ekleyelim:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
```

Ardından yeni bir fonksiyon tanımlıyoruz:

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)
```

* `@permission_classes([IsAuthenticated])` → Bu endpoint’e **sadece giriş yapmış kullanıcılar** erişebilir.
* `request.user` → Giriş yapan kullanıcıyı temsil eder.
* `UserSerializer` → Daha önce serialiser dosyasına yazdığımız sınıf, kullanıcı verilerini JSON formatına çevirir.

### Adım 2: URL Tanımlaması

`account/urls.py` dosyasında yolunu ekliyoruz:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('userinfo/', views.current_user, name='user_info'), # 👈 yeni endpoint
]
```

Artık `http://127.0.0.1:8000/api/account/userinfo/` adresi ile kullanıcı verilerini çekebileceğiz.


### Adım 3: Postman ile Deneme
Şimdi postman kullanarak test edelim:

<img width="1144" height="775" alt="Postmen Çıktısı" src="https://github.com/user-attachments/assets/50630a5b-dc30-4044-915c-39017d0b2e50" />

1. Postman’de yeni bir `GET` isteği oluştur.
2. URL olarak:

   ```
   http://127.0.0.1:8000/api/account/userinfo/
   ```
3. **Authorization** kısmına geç.
4. Açılan pencereden **Bearer Token** seç → daha önce aldığımız **access token**’ı ekle.
5. **Send** butonuna bas.
6. Başarılı olursa durum olarak `200 OK` göstermesi gerek.
7. Başarılı olursa kendi kullanıcı bilgilerini JSON formatında göreceksin:

```json
{
    "username": "yasiralrawi@example.com",
    "email": "yasiralrawi@example.com",
    "first_name": "Yasir",
    "last_name": "Alrawi"
}
```

> Bu adım sayesinde endpointlerimizi güvenli hale getirdik ve kullanıcılar sadece kendi verilerini görebiliyor.


---


## 1️⃣3️⃣ Kullanıcı Bilgilerini Güncelleme
Artık kullanıcı giriş yaptı ve kendi bilgilerini görebiliyor. Şimdi kendi kullanıcı bilgilerini güncelleyebilmesini sağlayacağız.


### Adım 1: Views.py Dosyasında Yeni Fonksiyon

Önce gerekli kütüphaneler zaten ekliydi; tekrar eklemeye gerek yok. Yeni bir fonksiyon ekliyoruz:

```python
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    # Mevcut kullanıcı bilgilerini güncelle
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.username = data.get('email', user.username)  # username email olarak tutuluyor

    # Şifre güncelleme opsiyonel
    if data.get('password'):
        user.set_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
```

* `@permission_classes([IsAuthenticated])` → Bu endpoint’e sadece giriş yapmış kullanıcılar erişebilir.
* `request.user` → Güncellenmek istenen kullanıcıyı temsil eder.
* `user.save()` → Değişiklikleri veritabanına kaydeder.
* Şifre değişimi yapılırsa `set_password()` kullanıyoruz ki şifre hashlenmiş şekilde saklansın.

---

### Adım 2: URL Tanımlaması

`account/urls.py` dosyasına ekliyoruz:

```python
urlpatterns = [
    path('register/', views.register, name='register'),
    path('userinfo/', views.current_user, name='user_info'),
    path('update/', views.update_user, name='update_user'),  # 👈 yeni endpoint
]
```

Artık `http://127.0.0.1:8000/api/account/update/` adresi ile kullanıcı bilgilerini güncelleyebiliriz.

---

### Adım 3: Postman ile Deneme
Güncelleme işlemi deneyelim:

<img width="1144" height="775" alt="1 (8)" src="https://github.com/user-attachments/assets/7127c4b0-8045-48b3-af56-5d5f69093bba" />



1. Postman’de yeni bir **PUT** isteği oluştur.
2. URL:

   ```
   http://127.0.0.1:8000/api/account/update/
   ```
3. **Authorization** kısmında biraz önceki eklediğimiz **Bearer Token** ekli olduğundan emin ol.
4. Body → raw → JSON ile güncellemek istediğin bilgileri gönder:

```json
{
    "username": "yasiralrawiguncellenmistir@example.com",
    "email": "yasiralrawiguncellenmistir@example.com",
    "first_name": "Yasir-guncellenmistir",
    "last_name": "Alrawi-guncellenmistir"
}
```

5. **Send** butonuna bas.
6.  Başarılı olursa `200 OK` durumunu göreceksin.
7.  Başarılı olursa güncellenmiş kullanıcı verilerini JSON olarak alırsın.


---
## 1️⃣4️⃣ Mailtrap ile E-Posta Gönderme Ayarları

Kullanıcı kayıt olurken veya şifresini unuttuğunda **e-posta göndermek** için Mailtrap kullanacağız.
Mailtrap, geliştirme aşamasında gerçek maillere gitmeden test etmemizi sağlayan güvenli bir SMTP servisidir.

### Adım 1: Mailtrap Hesabı Açma

👉 Önce [Mailtrap](https://mailtrap.io/register/signup?ref=header) adresine girip ücretsiz bir hesap oluşturuyoruz.
👉 Daha sonra **Inbox** oluşturarak SMTP ayarlarını kopyalıyoruz.

<img width="1919" height="912" alt="Mailtrap" src="https://github.com/user-attachments/assets/a3f24592-bca6-4bf2-b198-4f6c414a0259" />

1. Sandboxes'a tıklayacaksın.
2. Seçeneklerden `Django` seçeceksin.
3. Settings.py dosyasına eklenmesi gereken SMTP bilgileri göreceksin.
4. Copy butonuna tıklayarak kopyalayacaksın.

### Adım 2: settings.py Dosyasına SMTP Bilgilerini Ekleme

Mailtrap’ten aldığımız bilgileri `settings.py` dosyamıza ekliyoruz:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'host_user'       # Mailtrap'in verdiği kullanıcı adı
EMAIL_HOST_PASSWORD = 'host_password'  # Mailtrap'in verdiği şifre
EMAIL_PORT = 2525

# Geliştirme ortamı için:
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
```

⚠️ **Dikkat:**

* Geliştirme ortamında TLS/SSL kapalı tutuyoruz.
* **Gerçek sunucuda (production)** çalıştırırken:

  ```python
  EMAIL_USE_TLS = True
  EMAIL_USE_SSL = True
  ```


## 1️⃣5️⃣ Kullanıcı Şifre Sıfırlama Modeli ve Fonksiyonları
Şimdi kullanıcıların şifresini sıfırlayabilmesi için **Profile modeli** oluşturacağız. Bu model, kullanıcıya ait ekstra bilgileri tutacak (ör. reset token ve süresi).


### Adım 1: Gerekli kütüphaneleri ve modelleri tanımlamak
Profile modeli oluşturmak için bu kütüphaneleri kullanmaya ihtiyacımız olacaktır, bu yüzden `models.py` içine şunları ekliyoruz:

```python
from django.dispatch import receiver
from django.db.models.signals import post_save
```

Ondan sonra `Profile` modeli oluşturalım:
```python
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, default="", blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)
```

Bir kullanıcı (User) oluşturulduğunda otomatik olarak Profile da oluşturulsun istiyoruz bu yüzden Tam Profile modelin altında `receiver` tanımlayacağız:

```python
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
```

### Adım 2: Host bilgisini almak

Şimdi `views.py` dosyasına geçiyoruz. Önce gerekli yeni kütphaneleri dahil edeceğiz:

```python
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
```

Kullanıcıya şifre sıfırlama linki göndereceğimiz için host adresini dinamik almak gerekiyor. Bu fonksiyonu biraz sonra tanımlayacağımız linki gönderen fonksiyonun içinde kullanacağız:

```python
def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{protocol}://{host}/"
```

Artık şifre sıfırlama fonksiyonumuzu yazmaya başlayabiliriz:
```python
@api_view(["POST"])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=20)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = f"{host}api/reset_password/{token}"

    body = (
        f"Hello {user.first_name},\n\nWe received a request to reset your password."
        f" Please use the link below to set a new password. This link will expire in 20 minutes.\n\n"
        f"Reset Password Link: {link}\n\n"
        "If you did not request a password reset, please ignore this email."
    )

    send_mail(
        "Password Reset Request for Your Account",
        body,
        "no-reply@example.com",
        [user.email],
        fail_silently=False,
    )

    return Response({'details': f'A password reset link has been sent to {user.email}.'})
```

### Adım 3: URL tanımlamaları
`account/urls.py` içinde yeni endpointimizi ekliyoruz:

```python
urlpatterns = [
    path('register/', views.register, name='register'),
    path('userinfo/', views.current_user, name='user_info'),
    path('update/', views.update_user, name='update_user'),
    path('forget_password/', views.forget_password, name='forget_password'),  # 👈 yeni endpoint
]
```

### Adım 4: Migration Oluşturma
Yeni model eklediğimiz için yeni bir migration oluşturup veri tabana uygulamamız gerekiyor bu yüzden terminalde bu komutları kullanacğaız:

Migrations oluşturmak için:
```bash
python manage.py makemigrations
```
Veri tabana uygulamak için:
```bash
python manage.py migrate
```

### Adım 5: Postman ile test
1. Önce sunucuyu çalıştır:

```bash
python manage.py runserver
```

2. Postman’da `POST` metodu ile `http://127.0.0.1:8000/api/account/forget_password/` adresine kullanıcı mailini JSON olarak gönder.
