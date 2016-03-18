from dataservice import retrieve_movie_info
from dataservice import retrieve_user_review_history
from dataservice import update_user_recommend
import operator
import math
import time

class Helper(object):
    @classmethod
    def cosine_similarity(cls, movie_list1, movie_list2):
        return float(cls.__count_match(movie_list1, movie_list2)) / math.sqrt( len(movie_list1) * len(movie_list2) )
    
    @classmethod
    def __count_match(cls, list1, list2):
        count = 0
        for element in list1:
            if element in list2:
               count += 1
        return count

def calculate_top_5_user(user, user_review_history):
    
    user_similarity = {}
    user_id = user[0]
    movies = user[1]
    
    for otheruser_movies in user_review_history:
        
        similarity = Helper.cosine_similarity(movies, otheruser_movies)
        user_similarity[use_id] = similarity


    user_similarity.pop(user_id)
    sorted_tups = sorted(user_similarity.items(), key=operator.itemgetter(1), reverse=True)
    top_5_user = [sorted_tups[0][0], sorted_tups[1][0], sorted_tups[2][0], sorted_tups[3][0], sorted_tups[4][0]]
    #  print ("top_5_movie for "+ str(movie) + ":\t" + str(top_5_movie))
    update_user_recommend(user_id, top_5_user)


def main():
    try:
        user_review_history = retrieve_user_review_history()
        for user in user_review_history.items():
            calculate_top_5_user(user, user_review_history.values())
    except Exception as e:
        print("Exception detected:")
        print(e)


if __name__ == "__main__":
    main()