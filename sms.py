import requests

def send_sms(number_phone):
    message = 'children need many'
    send = requests.get('http://smsc.ru/sys/send.php?login=by.sm&psw=pinlox123&phones={0}&mes={1}'.format(number_phone, message))
    return(send)

print(send_sms(79069700068))
