import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Receives data file containing the song metadata and loads into songs and artists tables.

    Keyword arguments:
    cur -- the connected cursor
    filepath -- the file name and directory
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()
    artist_data = [item for sublist in artist_data for item in sublist]  # add to flatten the list
    cur.execute(song_table_insert, song_data)  # insert artist record
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Receives a data file containing the logs from user activity and loads into time, users and songplays tables.

    Keyword arguments:
    cur -- the connected cursor
    filepath -- the file name and directory
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df.copy()  # deep copy of df
    t['ts'] = pd.to_datetime(t['ts'], unit='ms')

    # insert time data records
    time_data = [df['ts'], t['ts'].dt.hour, t['ts'].dt.day, t['ts'].dt.weekofyear, t['ts'].dt.month, t['ts'].dt.year,
                 t['ts'].dt.weekday]
    column_labels = ['ts', 'hour', 'day', 'week of year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame.from_dict(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
        int(row.ts // 1000), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Get all the source files contained in the filepath and execute process_song_file or process_log_file.

    Keyword arguments:
    cur -- the connected cursor
    conn -- connection string to Postgres server
    filepath -- the file directory
    func -- function that will read and insert records to the tables
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """This program will read all files from song and log directories and properly load them into fact and dimesions tables.
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()