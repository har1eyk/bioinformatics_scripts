import sqlite3
import time
from Bio import SeqIO

try:
    conn = sqlite3.connect('/home/harley/Documents/16s_primers')
    cursor = conn.cursor()
    print ("connected to sqlite3")
except sqlite3.Error as error:
    print ("Failed to connect to sqlite")

#create table in db
tableName = 'first_primer_set'
create_table = '''CREATE TABLE IF NOT EXISTS {}
(seq_number INTEGER PRIMARY KEY AUTOINCREMENT,
seq_id text,
seq_description text,
seq_sequence text);'''.format(tableName)

cursor.execute(create_table)

#parse fasta file
filename = 'arb-silva.de_2022-05-16_id1164063.fasta'
with open("/home/harley/Downloads/Sequence_data_from_Greg/"+filename) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        # print(record.id)
        # print(record.seq)
        # print(record.description)
        # print (record)
        insert_values = (str(record.id), str(record.description), str(record.seq))
        insert_query = '''INSERT INTO {}
        (seq_id, seq_description, seq_sequence)
        VALUES (?, ?, ?)'''.format(tableName)
        try:
            cursor.execute(insert_query, insert_values)
        except sqlite3.Error as insertError:
            print ("Failed to insert record", record.id, insertError)

#close connections
conn.commit()
conn.close()
            