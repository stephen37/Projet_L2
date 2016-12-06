# -*- coding: utf-8 -*-
import pickle

def construct_data_set(path_movies, path_ratings, path_users, nb_samples, taux_test):
    f_movies = open(path_movies, "r")  #MovieID::Title::Genres
    f_ratings = open(path_ratings, "r")  #UserID::MovieID::Rating::Timestamp
    f_users = open(path_users, "r") #UserID::Gender::Age::Occupation::Zip-code

    m_genders = {'Action':0,
             'Adventure':1,
             'Animation':2,
	         'Children\'s':3,
	         'Comedy':4,
	         'Crime':5,
	         'Documentary':6,
	         'Drama':7,
	         'Fantasy':8,
	         'Film-Noir':9,
	         'Horror':10,
	         'Musical':11,
	         'Mystery':12,
	         'Romance':13,
	         'Sci-Fi':14,
	         'Thriller':15,
	         'War':16,
	         'Western':17}

    movies = {}
    users = {}

    for movie in f_movies:
        movie_split = movie.split('::')
        movie_ID = int(movie_split[0])
        movies[movie_ID] = movie_split[1:]

    for user in f_users:
        user_split = user.split('::')
        user_age = int(user_split[2])
        #replacing age by integer
        if user_age < 18:
            user_split[2] = 0
        if user_age >= 18 and user_age<= 24:
            user_split[2] = 1
        if user_age >= 25 and user_age<= 34:
            user_split[2] = 2
        if user_age >= 35 and user_age<= 44:
            user_split[2] = 3
        if user_age >= 45 and user_age<= 49:
            user_split[2] = 4
        if user_age >= 50 and user_age<= 55:
            user_split[2] = 5
        if user_age >= 56:
            user_split[2] = 6


        user_ID = int(user_split[0])
        users[user_ID] = user_split[1:]



    average_m = {}
    average_u = {}

    user_movieGen_average = {}
    for rating in f_ratings:
        # UserID::MovieID::Rating::Timestamp
        rating_split = rating.split('::')
        user_ID = int(rating_split[0])
        movie_ID = int(rating_split[1])
        rate = int(rating_split[2])
        if movie_ID in average_m:
            average_m[movie_ID].append(rate)
        else:
            average_m[movie_ID] = []
            average_m[movie_ID].append(rate)
        if user_ID in average_u:
            average_u[user_ID].append(rate)
        else:
            average_u[user_ID] = []
            average_u[user_ID].append(rate)

        movie_Genders = movies[movie_ID][1].split('|')
        for gen in movie_Genders:
            gen = gen.replace('\n', '')
            gen = m_genders[gen]
            if (user_ID, gen) in user_movieGen_average:
                user_movieGen_average[(user_ID, gen)].append(rate)
            else:
                user_movieGen_average[(user_ID, gen)] = []
                user_movieGen_average[(user_ID, gen)].append(rate)

        #ratings[(user_ID,movie_ID)] = int(rating_split[2])

    for id in average_m:
        average_m[id] =  sum(average_m[id])/float(len(average_m[id]))


    for id in average_u:
        average_u[id] =  sum(average_u[id])/float(len(average_u[id]))

    for id in user_movieGen_average:
        user_movieGen_average[id] = sum(user_movieGen_average[id]) / float(len(user_movieGen_average[id]))

    #
    # data_heads = ["18","18-24","25-34", "35-44", "45-49", "50-55", "56", #age
    #     "0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", #occupation
    #     "M", "F" #Gender
    #                 ]

    global_samples_set = []
    #global_target_set = []

    fw_samples = open("dataSet.dat", "w")
    #fw_targets = open("targets.dat", "w")

    n_g = 18
    f_ratings = open("ml-1m/ratings.dat", "r")
    for rating in f_ratings:
        data = [0] * 53
        rating_split = rating.split('::')
        userID = int(rating_split[0])
        movieID = int(rating_split[1])
        rate = int(rating_split[2])
        userAge = users[userID][1]
        data[userAge] = 1
        userOccupation = int(users[userID][2])
        data[userOccupation+7] = 1
        userGender = users[userID][0]
        if userGender == 'M':
            data[28] = 1
        else:
            data[29] = 1
        m_g = [0]*18
        u_g = [0.0]*18
        movie_Genders = movies[movieID][1].split('|')

        for gen in movie_Genders:
            gen = gen.replace('\n', '')
            m_g[m_genders[gen]]= 1
            data[m_genders[gen]+30] = 1
            u_g[m_genders[gen]] = user_movieGen_average[(userID, m_genders[gen])]

        data[48] = round(sum([(i * j)/n_g for (i, j) in zip(m_g, u_g)]),3)
        data[49] = round(average_u[userID],3) # average rating given by u
        data[50] = round(average_m[movieID],3) # average rating of m
        data[51] = 1 # Constant set to 1
        data[52] = rate


        global_samples_set.append(data)
        #global_target_set.append(rate)

    import random
    test_set_ind = random.sample(range(0, nb_samples-1),  int(taux_test*nb_samples))


    global_test_set = []
    global_train_set = []
    for i in range(0, nb_samples):
        if i in test_set_ind:
            global_test_set.append(global_samples_set[i])
        else:
            global_train_set.append(global_samples_set[i])

    pickle.dump(global_test_set, open( "global_test_set.p", "wb" ))
    pickle.dump(global_train_set, open( "global_train_set.p", "wb" ))


# ________________a executer une seule fois_______________________
#construct_data_set(path_movies="ml-1m/movies.dat", path_ratings="ml-1m/ratings.dat",path_users="ml-1m/users.dat",nb_samples = 100000, taux_test=0.2)
#_________________________________________________________________

global_train_set = pickle.load(open( "global_train_set.p", "rb" ))
global_test_set = pickle.load(open( "global_test_set.p", "rb" ))


train_samples = []
train_targets = []

test_samples = []
test_targets = []



fich_dataset = open("dataset_name.data", "w")
fich_datasol = open("dataset_name.solution", "w")

for sample in global_train_set:
    train_samples.append(sample[:len(sample)-1])
    sample_i = '\t'.join(str(e) for e in sample[:len(sample)-1]) + "\n"
    fich_dataset.write(sample_i)
    target_i = sample[len(sample)-1]
    train_targets.append(target_i)
    fich_datasol.write(str(target_i)+'\n')


# for sample in global_test_set:
#     test_samples.append(sample[:len(sample)-1])
#     test_targets.append(sample[len(sample)-1])
#
#
#
#
#
# from sklearn.neural_network import MLPClassifier
#
# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(50, 50, 50), random_state=1)
# clf.fit(train_samples, train_targets)
#
# predictions = clf.predict(test_samples)
#
#
# from sklearn.metrics import mean_squared_error
# print mean_squared_error(test_targets, list(predictions))**0.5


