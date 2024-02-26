import streamlit as st
import pandas as pd 
import re

#Header
st.image('app_assets/logo.jpg')
st.title('Fork It')
st.write('Welcome to Fork It, your tool to find recipes that optimise your macros!')

# Entering all your data

# Enter User ID
user_id = st.selectbox("Enter User ID:", ["1536", "10700", "29600", "13063", "35526", "3288"])

# Lots of slider stuff
# This sets the sliders and makes sure they add up to 100
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
# End of slider thing

# Define checkboxes for dietary requirements

st.title('Dietary Requirements')

lf = st.checkbox('Lactose Free')
gf = st.checkbox('Gluten Free')
v = st.checkbox('Vegeterian')
vg = st.checkbox('Vegan')

# Function to perform text search
def search_dataframe(search_term, dataframe):
    result_df = dataframe[dataframe['Keywords'].str.contains(search_term, case=False)]
    return result_df

search_term = st.text_input("Search for an ingredient:")

model = st.selectbox("Choose a model", ["KNN (general)", "KNN (specific)"])

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
    st.write(f"User: {user_id}")


# Functions defined

def load_rankings_data(file_path):
    rankings_df = pd.read_csv(file_path)
    return rankings_df

def top_n_values(column, n=1000000000):
    top_n = column.nlargest(n)
    top_values_list = [(idx, val) for idx, val in top_n.items()]
    return top_values_list


if model == "KNN (general)" and user_id == '1536':
    st.write("You selected a KNN general for a new user with no dietary requirements")
    top_values_list = pd.read_csv('app_data/knn_general_american.csv')
# general, vegan, new user
elif model == "KNN (general)" and user_id == '10700':
    st.write("You selected a KNN general for a new user with  vegan requirements")
    top_values_list = pd.read_csv('app_data/knn_general_veganitalian.csv')
# general, glutenfree, new user
elif model == "KNN (general)" and user_id == '29600':
    st.write("You selected a KNN general for a new user with gluten free requirements")
    top_values_list = pd.read_csv('app_data/knn_general_glutenfreefish.csv')
# general, no requirements, existing user
elif model == "KNN (general)" and user_id == '13063':
    st.write("You selected a KNN general for an existing user with no dietary requirements")
    top_values_list = pd.read_csv('app_data/knn_general_exist1.csv')
# general, no requirements, existing user
elif model == "KNN (general)" and user_id == '35526':
    st.write("You selected a KNN general for an existing user with no dietary requirements")
    top_values_list = pd.read_csv('app_data/knn_general_exist2.csv')
# general, vegan, existing user
elif model == "KNN (general)" and user_id == '3288':
    st.write("You selected a KNN general for an existing user with vegan requirements")
    top_values_list = pd.read_csv('app_data/knn_general_exist3.csv')
# specific, no requirements, existing user
elif model == "KNN (specific)" and user_id == '10700':
    st.write("You selected a KNN specific for a new user with vegan requirements")
    top_values_list = pd.read_csv('app_data/knn_vegan_veganitalian.csv')
# specific, no requirements, existing user
elif model == "KNN (specific)" and user_id == '29600':
    st.write("You selected a KNN specific for a new user with gluten free requirements")
    top_values_list = pd.read_csv('app_data/knn_glutenfree_glutenfreefish.csv')
# specific, vegan, existing user
elif model == "KNN (specific)" and user_id == '3288':
    st.write("You selected a KNN specific for an exisiting user with vegan requirements")
    top_values_list = pd.read_csv('app_data/knn_vegan_exist3.csv')
else:
    st.write("You've picked a combo that don't work")

if model == "KNN (general)":
    if lf:
        top_values_list = top_values_list[top_values_list['lactosefree'] == 1]
    if gf:
        top_values_list = top_values_list[top_values_list['glutenfree'] == 1]
    if v:
        top_values_list = top_values_list[top_values_list['vegetarian'] == 1]
    if vg:
        top_values_list = top_values_list[top_values_list['vegan'] == 1]
else:
    pass


# This loads all the lovely recipe data

def load_recipe_data():
    recipes_df = pd.read_pickle('recipe_slim_clean.pkl')
    return recipes_df

recipes_df = load_recipe_data()



# Merge top_values_list with recipes_df based on the 'RecipeId' column
merged_df = pd.merge(top_values_list, recipes_df, on='RecipeId')

# Convert relevant columns to numeric types individually
tolerance = float(tolerance)  # Assuming 'tolerance' is entered as a string


filtered_df = merged_df[
    (merged_df['Carb%'] >= (carbs - tolerance)) & 
    (merged_df['Carb%'] <= (carbs + tolerance)) &
    (merged_df['Fat%'] >= (fat - tolerance)) & 
    (merged_df['Fat%'] <= (fat + tolerance)) & 
    (merged_df['Protein%'] >= (protein - tolerance)) & 
    (merged_df['Protein%'] <= (protein + tolerance))
    ]

st.header('Recipes')
st.subheader('Top 10')
#st.write(filtered_df)


# Search Term

if search_term:
    # Do something with the search term, for example, print it
    merged_df.query('Keywords == @search_term')
else:
    # if no search term, does nothing
    pass


# Check if the search term is not empty
if search_term:
    # Use the search_dataframe function to filter the DataFrame
    df_search_result = search_dataframe(search_term, merged_df)
    
    # Display the search result
    st.write(f'Search Results for "{search_term}":')
    st.write(df_search_result)
else:
    pass


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
            st.image('app_assets/ph.webp')
        
        # Increment counters
        recipe_number += 1
        recipes_printed += 1