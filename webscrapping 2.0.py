import requests
from bs4 import BeautifulSoup
import sqlite3

# entering website url
url = ("https://www.worldometers.info/gdp/nepal-gdp/#:~:text=Nominal%20(current)%20Gross%20Domestic%20Product,"
       "when%20Real%20GDP%20was%20%2431%2C325%2C711%2C843.")

# getting response
response = requests.get(url)

# html parsing using beautiful soup
soup = BeautifulSoup(response.content, 'html.parser')

# finding required fields
rows = soup.find_all('tr')
# print(rows)

data = []
for row in rows:
    cols = row.find_all(['td'])
    cols = [col.text.strip() for col in cols]  # list comprehension
    data.append(cols)
del data[:3]  # removing first 3 lists within the list as it is not required
# print(data)


# connect to db or create if it does not exist
conn = sqlite3.connect('Nepal.db')

# create cursor object to execute SQL queries as it is not python language
cursor = conn.cursor()

# create a table with names of column
cursor.execute('''CREATE TABLE IF NOT EXISTS Nepal_DATA (Year INTEGER, GDP_Nominal INTEGER, GDP_REAL INTEGER, 
change INTEGER, GDP_per_capita INTEGER, Pop_Change INTEGER, Population INTEGER)''')

# insert data into table columns
try:
    for sublist in data:
        cursor.execute('''INSERT INTO Nepal_DATA(Year, GDP_Nominal, GDP_REAL, change, GDP_per_capita, 
        Pop_Change, Population) VALUES(?,?,?,?,?,?,?)''', sublist)

    conn.commit()
    print("Data successfully entered.")

except sqlite3.Error as e:
    print("ERROR", e)
    conn.rollback()  # rollback the changes if there is an error

# close database connection
conn.close()

