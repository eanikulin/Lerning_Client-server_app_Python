import subprocess


def ping(host):
    args = ['ping', host]
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in subproc_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))


ping('yandex.ru')
ping('youtube.com')
