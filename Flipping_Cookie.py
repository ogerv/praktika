##Нужен для запроса на криптохак
import requests
##Нужен для того, чтобы десериализовать ответ с криптохака(куку)
import json
## XOR, тут и так понятно
from Crypto.Util.strxor import strxor

##Получает с криптохака куку и десереализует ее в текст
def get_cookie():
	return requests.get('https://aes.cryptohack.org/flipping_cookie/get_cookie/').json()

##Отправляет куку с iv на криптохак и получает флаг
def get_flag(cookie, iv):
	return requests.get('https://aes.cryptohack.org/flipping_cookie/check_admin/'+cookie+'/'+iv).json()
##Кука с криптохака
Cookie=get_cookie()['cookie']
##iv, выдранный из куки
IV=bytes.fromhex(Cookie[:32])

##потребуются для подмены
FalseAdminBytes=b'admin=False;expi'  
TrueAdminBytes=b'admin=True;expir'

##Для того, чтобы подменить значение admin-а мы "ксорим" iv и значение admin=false, т.к. "ксорить" саму зашифрованную строку нет смысла
XORedIVFalse=strxor(IV,FalseAdminBytes)
##Тут мы получаем модифицированный iv, который уже при расшифровке даст нам admin=true
XORedIVTrue=strxor(TrueAdminBytes,XORedIVFalse).hex()

print(get_flag(Cookie[32:],XORedIVTrue)["flag"])
