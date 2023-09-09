import yaml
from jinja2 import Template, Environment, FileSystemLoader
import paramiko

# Baca nilai dari file YAML
with open("config.yml", "r") as config_file:
    config_data = yaml.safe_load(config_file)

# Muat template Jinja2
env = Environment(loader=FileSystemLoader(""))
template = env.get_template("template.j2")

# Render template dengan data dari YAML
output = template.render(config_data)

# print(output)

# paramiko membuat koneksi SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Parameter Perangkat yang akan diremote
router_ip = "182.23.107.170"
user = "cperooot"
password = "N4sional"

# terhubung ke perangkat
ssh_client.connect(router_ip, username=user, password=password, port=3232)

# Perintah yang akan dikirimkan
command = output

# kirim perintah ke perangkat
stdin, stdout, stderr = ssh_client.exec_command(command)

# menampilkan output (stdout) atau tangani pesan error (stderr)
print(stdout.read().decode())

# tutup koneksi ssh
ssh_client.close()

print("Konfiguration completed!")
