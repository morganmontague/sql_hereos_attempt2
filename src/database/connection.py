import psycopg
import math
import random
from pprint import pprint as pp
from psycopg import OperationalError

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
        connection.close()
        return cursor
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")

# ============== DONT EDIT ABOVE

def show_abilities():
    pp(execute_query("""
                SELECT  h.name, string_agg(att.name, ' ') FROM heroes h
                    JOIN abilities a ON a.hero_id = h.id
                    JOIN ability_types att ON a.ability_type_id = att.id
                    GROUP BY h.id;
            """).fetchall()
)

def ability_random():
        random_number = random.randint(1,7)
        params_ability = (random_number,)
        query_get_ability = """
            SELECT name FROM ability_types
            WHERE id = %s
            """
        result_ability = execute_query(query_get_ability, params_ability).fetchone()[0]

def restart(hero_name):
        restart_param = (hero_name,)
        restart_query = """
                        DELETE FROM heroes
                        WHERE name = %s 
                        """
        execute_query(restart_query, restart_param)




def hero_create():
    hero_name = input("What is your name? :  ")
    about = input(hero_name + " could you give me a short description of yourself? :  ")
    bio = input(hero_name + " do you have a backstory?:  ")
    reset = input("Your name is " + hero_name + ' and you describe yourself as ' + about + ". Finally you say your background is " + bio + ". If this is correct, write yes and we will add you to the list of heroes. If you want to change anything, write no and we will restart. (y/n) :  ")
    if reset == 'y':
        create_hero_params = (hero_name, about, bio)
        query_hero_create = """
                            INSERT INTO heroes (name, about_me, biography) VALUES (%s, %s, %s)
                            """
        execute_query(query_hero_create, create_hero_params)
        params_get_id = (hero_name,)
        query_get_id="""
                    SELECT id FROM heroes
                    WHERE name = %s
                    """
        result_id = execute_query(query_get_id, params_get_id).fetchone()[0]
    else: hero_create()


    confirm_id = input('Now let me guess your ability, first can you confirm your new hero is '+ str(result_id) + '.  (y/n):  ')
    if confirm_id == 'y':
        random_number = random.randint(1,7)
        params_ability = (random_number,)
        query_get_ability = """
            SELECT name FROM ability_types
            WHERE id = %s
            """
        result_ability = execute_query(query_get_ability, params_ability).fetchone()[0]
    else: 
        print('ERROR ERROR, RESTART, DELETING YOUR DATA, RESTART')
        restart(hero_name)
        hero_create()



        
    confirm_ability = input('I am now guessing your abilitiy is ' + str(result_ability)+'. (y/n):   ')
    if confirm_ability =='y':
        set_abilities_parma = (result_id, random_number)
        set_abilities_query = """
                            INSERT INTO
                            abilities (hero_id, ability_type_id)
                            VALUES
                            (%s, %s);
                            """
        execute_query(set_abilities_query, set_abilities_parma)
        pp('Here are the current heroes and their abilities')
        show_abilities()
    else: 
        print('failure, restarting')
        restart(hero_name)
        hero_create()



    friends = input("Are you ready to make a friend? (y/n):  ")
    if friends == 'y':
        length_query = """
                    SELECT COUNT(*) AS length_of_table FROM heroes
                    """
        result_length = execute_query(length_query,).fetchone()[0]
        random_friend = random.randint(1,(int(result_length)-1))
        set_friend_parma = (result_id, random_friend, 1)
        set_friend_query = """
                            INSERT INTO
                            relationships (hero1_id, hero2_id, relationship_type_id)
                            VALUES
                            (%s, %s, %s);
                            """
        execute_query(set_friend_query, set_friend_parma)
        show_friends_parma = (hero_name,)
        show_friend_query = ("""SELECT h2.name FROM relationship_types rt
                            JOIN relationships r ON rt.id = r.relationship_type_id
                            JOIN heroes h1 ON r.hero1_id = h1.id 
                            JOIN heroes h2 ON r.hero2_id = h2.id
                            WHERE h1.name = %s
                            """)
        new_friend = execute_query(show_friend_query, show_friends_parma).fetchone()[0]
        print(f"Your new friend's name is{new_friend}, you fight crime together, but one day you get into a silly fight over holes. Hope this doesn't grow too big.")
    else:
        pp(f'With no friends, {hero_name} dies of lonelyness')
        restart(hero_name)




hero_create()


# restart("test6")



# create_connection("postgres", "postgres", "postgres")

# show_abilities()

def show_friends(): 
    print(execute_query("""SELECT h1.name, rt.name, h2.name FROM relationship_types rt
                            JOIN relationships r ON rt.id = r.relationship_type_id
                            JOIN heroes h1 ON r.hero1_id = h1.id 
                            JOIN heroes h2 ON r.hero2_id = h2.id
                            ORDER BY rt.name DESC;""").fetchall())

# show_friends()


# def select_all():
#     query = """
#         SELECT * from heroes
#     """

#     list_of_heroes = execute_query(query).fetchall()
#     print(list_of_heroes)
#     for record in list_of_heroes:
#         print(record[1])

# select_all()



# def testing_area():
#     random_number = random.randint(1,7)
#     params = (random_number,)
#     query = """
#             SELECT name FROM ability_types
#             WHERE id = %s
#             """
#     result_ability = execute_query(query, params).fetchall()

