#!/usr/bin/env python
# coding: utf-8

# In[26]:


import http.client
import mimetypes
import json


def buy_offer():
    conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    properties = {'stockExchange': 'Warszawa', 'share': 'MBANK', 'amount': 1, 'price': share_price()}
    payload = str(json.dumps(properties))
    headers = {
      'Authorization': 'Basic MDExNDM4OTVAcHcuZWR1LnBsOmR6ZWtpMjM=',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/buyoffer", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
def share_price():
    conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {}
    conn.request("GET", "/api/shareprice/Warszawa?share=MBANK", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    info = json.loads(data)
    #print(info)
    buy_info = info[0]
    sell_info = info[1]
    print(sell_info['price'])
    return sell_info['price']
    
def client_data():
    conn = http.client.HTTPSConnection("stockserver.azurewebsites.net")
    payload = ''
    headers = {
      'Authorization': 'Basic MDExNDM4OTVAcHcuZWR1LnBsOmR6ZWtpMjM=',
      'Cookie': 'ARRAffinity=d23c730d49f8319f1179ce5146d72f5f9c0ec35f98096df37cb77e890b012a4d; ARRAffinitySameSite=d23c730d49f8319f1179ce5146d72f5f9c0ec35f98096df37cb77e890b012a4d'
    }
    conn.request("GET", "/api/client", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
#client_data()
#buy_offer()
#client_data()
#sprawdz_cene()
client_data()
for i in range(40):
    buy_offer()
    client_data()


# In[ ]:


# ### 
