import psycopg2
import re
import unicodedata


def format_string(input_string):
    input_string = input_string.lower().replace(" ", "")
    input_string = unicodedata.normalize('NFD', input_string)
    input_string = input_string.encode('ascii', 'ignore')
    input_string = input_string.decode("utf-8")
    input_string = re.sub('[^a-zA-Z0-9]', '', input_string)

    return str(input_string)


con = psycopg2.connect(
    host='',
    database='',
    user='',
    password=''
)


def main_function():
    required_lenght = False

    while not required_lenght:
        choice = input(
            '\nDo you want to know if a Movie is in the IMDb Top 250 Movies? Or maybe if an actor/director played/directed in one of these movies?\nEnter the title/name you\'re searching: ')
        choice = format_string(choice)
        if len(choice) <= 3:
            print('\nPlease enter at least 4 valid characters. Try again.\n')
        else:
            required_lenght = True

    cur = con.cursor()
    cur.execute('SELECT * FROM movies')
    rows = cur.fetchall()

    i = 1
    movie_results = ""
    print("\nMovies: ")

    for r in rows:
        if format_string(r[0]).find(choice) != -1:
            movie_results = movie_results + \
                "\n Title: "+r[0]+" | Rank: "+str(i)+"\n"
        i = i+1
    if movie_results == "":
        movie_results = "no movie with this title in the Top 250\n"
    print(movie_results)
    cur.close()

    cur = con.cursor()
    cur.execute('SELECT * FROM actors')
    rows = cur.fetchall()

    actor_results = ""
    print("Actors: ")

    for r in rows:
        if format_string(r[0]).find(choice) != -1:
            actor_results = actor_results + "Name: " + \
                r[0]+" | Played in "+str(r[2])+" movie(s).\n"
    if actor_results == "":
        actor_results = "no actor with this name in the Top 250\n"
    print(actor_results)
    cur.close()

    cur = con.cursor()
    cur.execute('SELECT * FROM directors')
    rows = cur.fetchall()

    director_results = ""
    print("Directors: ")

    for r in rows:
        if format_string(r[0]).find(choice) != -1:
            director_results = director_results + "Name: " + \
                r[0]+" | Directed "+str(r[2])+" movie(s).\n"
    if director_results == "":
        director_results = "no director with this name in the Top 250\n"
    print(director_results)

    print("IMPORTANT: Please note that we\'re only taking into account the 10 main actors for each movie.\n")
    cur.close()


main_function()

last_question = True

while last_question:
    answer = input('Do you want to continue (y/n): ').lower().strip()
    if answer == 'y' or answer == 'yes':
        main_function()
    elif answer == 'n' or answer == 'no':
        last_question = False
    else:
        print("\nPlease just anwer yes or no.\n")


con.close()
