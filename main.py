import sqlite3

# Step 1: Read the file and copy content to a list
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# Step 2: Establish a connection with SQLite database
connection = sqlite3.connect('stephen_king_adaptations.db')
cursor = connection.cursor()

# Step 3: Create a table in the database
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL
                )''')

# Step 4: Insert data into the table
for line in stephen_king_adaptations_list:
    movie_data = line.strip().split(',')
    cursor.execute('''INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
                      VALUES (?, ?, ?)''', (movie_data[1], int(movie_data[2]), float(movie_data[3])))

# Step 5: Loop for user interaction
while True:
    print("Options:")
    print("1. Search by Movie Name")
    print("2. Search by Movie Year")
    print("3. Search by Movie Rating")
    print("4. STOP")
    choice = input("Enter your choice: ")

    if choice == '1':
        movie_name = input("Enter the movie name: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?''', (movie_name,))
        result = cursor.fetchone()
        if result:
            print(f"Movie Name: {result[1]}, Year: {result[2]}, Rating: {result[3]}")
        else:
            print("No such movie exists in our database")
    elif choice == '2':
        movie_year = input("Enter the movie year: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?''', (int(movie_year),))
        results = cursor.fetchall()
        if results:
            for result in results:
                print(f"Name: {result[1]}, Year: {result[2]}, Rating: {result[3]}")
        else:
            print("No movies were found for that year in our database.")
    elif choice == '3':
        rating = input("Enter the minimum rating: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?''', (float(rating),))
        results = cursor.fetchall()
        if results:
            for result in results:
                print(f"Name: {result[1]}, Year: {result[2]}, Rating: {result[3]}")
        else:
            print("No movies were found in the database.")
    elif choice == '4':
        break

# Step 6: Commit changes and close the database
connection.commit()
connection.close()