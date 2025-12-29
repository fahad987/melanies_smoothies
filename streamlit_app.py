# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title("My Parents New Healthy Diner")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be: ',name_on_order)

#title = st.text_input('Move Title', 'Life Of Brain')
#st.write('The Current movie title is ', title)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

st.header("🍓 Build Your Smoothie")

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    # Ensure this line aligns perfectly with the 'for' loop above
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
        
   # if ingredients_string:
    #    session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!')
