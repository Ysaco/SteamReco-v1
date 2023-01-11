from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
from datetime import date
from PIL import Image
import webbrowser

#game_list = pd.read_excel('Webscraping_1.csv')
game_list = pd.read_excel(r'C:\Users\isaac\IH\Proyecto\SteamReco_test\streamlit-example\19618_6.xlsx')


st.markdown("""
<style>
.title-font {
    font-size:25px !important;}

.header-font {
    font-size:25px !important;

}
</style>
""", unsafe_allow_html=True)

img = Image.open(r"C:\Users\isaac\IH\Proyecto\SteamReco_test\streamlit-example\Logo3.png")
st.image(img)
st.title('Welcome to SteamReco!')


st.markdown('<p class="header-font">SteamReco is a game recommendation system based of steam games for our fellow gamers! <span> &#127918; </span></p>', unsafe_allow_html=True)

st.markdown('<p class="header-font">This app uses a database based on a webscraping on the steam webpage, it does not use SteamKit or any external tool, just BeautifulSoup and a bit of patience</p>', unsafe_allow_html=True)

st.markdown('<p class="header-font">For more info, insight, or further development on this web app, feel free to contact me at ysaco7@gmail.com</p>', unsafe_allow_html=True)

st.text('')



vectorizer_train = TfidfVectorizer(analyzer = 'word', min_df=0.0, max_df = 1.0, strip_accents = None,
                                       encoding = 'utf-8', preprocessor=None)
vector_matrix = vectorizer_train.fit_transform(game_list['genre'])

cos_matrix = linear_kernel(vector_matrix,vector_matrix)

def get_title_from_index(index):
    return game_list[game_list.index == index]['title'].values[0]

def get_index_from_title(title):
    return game_list[game_list.title == title].index.values[0]

def get_picture_from_index(index):
    return game_list[game_list.index == index]['photo'].values[0]

def get_description_from_index(index):
    return game_list[game_list.index == index]['description'].values[0]

def get_link_from_index(index):
    try:
        return game_list[game_list.index == index]['link'].values[0]
    except:
        pass

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def matching_score(a,b):
    return fuzz.ratio(a,b)

def find_closest_title(title):
    leven_scores = list(enumerate(game_list['title'].apply(matching_score, b=title)))
    sorted_leven_scores = sorted(leven_scores, key=lambda x: x[1], reverse=True)
    closest_title = get_title_from_index(sorted_leven_scores[0][0])
    distance_score = sorted_leven_scores[0][1]
    
    return closest_title, distance_score


def contents_recommender(insert_game, quantity):
    
    closest_title, distance_score = find_closest_title(insert_game)

    if distance_score == 100:
        
        name = []
        namewth_id = []
        photo = []
        description = []
        url = []
        game_index = get_index_from_title(closest_title)
        game_list = list(enumerate(cos_matrix[int(game_index)]))
        similar_games = list(filter(lambda x:x[0] != int(game_index), sorted(game_list,key=lambda x:x[1], reverse=True)))


        for i in similar_games[:quantity]:
            namewth_id.append(str(get_title_from_index(i[0]))+' '+str(math.trunc(i[1]*100))+'%')
            name.append(str(get_title_from_index(i[0])))
            photo.append(str(get_picture_from_index(i[0])))
            description.append(str(get_description_from_index(i[0])))
            url.append(str(get_link_from_index(i[0])))
    
        return namewth_id, photo, name, description, url

    else:


        name = []
        namewth_id = []
        photo = []
        description = []
        url = []
        game_index = get_index_from_title(closest_title)
        game_list = list(enumerate(cos_matrix[int(game_index)]))
        similar_games = list(filter(lambda x:x[0] != int(game_index), sorted(game_list,key=lambda x:x[1], reverse=True)))


        for i in similar_games[:quantity]:
            namewth_id.append(str(get_title_from_index(i[0]))+' '+str(math.trunc(i[1]*100))+'%')
            name.append(str(get_title_from_index(i[0])))
            photo.append(str(get_picture_from_index(i[0])))
            description.append(str(get_description_from_index(i[0])))
            url.append(str(get_link_from_index(i[0])))
    
        return namewth_id, photo, name, description, url







col1, col2 = st.columns([1, 3])
with col1:     
    insert_game = st.text_input("", placeholder =("Insert a game you like"))

quantity = st.slider("Quantity of games you would like to see", 10, 1000, 100)


closest_title, distance_score = find_closest_title(insert_game)
namewth_id, photo, name, description, url = contents_recommender(insert_game, quantity)
mygrid = make_grid(len(namewth_id)+1, 4)   


if distance_score == 100:
    with st.container():
        mygrid[0][0].text(str('List of games similar to '+str(closest_title)+':'))
        mygrid[0][0].text(' ')

    for i in range(len(namewth_id)):
            mygrid[i+1][0].text(namewth_id[i])
            mygrid[i+1][0].image(photo[i])

            mygrid[i+1][1].write('#')
            if  mygrid[i+1][1].button('More info on '+str(name[i])):
                webbrowser.open_new_tab(url[i])
            mygrid[i+1][1].write(description[i])

else:
    with st.container():
        mygrid[0][0].text(str('Did you mean '+str(closest_title)+'?'))
        mygrid[0][0].text(str('List of games similar to '+str(closest_title)+':'))
        mygrid[0][0].text(' ')

    for i in range(len(namewth_id)):
        with st.container():
                mygrid[i+1][0].text(namewth_id[i])
                mygrid[i+1][0].image(photo[i])

                mygrid[i+1][1].write('#')
                if  mygrid[i+1][1].button('More info on '+str(name[i])):
                    webbrowser.open_new_tab(url[i])
                mygrid[i+1][1].write(description[i])

st.subheader('Go back to the top', anchor ='welcome-to-steamreco')