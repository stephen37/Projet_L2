# -*- coding: utf-8 -*-
import csv
from math import sqrt

#_______________________________________________________________________________________________________________________
# http://dataaspirant.com/2015/05/25/collaborative-filtering-recommendation-engine-implementation-in-python/
train_path = "MovieLens_train.solution"

def loadTrainData(train_path) : 
	file_train = csv.reader(open(train_path,"rb"))
	dataset = {}
	for row in file_train:
		splited_row = row[0].split(" ")
		userID = splited_row[0]
		rates = {}
		for rate in splited_row[1:]:
			rate = rate.split(":")
			if len(rate)>1:
				rates[rate[0]] = float(rate[1])

		dataset[userID] = rates
		



def similarity_score(person1, person2, dataset):
    # Returns ratio Euclidean distance score of person1 and person2

    both_viewed = {}  # To get both rated items by person1 and person2

    for item in dataset[person1]:
        if item in dataset[person2]:
            both_viewed[item] = 1

        # Conditions to check they both have an common rating items
        if len(both_viewed) == 0:
            return 0

        # Finding Euclidean distance
        sum_of_eclidean_distance = []

        for item in dataset[person1]:
            if item in dataset[person2]:
                sum_of_eclidean_distance.append(pow(dataset[person1][item] - dataset[person2][item], 2))
        sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

        return 1 / (1 + sqrt(sum_of_eclidean_distance))


def pearson_correlation(person1, person2, dataset):
    # To get both rated items
    both_rated = {}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    # Checking for number of ratings in common
    if number_of_ratings == 0:
        return 0

    # Add up all the preferences of each user
    person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
    person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

    # Sum up the squares of preferences of each user
    person1_square_preferences_sum = sum([pow(dataset[person1][item], 2) for item in both_rated])
    person2_square_preferences_sum = sum([pow(dataset[person2][item], 2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
    person1_preferences_sum * person2_preferences_sum / number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (
    person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r


def most_similar_users(person, number_of_users):
    # returns the number_of_users (similar persons) for a given specific person.
    scores = [(pearson_correlation(person, other_person), other_person) for other_person in dataset if other_person != person]
    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def user_reommendations(person, dataset):

    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}
    simSums = {}
    rankings_list = []
    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        sim = pearson_correlation(person, other, dataset)

        # ignore scores of zero or lower
        if sim  <=0:
            continue
        for item in dataset[other]:

            # only score movies i haven't seen yet
            if item not in dataset[person] or dataset[person][item] == 0:
                # Similrity * score
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

                    # Create the normalized list

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    # returns the recommended items
    recommendataions_list = [recommend_item for score, recommend_item in rankings]
    return recommendataions_list


# for user1 in dataset:
#     for user2 in dataset:
#         print "Similarity Score: ", similarity_score(user1, user2)
#         print "Pearson Correlation: ", pearson_correlation(user1, user2)
#         print " "

def makeSubmissionFile(predictionFile, usersBase, dataset) : 
    fsol = open(predictionFile, "w")
    users = open(usersBase, "r")
    firstLine=1
    for user in users : 
        if (firstLine == 1):
    		fsol.write(str(int(user)))
    		firstLine = 0
        else:
    		fsol.write("\n" + str(int(user)))
        rec = user_reommendations(str(int(user)), dataset)
        mini =min ([100, len(rec)])
        for val in rec[0:mini]  :
    		fsol.write(" "+val)

#makeSubmissionFile("FC.predict", "MovieLens_valid.data")

#for user in dataset:
#    print "User: ", user
#    print "Recommendations: ", user_reommendations(user)
#    print

#_______________________________________________________________________________________________________________________
    # f = open("ml-1m/ratings.dat", "r")
    # fw = open("ratings.csv", "w")
    #
    # user = 0
    #
    # for line in f:
    # 	token = line.split("::")
    # 	if (int(token[0]) != user):
    # 		user = int(token[0])
    # 		fw.write("\n" + str(user))
    # 	fw.write(" " + token[1] + ":" + token[2])
    #
    # import random
    #
    # f = open("ratings.csv", "r")
    # ftrain = open("train.csv", "w")
    # fvalid = open("valid.csv", "w")
    # ftest = open("test.csv", "w")
    #
    # PVALID = 10;  # Pourcentage de l'ensemble de validation
    # PTEST = 10;  # Pourcentage de l'ensemble de test
    # PTRAIN = 100 - PVALID - PTEST
    # LIMITE = 100  # Nombre minimum de films notés pour être ajouté aux données
    #
    # firstLine = 1;
    #
    # for line in f:
    #     token = line.split(" ")
    #     userN = token[0]
    #     token.pop(0);
    #
    #     movieNumber = len(token)
    #
    #     # Si movieNumber inférieur à la limite on saute la ligne
    #     if (movieNumber < LIMITE):
    #         continue
    #
    #     # On enlève le linebreak sur le dernier token
    #     token[movieNumber - 1] = token[movieNumber - 1][:-1]
    #
    #     testLen = int((movieNumber * PTEST) / 100)
    #     validLen = int((movieNumber * PVALID) / 100)
    #     trainLen = int(movieNumber - testLen - validLen)
    #
    #     random.shuffle(token)
    #
    #     test = token[:testLen]
    #     valid = token[testLen:testLen + validLen]
    #     train = token[testLen + validLen:]
    #
    #     if (firstLine == 1):
    #         ftrain.write(userN)
    #         fvalid.write(userN)
    #         ftest.write(userN)
    #         firstLine = 0
    #     else:
    #         ftrain.write("\n" + userN)
    #         fvalid.write("\n" + userN)
    #         ftest.write("\n" + userN)
    #     for val in train:
    #         ftrain.write(" " + val)
    #
    #     for val in valid:
    #         fvalid.write(" " + val)
    #
    #     for val in test:
    #         ftest.write(" " + val)
    #
    #
#_______________________________________________________________________________________________________________________
# import graphlab
# import pandas as pd
#Reading users file:
# u_cols = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']
# users = pd.read_csv('ml-1m/users.dat', sep='::', names=u_cols,
#  encoding='latin-1')

#Reading ratings file:
# r_cols = ['UserID', 'MovieID', 'Rating', 'Timestamp']
# ratings = pd.read_csv('ml-1m/ratings.dat', sep='::', names=r_cols,
#  encoding='latin-1')


#Reading items file:
# m_cols = ['MovieID', 'Title' ,'Genres']
# movies = pd.read_csv('ml-1m/movies.dat', sep='::', names=m_cols, encoding='latin-1')

# import random
# def create_train_test():
#     fw_train = open("ratings.train", "w")
#     fw_test = open("ratings.test", "w")
#     ratings_file = open("ml-1m/ratings.dat", "r")
#     temp = {}
#     for line in ratings_file:
#         current_user = line.split('::')[0]
#         if current_user in temp:
#             temp[current_user].append(line)
#         else:
#             temp[current_user] = []
#             temp[current_user].append(line)
#
#     for user in temp:
#         # ajouter un shuffle ici
#         for line in temp[user][0:9]:
#             fw_test.write(line)
#         for line in temp[user][10:]:
#             fw_train.write(line)
#
# #create_train_test()
#
#
# r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
# ratings_base = pd.read_csv('ratings.train', sep='::', names=r_cols, encoding='latin-1')
# ratings_test = pd.read_csv('ratings.test', sep='::', names=r_cols, encoding='latin-1')
#
# train_data = graphlab.SFrame(ratings_base)
# test_data = graphlab.SFrame(ratings_test)

# popularity_model = graphlab.popularity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating')
#
# popularity_recomm = popularity_model.recommend(users=range(1,6),k=5)
# popularity_recomm.print_rows(num_rows=25)
