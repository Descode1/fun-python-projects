import sqlite3, os
from playsound3 import playsound

conn = sqlite3.connect('music.db', isolation_level=None)

def init_db():
    conn.execute(
        'CREATE TABLE IF NOT EXISTS songs(' \
        'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
        'title TEXT,' \
        'artist Text,' \
        'album TEXT,' \
        'filepath TEXT)'
    )
    conn.execute(
        'CREATE TABLE IF NOT EXISTS playlists (' \
        'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
        'name TEXT)'   
    )
    conn.execute(
        'CREATE TABLE IF NOT EXISTS playlist_songs(' \
        'playlist_id INTEGER,' \
        'song_id INTEGER,' \
        'FOREIGN KEY (playlist_id) REFERENCES playlist(id),' \
        'FOREIGN KEY (song_id) REFERENCES songs(id))'
    )
def add_song(title, artist, album, filepath):

    conn.execute('INSERT INTO songs (title, artist, album, filepath) VALUES (?, ?, ?, ?)',
                 (title, artist, album, filepath))
    
def list_songs():
    result = conn.execute('SELECT id, title, artist FROM songs').fetchall()
    for row in result:
        print(f'[{row[0]}] {row[1]} - {row[2]}')

def play_song(song_id):
    
    result = conn.execute('SELECT filepath FROM songs WHERE id=?', (song_id,)).fetchone()
    if result:
        filepath = result[0]
        if os.path.exists(filepath):
            print(f'playing: {filepath}')
            playsound(filepath, block = False)
        else:
            print('File not found.')
   #TODO: add playlist functionality 
if __name__ == '__main__':
    init_db()
    while True:
        cmd = input("\n [music-cli] > ").strip().lower()
        if cmd == "add":
            title = input('Title: ')
            artist = input('Artist: ')
            album = input('Album: ')
            filepath = input('Path to file: ')
            add_song(title, artist, album, filepath)
        elif cmd == "list":
            list_songs()
        elif cmd.startswith('play'):
            _, song_id = cmd.split()
            sound = play_song(int(song_id))  
        elif cmd == "quit":
            break
        else:
            print('Commands: add, list, play <id>, quit')
