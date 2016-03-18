from dataservice import retrieve_movie_info
from dataservice import retrieve_user_review_history
from dataservice import update_movie_recommend
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

def calculate_top_5_movie(movie, user_review_history):
    
    movie_similarity = {}
    
    for movies in user_review_history:
        
        similarity = Helper.cosine_similarity([movie], movies)
        for other_movie in movies:
            if movie_similarity.has_key(other_movie):
                movie_similarity[other_movie] = movie_similarity[other_movie] + similarity
            else:
                movie_similarity[other_movie] = similarity


    if not movie_similarity.has_key(movie):
        return
    
    
    movie_similarity.pop(movie)
    sorted_tups = sorted(movie_similarity.items(), key=operator.itemgetter(1), reverse=True)
    top_5_movie = [sorted_tups[0][0], sorted_tups[1][0], sorted_tups[2][0], sorted_tups[3][0], sorted_tups[4][0]]
    #  print ("top_5_movie for "+ str(movie) + ":\t" + str(top_5_movie))
    update_movie_recommend(movie, top_5_movie)


def main():
    try:
        movie_info = retrieve_movie_info()
        user_review_history = retrieve_user_review_history()
        for movie in movie_info.keys():
            calculate_top_5_movie(movie, user_review_history.values())
    except Exception as e:
        print("Exception detected:")
        print(e)


if __name__ == "__main__":
        main()
