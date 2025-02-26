# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw: ")
st.write(
    f"""Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
# st.write

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections=5
)

if ingredient_list :
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredients_string=''
    for fruit_chosen in ingredient_list :
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    time_to_insert = st.button('Submit order')
    st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
# New section to display smoothifroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
