from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Song, Playlist  # Assuming Song and Playlist models exist
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')  # Gets the note from the HTML 

        if not note or len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Providing the schema for the note 
            db.session.add(new_note)  # Adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)  # This function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/add-song', methods=['POST'])
@login_required
def add_song():
    song_data = request.form.get('song')  # Get song data from the form
    if len(song_data) < 1:
        flash('Song data is too short!', category='error')
    else:
        new_song = Song(data=song_data, user_id=current_user.id)  # Assuming Song model has a 'data' field
        db.session.add(new_song)
        db.session.commit()
        flash('Song added!', category='success')
    return render_template("songs.html", user=current_user)


@views.route('/delete-song', methods=['POST'])
@login_required
def delete_song():
    song = json.loads(request.data)  # Expecting JSON data from the frontend
    songId = song['songId']
    song = Song.query.get(songId)
    if song:
        if song.user_id == current_user.id:
            db.session.delete(song)
            db.session.commit()
    return jsonify({})


@views.route('/create-playlist', methods=['POST'])
@login_required
def create_playlist():
    playlist_name = request.form.get('playlist_name')  # Get playlist name from the form
    if len(playlist_name) < 1:
        flash('Playlist name is too short!', category='error')
    else:
        new_playlist = Playlist(name=playlist_name, user_id=current_user.id)  # Assuming Playlist model has a 'name' field
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist created!', category='success')
    return render_template("playlists.html", user=current_user)


@views.route('/add-song-to-playlist', methods=['POST'])
@login_required
def add_song_to_playlist():
    data = json.loads(request.data)  # Expecting JSON data from the frontend
    song_id = data['songId']
    playlist_id = data['playlistId']
    playlist = Playlist.query.get(playlist_id)
    song = Song.query.get(song_id)
    if playlist and song:
        if playlist.user_id == current_user.id:
            playlist.songs.append(song)  # Assuming a many-to-many relationship
            db.session.commit()
            flash('Song added to playlist!', category='success')
    return jsonify({})


@views.route('/delete-playlist', methods=['POST'])
@login_required
def delete_playlist():
    playlist = json.loads(request.data)  # Expecting JSON data from the frontend
    playlistId = playlist['playlistId']
    playlist = Playlist.query.get(playlistId)
    if playlist:
        if playlist.user_id == current_user.id:
            db.session.delete(playlist)
            db.session.commit()
    return jsonify({})
