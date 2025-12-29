import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# App title - corrected from 'streamlit.title' to 'st.title'
st.title("My Parents New Healthy Diner")

st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on smoothie:")

if name_on_order:
    st.write("The name on your smoothie will be:", name_on_order)

    # Snowflake connection
    cnx = st.connection("snowflake")
    session = cnx.session()

    # Load fruit options
    my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

    # Convert dataframe to list for the multiselect
    # This ensures the multiselect can iterate through the data correctly
    fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

    st.header("🍓 Build Your Smoothie")

    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        fruit_list,
        max_selections=5
    )

    if ingredients_list:
        # Join the list into a single string separated by spaces
        ingredients_string = " ".join(ingredients_list)

        # Build the SQL Insert Statement
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        if st.button("Submit Order"):
            session.sql(my_insert_stmt).collect()
            st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
