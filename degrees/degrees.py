# Imports to be used
import csv
import sys

from util import Node, nodeQueue

# objects to be used for mapping 

names = {} # will corespond to person_ids

people = {} # will correspond to a dict of: name, dob, set of movie ids

movies = {} # will correspond to a dict of: title, year, starts (set of person ids)

# load the data
def load_data():

    # first load the people
    with open(f"imdb/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name":row["name"],
                "birth":row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # load the movies
    with open(f"imdb/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row['title'],
                "year": row['year'],
                "stars": set()
            }

    # load stars
    with open(f"imdb/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    # get command arguments
    if len(sys.argv) > 1:
        sys.exit("Usage: python degrees.py")

    # Load data from files into memory
    print("Loading data...")
    load_data()
    print("Data loaded.")
    imdb()

def imdb():
        # get the user inputs
        source = name1()
        target = name2(source)
        
        # find the shortest path
        path = shortest_path(source, target)

        if path is None:
            print("Not connected. Would you like to try again?")
            tryAgain()
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")
        print("Would you like to try again?")
        tryAgain()

def name1():
        # get input for first name, if empty or not in list, try again
        source = person_id_for_name(input("Name 1: "))
        if source is None:
            print("Person not found, Try again.")
            name1()

        return source

def name2(source):
        # get input for second name, if empty or not in list, try again
        target = person_id_for_name(input("Name 2: "))
        if target is None:
            print("Person not found, Try again.")
            name2(source)

        # If the source actor is same as target actor try again
        if source == target:
            print("Can't use the same actor twice.")
            name2(source)
        
        return target

def tryAgain():
    try_again = input("Y or N: ")
    try_again.lower()

    if try_again == "y" or try_again == "yes":
        imdb()
    else:
        sys.exit("Thank you, Goodbye!")
    

def shortest_path(source, target):
    
    # first set the data structure to use
    horizon = nodeQueue()

    # add a node to the horizon, 
    # the first node will be the initial person, with no parenr node & no action
    horizon.add(Node(source, None, None))

    # initialise an empty set for nodes explored
    nodesExplored = set()

    # loop until solution found
    while True:

        # first check if horizon empty
        if horizon.isEmpty():
            return None
        
        # take a node from the horizon
        node = horizon.remove()

        # If the removed node is the target 
        if node.state == target:
            # Then add it to the solutions array
            solution = []
            # While the parent node is not none
            while node.parent is not None:
                # Add to the solutions, the action taken and the node state (actor)
                solution.append((node.action, node.state))
                # the node now becomes the new parent node
                node = node.parent
            # Reverse the solution array 
            solution.reverse()
            # Return the solution
            return solution

        # If the node is not the target then add it to the nodes explored 
        nodesExplored.add(node.state)

        # for the movies and actors in the possible neighbors 
        for movie_id, person_id in neighbors_for_person(node.state):
            # If the neighbor is not already in the nodes explored
            if not (person_id in nodesExplored):
                # create the child node with the person, the node info and the movie info
                child = Node(person_id, node, movie_id)
                # add the child to the frontier
                horizon.add(child)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
