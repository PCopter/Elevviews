
# Elevview
Elevview Web application ถูกพัฒนาขึ้นด้วย Django framework ซึ่งภายในประกอบด้วย 3 องค์ปรกอบหลักคือ 
- Backends --> Python 
- Frontends --> HTML, JsและCSS
- Database --> MySQL

โดย Elevview ถูก deploy บน AWS EC2 และใช้ AWS S3 เป็น storages
## Install and Run Elevview by VSCode (on localhost)
0.ติดตั้ง Python, Pipenv, MySQL, MySQLWorkbench ลงเครื่องให้เรียบร้อยก่อน
- https://www.mysql.com/downloads/
- https://dev.mysql.com/downloads/workbench/
- https://www.python.org/downloads/
```bash
pipenvinstall
```
1. ดาวน์โหลดโปรเจ็คนี้ลงเครื่อง หรือทำการ clone ลงเครื่อง
```bash
git clone https://github.com/PCopter/Elevviews.git
```
2. เปิดโฟลเดอร์โปรเจ็คใน VSCode ไปที่ project/setting แล้วให้ 
- [ ] commend สำหรับการพัฒนาบน cloud --> AWS EC2 และ whitenose
- [x] uncommend สำหรับการพัฒนาบนเครื่องตนเอง 
```bash
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', --> commend
]
DATABASES = {
    # สำหรับการพัฒนาบนเครื่องตนเอง
    # 'default': {
    #     'ENGINE': 'mysql.connector.django',
    #     'ENGINE': 'django.db.backends.mysql',  
    #     'NAME': os.getenv("DB_NAME"),
    #     'USER' : os.getenv("DB_USER"),
    #     'PASSWORD' : os.getenv("DB_PASSWORD"),
    #     'HOST' : os.getenv("DB_HOST", "localhost"),
    #     'PORT' : os.getenv("DB_PORT", "3306"),
    #     'OPTIONS': {
    #         'charset': 'utf8mb4', 
    #     },
    # } 
    # สำหรับการพัฒนาบน cloud --> AWS EC2
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'Elevviews',
        'PASSWORD': 'cC.053346532',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
             'charset': 'utf8mb4', 
         },
    }
}
```
3. เปิดไฟล์ project_jrd/.env.sample แล้วเปลี่ยนชื่อเป็น .env จากนั้นให้เปลี่ยนการตั้งค่าให้สอดคล้องกับเครื่องของคุณ เสร็จแล้วบันทึกไฟล์ได้เลย
4. เปิด VSCode Terminal
5. ติดตั้ง Packages ของโปรเจ็ค
```bash
pipenv install
```
6. Activate pipenv environment
```bash
pipenv shell
```
7. จัดการ Database migrations ให้เรียบร้อย
```bash
python manage.py migrate
```
8. สร้าง Admin (Super user) ให้เรียบร้อย
```bash
python manage.py createsuperuser
```
9. เปิดเว็บโปรเจ็ค
```bash
python manage.py runserver
```
อาจศึกษาเพื่มเติมได้ที่ 
https://www.youtube.com/watch?v=BBL8W-lpNHw และ
https://www.youtube.com/watch?v=tTi2QxB1HJ8
## Install and Run Elevview by VSCode (on AWS EC2)

1. สร้าง EC2 Instance
2. ติดตั้ง Dependencies บน EC2
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```
3. Clone Django Project และตั้งค่า Virtual Environment
```bash
cd /home/ubuntu
git clone https://github.com/PCopter/Elevviews.git
cd your-repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. ตั้งค่า Database (MySQL)
```bash
sudo mysql
```
ภายใน MySQL prompt:
```sql
CREATE DATABASE mydb;
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
EXIT;
```

ตั้งค่า `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'your-ec2-public-ip',
        'PORT': '3306',
    }
}
```
5. จัดการ Database migrations ให้เรียบร้อย
```bash
python manage.py migrate
```
6. สร้าง Admin (Super user) ให้เรียบร้อย
```bash
python manage.py createsuperuser
```
7. เปิดเว็บโปรเจ็ค
```bash
python manage.py runserver 0.0.0.0:8000
```
อาจศึกษาเพื่มเติมได้ที่ 
https://www.youtube.com/watch?v=uiPSnrE6uWE และ
https://www.youtube.com/watch?v=tryZWxTVDks
