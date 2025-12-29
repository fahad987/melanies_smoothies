# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# App Title
st.title("My Parents New Healthy Diner")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on Order
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be: ', name_on_order)

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get Fruit Options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'),col('SEARCH_ON'))
# st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# st.stop()

pd_df =my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

# Build the Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Logic when ingredients are selected
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        # Display nutrition info for each fruit
        st.subheader(fruit_chosen + ' Nutrition Information')
        try:
            # API Call using the fruit name
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}" + fruit_chosen)
            if smoothiefroot_response.status_code == 200:
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.warning(f"No nutrition data found for {fruit_chosen}")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

    # Build the SQL Insert Statement
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
