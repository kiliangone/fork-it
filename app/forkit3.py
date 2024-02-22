import streamlit as st
import pandas as pd 

#Header
st.title('Fork It')
st.image('app_assets/logo.webp')

# Load all the data 

# Example list of user IDs
# user_ids = [365441,     227130,     339672,     300249,    1284192,
#              88910,     146783,     567343,     323144,     450518,
#                  79617,      67010,      53586,     508275,     728020,
#                 954556,      28729, 2002151809,     238538,     268464,
#                1021716,    2179839,      30949,    1230396,    1222615,
#                 608030,    1486890,     392230,    2210022,     135549,
#                  93997,     851332,     607367,    1031671,      25356,
#                 290786,      87109,    1602708,    1239646,     213139,
#                 121807,     591021,     120448,      60199,     802269,
#                 336698,     815244,     767152,    1410967,    1568090,
#                 563121,     139270,     632534,    1292822,      78213,
#                 732379,     403089,     503618,     289709,     237008,
#                 295018,     943653,     797864,     763856, 2000390617,
#                 817635,     329600,     756573,     305256,     234120,
#                   7093,     792502,     165612,     328099,     241557,
#                 552864,     785604,     296809,       4036,     747477,
#                  86604,     803511,    1463003,      37502,     555701,
#                 691937,     304705,     580134,     498431,     458575,
#                 314327,       9333,     464253,    1723051, 1802579575,
#                  56447,     368823,     979991,    1914273,      71288]

user_names = ["American", "Gluten Free Fish", "Vegan Italian"]

# Creating a dropdown menu with the list of user IDs
selected_user_name = st.selectbox('Select a user ID:', user_names)

# Displaying the selected user ID
st.write(f"You're a {selected_user_name}")


st.write('Welcome to Fork It, your tool to find recipes that optimise your macros!')

# Session state callbacks
def callback_carbs():
    """The callback renormalizes the values that were not updated."""
    # Here, if we modify carbs, we calculate the remaining value for normalisation of fat, protein
    remain = 100 - st.session_state.carbs
    # This is the proportions of fat, protein in remain
    sum = st.session_state.fat + st.session_state.protein
    # This is the normalisation step
    st.session_state.fat = st.session_state.fat/sum*remain
    st.session_state.protein = st.session_state.protein/sum*remain

def callback_fat():
    remain = 100 - st.session_state.fat
    sum = st.session_state.carbs + st.session_state.protein
    st.session_state.carbs = st.session_state.carbs/sum*remain
    st.session_state.protein = st.session_state.protein/sum*remain

def callback_protein():
    remain = 100 - st.session_state.protein
    sum = st.session_state.carbs + st.session_state.fat
    st.session_state.carbs = st.session_state.carbs/sum*remain
    st.session_state.fat = st.session_state.fat/sum*remain


# Session state initialise
# Check if 'key' already exists in session_state
# If not, then initialize it
if 'carbs' not in st.session_state:
    st.session_state['carbs'] = 50

if 'fat' not in st.session_state:
    st.session_state['fat'] = 25

if 'protein' not in st.session_state:
    st.session_state['protein'] = 25

# Define a function to update the sliders based on the selected diet plan
def update_macros(plan):
    if plan == 'Keto':
        st.session_state.carbs = 5
        st.session_state.fat = 70
        st.session_state.protein = 25
    elif plan == 'Low Fat':
        st.session_state.carbs = 10
        st.session_state.fat = 75
        st.session_state.protein = 15
    elif plan == 'High Protein':
        st.session_state.carbs = 25
        st.session_state.fat = 35
        st.session_state.protein = 40
    elif plan == 'Low Carb':
        st.session_state.carbs = 20
        st.session_state.fat = 40
        st.session_state.protein = 40
    # No need to do anything for 'Custom' as it allows manual adjustment

# Define the radio buttons for diet plans
diet_plan = st.radio("Select a diet plan:", ('Custom', 'Keto', 'Low Fat', 'High Protein', 'Low Carb'))

# Define checkboxes for dietary requirements

diet_requirements = st.radio("Select your requirement:", ('Lactose Free', 'Gluten Free', 'Vegeterian', 'Vegan', 'American', 'None'))

# st.title('Dietary Requirements')

# lf = st.checkbox('Lactose Free')
# gf = st.checkbox('Gluten Free')
# v = st.checkbox('Vegeterian')
# vg = st.checkbox('Vegan')

# Function to perform text search
def search_dataframe(search_term, dataframe):
    result_df = dataframe[dataframe['Description'].str.contains(search_term, case=False)]
    return result_df

search_term = st.text_input("Search for a term:")

model = st.selectbox("Choose a model", ["NMF (general)", "NMF (specific)", "KNN (general)", "KNN (specific)"])

tolerance = st.text_input("Enter your macro tolerance", value = "0")

# Update the slider values based on the selected diet plan
if diet_plan != 'Custom':
    update_macros(diet_plan)

# The macro sliders

st.slider("% of carbs",
                min_value = 0,
                max_value = 100,
                step = 1,
                key='carbs', on_change=callback_carbs)

st.slider("% of fat",
                min_value = 0,
                max_value = 100,
                step = 1,
                key='fat', on_change=callback_fat)

st.slider("% of protein",
                min_value = 0,
                max_value = 100,
                step = 1,
                key='protein', on_change=callback_protein)

with st.form("entry_form", clear_on_submit=False):
    carbs = st.session_state.carbs
    fat = st.session_state.fat
    protein = st.session_state.protein
    submitted = st.form_submit_button(label="Submit")








# Stuff that happens after all the info is submitted 
    
# Returning all the info added

if submitted:
    st.write(f"Thanks, your macros for your meal are:")
    st.write(f"Carbs: {carbs}%              +/- {tolerance}%")
    st.write(f"Fat: {fat}                   +/- {tolerance}%")
    st.write(f"Protein: {protein}           +/- {tolerance}%")
    st.write(f"User: {selected_user_id}")
    # if lf:
    #     st.write(f"You are lactose free")
    # if gf:
    #     st.write(f"You are gluten free")
    # if v:
    #     st.write(f"You are a veggisaurus")
    # if vg:
    #     st.write(f"You are a vegan")




# Different Models

# NMF General

if model == "NMF (general)":
    # Code to execute if "NMF (general)" is selected
    st.write("You selected NMF (general).")
    def load_rankings_data():
        rankings_df = pd.read_pickle('app_data/!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!.pkl')
        return rankings_df

    def top_n_values(column, n=1000000000):
        top_n = column.nlargest(n)
        top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
        return top_values_list
    
    # Additional condition to filter the DataFrame
    if diet_requirements == "Lactose Free":
        (rankings_df['lactosefree'] == 1)
    elif diet_requirements == "Lactose Free":
        (rankings_df['glutenfree'] == 1)
    elif diet_requirements == "Lactose Free":
        (rankings_df['vegan'] == 1)
    elif diet_requirements == "Lactose Free":
        (rankings_df['vegeterian'] == 1)
    else diet_requirements == "None":
        (rankings_df)

# NMF Specific

elif model == "NMF (specific)":
    # Lactose Free
    if diet_requirements == "Lactose Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO specific model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle('app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Gluten Free  
    elif diet_requirements == "Gluten Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Gluten Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/nmf_glutenfree_glutenfreefish.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegan
    if diet_requirements == "Vegan":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/nmf_vegan_veganitalian.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegeterian
    if diet_requirements == "Vegeterian":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO specific model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle'app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list

# KNN General    

elif model == "KNN (general)":
# Lactose Free
    if diet_requirements == "Lactose Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO general model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle('app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Gluten Free  
    elif diet_requirements == "Gluten Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Gluten Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/knn_general_glutenfreefish.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegan
    if diet_requirements == "Vegan":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/knn_general_veganitalian.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegeterian
    if diet_requirements == "Vegeterian":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO general model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle'app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list

# KNN Specific 

elif model == "KNN (specific)":
# Lactose Free
    if diet_requirements == "Lactose Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO specific model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle('app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Gluten Free  
    elif diet_requirements == "Gluten Free":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Gluten Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/knn_glutenfree_glutenfreefish.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegan
    if diet_requirements == "Vegan":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free")
        def load_rankings_data():
            rankings_df = pd.read_csv('app_data/knn_vegan_veganitalian.csv')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list
    # Vegeterian
    if diet_requirements == "Vegeterian":
        (rankings_df['lactosefree'] == 1)
        st.write("You selected NMF (specific) & Lactose Free, note there is NO specific model here")
        def load_rankings_data():
            rankings_df = pd.read_pickle'app_data/sample_df.pkl')
            return rankings_df
        def top_n_values(column, n=1000000000):
            top_n = column.nlargest(n)
            top_values_list = [(idx, val) for idx, val in top_n.iteritems()]
            return top_values_list

# Outputting Results

st.header('Rankings')

# Load ranking data
rankings_df = load_rankings_data()
# Get data for selected user
row_of_interest = rankings_df.loc[selected_user_id]
# Get the top 10 values in the row
top_values = top_n_values(row_of_interest)
# Pass values to a variable 
top_recipes = [item[0] for item in top_values]

st.write(top_recipes[:10])

def load_recipe_data():
    recipes_df = pd.read_pickle('data/recipes2.pkl')
    return recipes_df



# Taking the outputted result and passing them into this to apply the filters

# Macros

st.header('Recipes')
recipes_df = load_recipe_data()
top_10_df = recipes_df[recipes_df['RecipeId'].isin(top_recipes)]
st.subheader('Top 10')
st.write(top_10_df)
filtered_df = top_10_df[
    (top_10_df['Carb%'] >= (carbs - tolerance)) & 
    (top_10_df['Carb%'] <= (carbs + tolerance)) &
    (top_10_df['Fat%'] >= (fat - tolerance)) & 
    (top_10_df['Fat%'] <= (fat + tolerance)) & 
    (top_10_df['Protein%'] >= (protein - tolerance)) & 
    (top_10_df['Protein%'] <= (protein + tolerance))
]

# Dietary Requirements

if lf:
    filtered_df = filtered_df[filtered_df['lactosefree'] == 1]
if gf:
    filtered_df = filtered_df[filtered_df['glutenfree'] == 1]
if v:
    filtered_df = filtered_df[filtered_df['vegetarian'] == 1]
if vg:
    filtered_df = filtered_df[filtered_df['vegan'] == 1]

# Search Term

# Check if the search term is not empty
if search_term:
    # Use the search_dataframe function to filter the DataFrame
    df_search_result = search_dataframe(search_term, df)
    
    # Display the search result
    st.write(f'Search Results for "{search_term}":')
    st.write(df_search_result)
else:
    st.write('Enter a search term to filter the DataFrame.')











# checks we can enable to check results match dataframe

# st.write(recipes_df.dtypes)
# st.write(filtered_df)
# st.write(recipes_df.head())













# Returning results with custom formatting

recipe_number = 1
recipes_printed = 0

if filtered_df.empty:
    st.write("No Recipes")
else:
    for index, row in filtered_df.iterrows():
        if recipes_printed >= 10:
            break  # Exit the loop if 10 recipes have been printed
        
        st.title(f"Recipe {recipe_number}: {row['Name']}")
        st.write(f"https://www.food.com/{row['Name'].replace(' ', '-').lower()}-{row['RecipeId']}")
        st.write(f"- Carbs: {round(row['Carb%'])}%")
        st.write(f"- Fat: {round(row['Fat%'])}%")
        st.write(f"- Protein: {round(row['Protein%'])}%")

            # Add this line to display the RecipeCategory
        st.write(f"- Category: {row['RecipeCategory']}")

        # Extract URLs from the string using regular expressions
        image_urls = re.findall(r'https?://\S+', row['Images'])
        
        # Check if there are any URLs extracted
        if image_urls:
            # Display the first image URL
            st.image(image_urls[0].rstrip('",'), caption=f"{row['Name']}")
        else:
            # Display a message if no valid image URL was found
            st.image('assets/ph.png')
        
        # Increment counters
        recipe_number += 1
        recipes_printed += 1


# to add