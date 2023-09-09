import json
import paramiko
import threading
import yaml
from jinja2 import Template, Environment, FileSystemLoader


# Fungsi untuk melakukan koneksi SSH ke perangkat
def connect_to_router(router):
    ip = router["ip"]
    username = router["username"]
    password = router["password"]

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username=username, password=password, port=3232)

        # Sekarang Anda dapat melakukan sesuatu dengan perangkat,
        # seperti mengirimkan perintah melalui SSH, misalnya:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        print(f"Informasi dari {ip}:\n{output}")

    except Exception as e:
        print(f"Terjadi kesalahan saat terhubung ke {ip}: {str(e)}")
    finally:
        ssh_client.close()  # Tutup koneksi SSH setelah selesai


# Baca nilai dari file YAML
with open("param.yml", "r") as config_file:
    config_data = yaml.safe_load(config_file)

# Muat template Jinja2
env = Environment(loader=FileSystemLoader(""))
template = env.get_template("template.j2")

# Render template dengan data dari YAML
command = template.render(config_data)

# Baca data dari file JSON
with open("list.json", "r") as json_file:
    router_data = json.load(json_file)

# Buat thread untuk setiap router
threads = []
for router in router_data["routers"]:
    thread = threading.Thread(target=connect_to_router, args=(router,))
    threads.append(thread)
    thread.start()

# Tunggu semua thread selesai
for thread in threads:
    thread.join()
