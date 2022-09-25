#!/usr/bin/env python
# coding: utf-8

# ### Import packages

# In[1]:


import pandas as pd 


# In[2]:


import requests


# In[3]:


from bs4 import BeautifulSoup


# ### HTTP request

# In[4]:


website="https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=New%20York%2C%20NY&=&s=default"


# In[5]:


response= requests.get(website)


# In[6]:


response.status_code


# ### Soup object

# In[7]:


soup= BeautifulSoup(response.content, "html.parser")


# ### Scrape website

# Name, description, number, address, number of years in the market

# In[8]:


results=soup.findAll("div",{"class":"result"})


# In[9]:


Restaurants_name=[i.find("a",{"class":"business-name"}).text for i in results]


# In[10]:


Restaurants_number=[i.find("div",{"class":"phones phone primary"}).text for i in results]


# In[11]:


Restaurants_street=[i.find("div",{"class":"street-address"}).text for i in results]


# In[12]:


Restaurants_number=[i.find("div",{"class":"number"}) for i in results]


# ### URL part one 

# In[13]:


#we combine url part one with url part two in order to have the absolute url specific to each restaurant details
URL_PartOne="https://www.yellowpages.com"


# ### Creat list URL part two

# In[14]:


URL_PartTwo=[i.find("a",{"class":"business-name"})["href"] for i in results]


# ### Create absolute URL respective to each restaurant

# In[15]:


URL=[URL_PartOne+i for i in URL_PartTwo]


# ### Scrap the data you need from the first link

# In[16]:


first_link=URL[1]


# ### HTTP request and soup object

# In[17]:


response_FirstLink= requests.get(first_link)


# In[18]:


soup= BeautifulSoup(response_FirstLink.content,"html.parser")


# ### Get the Name, Address, Phone, Email, Website link

# In[19]:


Name=soup.find("div", {"class":"sales-info"}).find("h1").getText().replace("\ufeffAdd to Favorites","")


# In[20]:


Address=soup.find("span", {"class":"address"}).find("span").text


# In[21]:


Phone=soup.find("a", {"class":"phone"})["href"].replace("tel:","")


# In[22]:


# Email=soup.find("a", {"class":"email-business"})["href"].replace("mailto:","")


# In[23]:


# Restaurant_Website=soup.find("a", {"class":"website-link"}).get("href")


# In[24]:


# Restaurant_Website


# ### Create a dataframe for the first link

# In[25]:


YellowPages_Scraping_df= pd.DataFrame(columns=["Name", "Address", "Phone", "Email", "Restaurant_Website"])


# In[26]:


for j in range(1,2):
    
    #Iterate over the main page. 
    URL_MainPage="https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=New%20York%2C%20NY&page="+str(j)
    #HTTP request main page.
    response_MainPage=requests.get(URL_MainPage)
    #Soup object main page.
    soup_MainPage= BeautifulSoup(response_MainPage.content,"html.parser")
    #Create the iterable bs4 object of the main page.
    Container_MainPage=soup_MainPage.findAll("div",{"class":"result"})
    #Create the first part URL to which the second part URL will be concatenated.
    URL_PartOne="https://www.yellowpages.com"
    #Find the second URL part in the main page. 
    URL_PartTwo=[k.find("a",{"class":"business-name"})["href"] for k in Container_MainPage]
    #Concatenate to create the Absolute URL list.
    URL=[URL_PartOne+b for b in URL_PartTwo]
    #Iterate over the detail pages of the main page j.
    
    
    for i in range (len(URL)):
        
        URL_DetailPage= URL[i]
        #HTTP request detail page.
        response_DetailPage= requests.get(URL_DetailPage)
        #Soup object detail page.
        soup_DetailPage= BeautifulSoup(response_DetailPage.content,"html.parser")
        #Get the needed values
        try:
            Name=soup_DetailPage.find("div", {"class":"sales-info"}).find("h1").getText().replace("\ufeffAdd to Favorites","")
        except:
            Namee="N/A"
        
        try:
            Name=soup_DetailPage.find("div", {"class":"sales-info"}).find("h1").getText().replace("\ufeffAdd to Favorites","")
        except:
            Name="N/A"  
            
        try:
            Address=soup_DetailPage.find("span", {"class":"address"}).find("span").text
        except:
            Address="N/A"  
            
        try:
            Phone=soup_DetailPage.find("a", {"class":"phone"})["href"].replace("tel:","")
        except:
            Phone="N/A"
            
        try:
            Email=soup_DetailPage.find("a", {"class":"email-business"})["href"].replace("mailto:","")
        except:
            Email="N/A"

        try:
            Restaurant_Website=soup_DetailPage.find("a", {"class":"website-link"}).get("href")
        except:
            Restaurant_Website="N/A"
        print(i)
        #Append the dataframe with the results
        YellowPages_Scraping_df=YellowPages_Scraping_df.append({"Name":Name, "Address":Address,
                                      "Phone":Phone, "Email":Email, "Restaurant_Website":Restaurant_Website}, ignore_index=True)
YellowPages_Scraping_df


# In[28]:


YellowPages_Scraping_df


# ### Create an excel file out of the output and save it in a folder on your mac

# In[27]:


YellowPages_Scraping_df.to_excel("/Users/AA/Desktop/Coding /Python projects/Udemy web scraping project 1/Books_table.xlsx", index=False)

