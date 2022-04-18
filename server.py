'''Flask Server for project'''

from flask import Flask, render_template, request, redirect, session, flash
import jinja2
import os

import crud
import model

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

##spotipy finds the credentials in the environment and sets it to auth_manager
##for searching and ClientCredentials flow
authorization = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=authorization)
url = 'https://api.spotify.com/v1/search?'
app_id = os.environ['APP_ID']

scope = 'playlist-modify-public'
spot2 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

app = Flask(__name__)
model.connect_to_db(app)

app.secret_key = os.environ['SECRET_KEY']


# results = spot.search(q='',type='track',limit=50)
'''relevant info is results['tracks']['items']
will result in a list full of libraries

songs = results['tracks']['items']
will want song['name'] for checks
and song['uri'] for further fetching
song['artists'][0]['name'] to get primary artist name'''

# tracks = spot.playlist_tracks(playlist_id)
# new = spot2.user_playlist_create(app_id, 'test')
'''new playlist redirects to a new page, set it specifically
play more with the redirect and authorization, it's confusing'''


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/log_in', methods=['POST'])
def sign_in():
    '''logs the user in or redirects'''

    ##gets email and password from from
    in_email = request.form.get('email')
    in_pass = request.form.get('password')

    ##log in checks database information
    user = crud.log_in(in_email, in_pass)

    if user == True:
        session['login'] = True
        return redirect('/my_playlists')
    if user == False:
        flash('Wrong password and/or email')
        return redirect('/join')

@app.route('/join_up', methods=['POST'])
def sign_up():
    '''checks user email and creates an account'''

    in_email = request.form.get('email')
    in_pass = request.form.get('password')
    in_name = request.form.get('name')

    check = crud.create_account(in_email, in_pass, in_name)

    if check == True:
        session['login'] = True
        return redirect('/my_playlists')
    else: 
        flash('Email taken')
        return redirect('/join')

@app.route('/logout')
def logout():
    '''logs a user out'''
    session['login'] = False

    return redirect('/')        



@app.route('/my_playlists')
def show_user_playlists():
    return render_template('my_playlists.html')



@app.route('/new_playlist')
def new_playlist():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('new_playlist.html')

@app.route('/make', methods=['POST'])
def make_playlsit():
    '''search through the database to fill out the playlist'''

    name = request.form.get('new')
    
    tracks = crud.make_playlist(name)

    return redirect('/new_playlist')


@app.route('/search')
def search():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('search.html')


@app.route('/join')
def show_sign_in():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('join.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
