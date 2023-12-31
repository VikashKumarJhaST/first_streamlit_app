import streamlit
import pandas
import requests
import snowflake.connector

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

 # Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show )

#display fruitvice api
streamlit.header("fruityvice fruit advice");
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
 
# normalize the data 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# display normal data(in tables)
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("the fruit load list contain")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)
my_cur.execute("INSERT INTO fruit_load_list VALUES ('"+fruit_choice+"')")
