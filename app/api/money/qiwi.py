import requests
import json

'''
Класс qiwi с методами для работы с api qiwi
'''

class QIWI():
    def __init__(self, login, token):
        self.token = token
        # '3a802710e7f2e71ca559764a8a60df21'
        self.login = login
        # '+79069700068'
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'Bearer {token}'.format(token=token)
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/json'

    def getInfo(self):
        h = self.session.get('https://edge.qiwi.com/person-profile/v1/profile/current')
        return json.loads(h.text)

    def historyPayments(self, login, number):
        h = self.session.get("https://edge.qiwi.com/payment-history/v1/persons/{login}/payments?rows={number}"
                  .format(login=login, number=number))
        return json.loads(h.text)

    # print (history_payments(10))

    def getPaymentInfo(self, login, number):
        txnId = self.historyPayments(login, number)['data'][1]['txnId']
        types = self.historyPayments(login, number)['data'][1]['type']
        h = self.session.get("https://edge.qiwi.com/payment-history/v1/transactions/{txnId}?type={types}"
                  .format(txnId=txnId, types=types))
        return json.loads(h.text)

    # print (get_payment_info(10))

    def get_balance(self):
        h = self.session.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')
        return  json.loads(h.text)

    # print (get_balance())

    def translationQIWI(self, login, phone_number, sum, comment):
        h = self.session.get("https://edge.qiwi.com/payment-history/v1/persons/{login}/payments?rows={number}"
                  .format(login=login, number=1))
        idd =int(json.loads(h.text)["data"][0]["trmTxnId"])
        idd+=1
        data = '{ "id":"'+str(idd)+'", "sum": { "amount":'+str(sum)+', "currency":"643" }, "paymentMethod": { "type":"Account", "accountId":"643" }, "comment":"'+comment+'", "fields": { "account":"'+phone_number+'" } }'
        h = self.session.post("https://edge.qiwi.com/sinap/api/v2/terms/99/payments", data=data)
        return (h.text)

    def translationCARD(self, card_number, sum, comment):
        data = '{ "id":"11111111111114", "sum": { "amount":'+str(sum)+', "currency":"643" }, "paymentMethod": { "type":"Account", "accountId":"643" }, "comment":"'+comment+'", "fields": { "account":"'+card_number+'" } }'
        h = self.session.post("https://edge.qiwi.com/sinap/api/v2/terms/1963/payments", data=data)
        return (h.text)
#print (translation_kiwi("+79653689542"))


#myqiwi=QIWI('+79069700068','3a802710e7f2e71ca559764a8a60df21' )
#antqiwi=QIWI('+79137144010','94b289a122758199dac27ad2f47e9144')


#print(myqiwi.historyPayments("+79069700068",1)["data"][0]["trmTxnId"])
#print()
#print (antqiwi.get_balance()["accounts"][0]["balance"]["amount"])
#print(antqiwi.translationQIWI("+79069700068",2,"comment"))
#print(myqiwi.translationQIWI("+79069700068", "+79137144010",2,"comment"))
#print (myqiwi.get_balance()["accounts"][0]["balance"]["amount"])

#print(myqiwi.translationCARD("4276020705240411",2,"comment"))
