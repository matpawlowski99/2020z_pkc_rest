#!/usr/bin/env python
# coding: utf-8

# In[7]:


import http.client
import mimetypes
import json


def buy_offer(exchange, share, buy_price):
    #conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    properties = {'stockExchange': exchange, 'share': share, 'amount': 1, 'price': buy_price}
    payload = str(json.dumps(properties))
    headers = {
      'Authorization': 'Basic MDExNDM4MzFAcHcuZWR1LnBsOmhhc2Vsa28=',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/buyoffer", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #print(data.decode("utf-8"))
    return exchange, share, buy_price

def sell_offer(exchange, share, sell_price):
    properties = {'stockExchange': exchange, 'share': share, 'amount': 1, 'price': sell_price}
    payload = str(json.dumps(properties))
    headers = {
      'Authorization': 'Basic MDExNDM4MzFAcHcuZWR1LnBsOmhhc2Vsa28=',
      'Content-Type': 'application/json',
      'Cookie': 'ARRAffinity=30e33c1fd6045aee37ef50a5f26a231b54d1a1378afcfc7c824eae81a976a177; ARRAffinitySameSite=30e33c1fd6045aee37ef50a5f26a231b54d1a1378afcfc7c824eae81a976a177'
    }
    conn.request("POST", "/api/selloffer", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #print(data.decode("utf-8"))
    return exchange, share, sell_price
    
def share_price(exchange, share, flag):
#def share_price(_list, exchange_nr, share_nr):
    #conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {}
    if (flag == False):
        conn.request("GET", f"/api/shareprice/{list_of_exchanges[exchange]}?share={list_of_shareslist[exchange][share]}", payload, headers)
    elif (flag == True): 
        conn.request("GET", f"/api/shareprice/{exchange}?share={share}", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    info = json.loads(data)
    #print(info)
    buy_info = info[0]
    sell_info = info[1]
    #print(sell_info['price'])
    if (flag == False):
        return list_of_exchanges[exchange], list_of_shareslist[exchange][share], sell_info['price'], buy_info['price'], sell_info['amount']
    elif (flag == True):
        return sell_info['price'], buy_info['price']
    
def client_data():
    #conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {
      'Authorization': 'Basic MDExNDM4MzFAcHcuZWR1LnBsOmhhc2Vsa28=',
      'Cookie': 'ARRAffinity=d23c730d49f8319f1179ce5146d72f5f9c0ec35f98096df37cb77e890b012a4d; ARRAffinitySameSite=d23c730d49f8319f1179ce5146d72f5f9c0ec35f98096df37cb77e890b012a4d'
    }
    conn.request("GET", "/api/client", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    info = json.loads(data)
    #funds = info['funds']
    #shares = info['shares']
    #print(data.decode("utf-8"))
    return info['funds'], info['shares']
    
def stock_exchange_list():
    #conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {}
    conn.request("GET", "/api/stockexchanges", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #print(data)
    data_extracted = list_from_string(data)
    #print(data_extracted[0])
    #print(len(data_extracted))
    return data_extracted
    
def shares_list(exchange_nr):
    #conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {}
    conn.request("GET", f"/api/shareslist/{list_of_exchanges[exchange_nr]}", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data_extracted = list_from_string(data)
    #print(data_extracted)
    return data_extracted

def history():
    payload = ''
    headers = {
      'Authorization': 'Basic MDExNDM4MzFAcHcuZWR1LnBsOmhhc2Vsa28=',
      'Cookie': 'ARRAffinity=30e33c1fd6045aee37ef50a5f26a231b54d1a1378afcfc7c824eae81a976a177; ARRAffinitySameSite=30e33c1fd6045aee37ef50a5f26a231b54d1a1378afcfc7c824eae81a976a177'
    }
    conn.request("GET", "/api/history", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #print(data.decode("utf-8"))
    
def list_from_string(string):
    _list = list(string.split(","))
    for i, var in enumerate(_list):
        var = ''.join(filter(str.isalnum, var))
        _list[i] = var
    return _list 
    
def sort_key(price_of_share):
    return price_of_share[2]
    
#stock_exchange_list()
#shares_list()
#list_of_exchanges = []
#'''
import time

start_time = time.time()

conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")

print("ROZPOCZĘTO DZIAŁANIE PROGRAMU")
print("")
print("Aktualny stan portfela: " + str(client_data()[0]) + " PLN")
print("Zakupione akcje: " + str(client_data()[1]))
print("")

list_of_shareslist = []
list_of_tuples = []

print("Wczytuję listę dostępnych giełd...")
list_of_exchanges = stock_exchange_list()
print("Wczytano listę dostępnych giełd")
print("")
#print(list_of_exchanges)
#print(len(list_of_exchanges))

for i in range(len(list_of_exchanges)):
    if (i==0):
        print("Wczytuję listę spółek dostępnych na każdej giełdzie i pobieram aktualne oferty na ich akcje... Może to chwilę potrwać...")
    list_of_shareslist.append(shares_list(i))    #zbiór z listami spółek
    #print(list_of_shareslist[i])
    for j in range(len(list_of_shareslist[i])):
        shares_info_tuple = tuple(share_price(i, j, False))
        if (shares_info_tuple[2]<=1000):
            list_of_tuples.append(shares_info_tuple)
        #list_of_tuples.append(tuple(share_price(list_of_exchanges, i, j)))
    if (i==len(list_of_exchanges)-1):
        print("Wczytano listę spółek dostępnych na każdej giełdzie")
        print("")
        
#print(list_from_string(list_of_shareslist[0])[0])
#print(len(list_of_shareslist[0]))
#print(list_of_shareslist[0])
#print(list_of_shareslist[0][5])

print("Sortuję listę spółek według ceny ofert na ich akcje od najdroższej do najtańszej...")
list_of_tuples.sort(reverse=True, key=sort_key)
print(list_of_tuples)
print("Posortowano")
print("")
#print(client_data())

#print(client_data())
print("Kupuję i ewentualnie sprzedaję odpowiednie akcje...")
print("")

list_of_buyed_shares = []
end = False

i=0
while i==0:
    #list_of_buyed_shares = []
    for iterator_i in range(len(list_of_tuples)):
        client_funds = client_data()[0]
        if (iterator_i == 0 and list_of_tuples[len(list_of_tuples)-1][4]>=1):
            buyed_info_tuple = tuple(buy_offer(list_of_tuples[len(list_of_tuples)-1][0], list_of_tuples[len(list_of_tuples)-1][1], share_price(list_of_tuples[len(list_of_tuples)-1][0], list_of_tuples[len(list_of_tuples)-1][1], True)[0]))
            list_of_buyed_shares.append(buyed_info_tuple)
            print("Zakupiono 1 akcję spółki " + buyed_info_tuple[1] + " na giełdzie " + buyed_info_tuple[0] + " za " + str(buyed_info_tuple[2]) + " PLN")
            client_funds = client_data()[0]
        if (client_funds<=90001):
            if (client_funds<89999):
                list_of_buyed_shares.sort(reverse=False, key=sort_key)
                for iterator_j in range(len(list_of_buyed_shares)):
                    current_sell_price = share_price(list_of_buyed_shares[iterator_j][0], list_of_buyed_shares[iterator_j][1], True)[1]
                    #if (client_funds+current_sell_price<=98731):
                    selled_info_tuple = tuple(sell_offer(list_of_buyed_shares[iterator_j][0], list_of_buyed_shares[iterator_j][1], current_sell_price))
                        #list_of_buyed_shares.pop(iterator_j)
                    print("Sprzedano 1 akcję spółki " + selled_info_tuple[1] + " na giełdzie " + selled_info_tuple[0] + " za " + str(selled_info_tuple[2]) + " PLN")
                    client_funds = client_data()[0]
                    if (client_funds>=89999 and client_funds<=90001):
                        i = 1
                        end = True
                        break
                    if (client_funds>90001):
                        break
            else:
                i = 1
                break
            if (end==True):
                break
        if (client_funds-list_of_tuples[iterator_i][2]>=89999 and list_of_tuples[iterator_i][4]>=1):
            buyed_info_tuple = tuple(buy_offer(list_of_tuples[iterator_i][0], list_of_tuples[iterator_i][1], share_price(list_of_tuples[iterator_i][0], list_of_tuples[iterator_i][1], True)[0]))
            list_of_buyed_shares.append(buyed_info_tuple)
            print("Zakupiono 1 akcję spółki " + buyed_info_tuple[1] + " na giełdzie " + buyed_info_tuple[0] + " za " + str(buyed_info_tuple[2]) + " PLN")
    
print("")
print("Zakończyłem kupowanie i ewentualne sprzedawanie akcji")
print("")
print("Aktualny stan portfela: " + str(client_data()[0]) + " PLN")
print("Zakupione akcje: " + str(client_data()[1]))
    #current_shareprice = share_price(list_of_tuples[iterator_i][0], list_of_tuples[iterator_i][1], True)
    #print(current_shareprice)

print("")
print("ZAKOŃCZONO DZIAŁANIE PROGRAMU")

print("Program pracował przez: " + str(time.time()-start_time) + " s")
#'''
#print(client_data())
#print(client_data()[0])
#print(client_data()[1])


# In[ ]:




