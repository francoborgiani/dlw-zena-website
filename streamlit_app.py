
import streamlit
import snowflake.connector
import pandas as pd

streamlit.title('Zena\'s Amazing Athleisure Catalog')

# Snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run snowflake query for getting the catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()

catalog_df = pd.DataFrame(my_catalog)

# temp write the catalog_df to the page so I can see what I'm working with
# streamlit.write(catalog_df)

# save first column into a list
color_list = catalog_df[0].values.tolist()

# picklist for the color or style
option = streamlit.selectbox('Picka sweatsuit color or style:', list(color_list))

product_caption = f"Our warm, comfortable, { option } sweatsuit!"

my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
selected_catalogs_df = my_cur.fetchone()
streamlit.image(
selected_catalogs_df[0],
width=400,
caption= product_caption
)
streamlit.write('Price: ', selected_catalogs_df[1])
streamlit.write('Sizes Available: ',selected_catalogs_df[2])
streamlit.write(selected_catalogs_df[3])