import requests
from bs4 import BeautifulSoup
from requests_toolbelt.utils import dump

API_IGRACIAS_MOBILE = "https://igracias.ittelkom-pwt.ac.id/api/android/ittp_api.php"
API_IGRACIAS_WEB = "https://igracias.ittelkom-pwt.ac.id/"
API_QR_CODE = 'https://zxing.org/w/decode'


class requestCollection:
    def __init__(self):
        pass

    def get_jadwal(self, nim):
        get_jadwal = requests.get(API_IGRACIAS_MOBILE, params={"mod": "jadwalMahasiswa", "studentid": nim})
        parse = BeautifulSoup(get_jadwal.text, "html.parser")

        jadwal = []
        for i in parse.find_all("tr"):
            data = i.text.split(" ")[0]
            if data == "JADWAL" :
                print("String JADWAL ditemukan")
                continue

            jadwal.append(i.text.replace("\n", "").replace("\t", "").replace("\r", "\n") + "\n\n")

        return jadwal

    def get_kehadiran(self, nim):
        get_kehadiran = requests.get(API_IGRACIAS_MOBILE, params={"mod": "RekapKehadiranMahasiswa", "studentid": nim})
        parse = BeautifulSoup(get_kehadiran.text, "html.parser")

        kehadiran = []
        for i in parse.find_all("tr"):
            if "NAMA MATA KULIAH" in i.text:
                continue
            kehadiran.append(i.text)

        tmp_kehadiran = []
        for i in kehadiran:
            tmp_kehadiran.append({
                "nama_matkul": i.split("\n")[0],
                "hadir": i.split("\n")[1],
                "Pertemuan": i.split("\n")[2],
                "Persentase": i.split("\n")[3]
            })
        return tmp_kehadiran

    def get_link_matkul(self, username, password, nim):
        get_php_session = requests.get(
            url=API_IGRACIAS_WEB,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }
        )
        get_headers = get_php_session.headers["Set-Cookie"].split(";")[0]

        get_login = requests.post(
            url=API_IGRACIAS_WEB,
            data={"textUsername": username, "textPassword": password, "submit": "Login"},
            headers={
                "Cookie": get_headers,
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            },
            timeout=30
        )

        if "Username and Password not correct or not match!" in get_login.text:
            return False
        else:
            requests.get(
                url=API_IGRACIAS_WEB + "/registration/?pageid=17985",
                headers={
                    "Cookie": get_headers,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
                },
                timeout=30
            )
            get_link_matkul = requests.get(
                url=API_IGRACIAS_WEB + "libraries/ajax/ajax.schedule.php",
                params={"act": "viewStudentSchedule", "studentId": nim},
                headers={
                    "Host": "igracias.ittelkom-pwt.ac.id",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "X-Requested-With": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
                    "Referer": "https://igracias.ittelkom-pwt.ac.id/registration/?pageid=17985",
                    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
                    "Cookie": get_headers,
                },
                timeout=30
            )
            return get_link_matkul

    def get_scan_qrcode(self, nim, data):
        get_scan_qrcode = requests.get(
            url=API_IGRACIAS_MOBILE + "?mod=presensiMhs&usid={nim}&urlid={data}".format(nim=nim, data=data),
        )
        return get_scan_qrcode

    def parse_qr_code(self, file):
        files = {'f': open(file, 'rb')}
        r = requests.post(url=API_QR_CODE, files=files)
        print("[DEBUG] QR CODE REQUEST : " + r.text)
        parse = BeautifulSoup(r.text, 'html.parser')

        if r.text == "Forbidden":
            return False
        elif "Decode Succeeded" in parse.find('h1').text:
            return parse.find('pre').text
        else:
            return False
