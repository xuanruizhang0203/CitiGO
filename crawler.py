
# coding: utf-8

# In[1]:

import pandas as pd
import urllib.request
import re
import datetime
import itertools


# In[2]:

def get_data(ur1):
    return str(urllib.request.urlopen(ur1).read())

def extract(data):
    result = data.split("underline")
    result = list(map(lambda x: x.split('</a><br/>')[0] , result))[1:]
    return result

def drop_bi(data):
    data = list(map(lambda x: re.sub('<b><i>(.*?)</i>', '<b>',x) , data))
    return data

def drop(data):
    data = list(map(lambda x: x.split('<b>')[1] , data))
    return data

def rep(s):
    a= s.replace("<IMG src=\\'images/",' ').replace('6d', '6').replace(".png\\' >",'_LINE')
    
    return re.sub('<[^>]+>', '', a)

def rep_ls(ls):
    return list(map(rep, ls))

def drop_ff(ls, string):
    return list(map(lambda x: x.replace(string, ''), ls))

def clean(url):
    data = get_data(url)
    data = extract(data)
    data = drop_bi(data)
    data = drop(data)
    data = rep_ls(data)
    data = drop_ff(data,"F&F_Pos_16 (LINE)")
    data = drop_ff(data,"&nbsp;")
    data = drop_ff(data,"\\")
    return data


# In[3]:

def get_clean_data(data):
    url = 'http://travel.mtanyct.info/serviceadvisory/routeStatusResult.aspx?tag=ALL&date='+data+'&time=&method=getstatus4'
    return clean(url)


# In[1]:

#get_clean_data('11/5/2017')


# In[5]:

def get_data_over_period(start, num_of_days):
    start_date = datetime.datetime.strptime(start, '%m/%d/20%y')
    date_list = [start_date + datetime.timedelta(days=x) for x in range(0, num_of_days)]
    dates = list(map(lambda x: x.strftime('%m/%d/20%y'), date_list))
    dataset = []
    dataset = list(map(get_clean_data, dates))
    answer = set(list(list(itertools.chain.from_iterable(dataset))))
    return answer


# In[6]:

#n = get_data_over_period('11/5/2017', 2)


# In[8]:

# text_file = open("Output.txt", "w")
# for s in n:
#     text_file.write(s+"\n")
# text_file.close()


# In[ ]:



