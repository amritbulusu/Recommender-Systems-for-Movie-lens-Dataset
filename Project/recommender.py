
import math
new = {}
def loadDataset(path=""):
        movies = {}
        for line in open("Dataset\ml-100k\u.item"):
                (id, movie) = line.split("|")[0:2]
                movies[id] = movie
        utility = {}
        for line in open(path, 'r'):
                (userId, movieId, rating, ts) = line.split("\t")
                utility.setdefault(userId, {})
                utility[userId][movies[movieId]] = float(rating)
        return utility
# print loadDataset('C:/Users/Amrit/Desktop/Dataset/ml-100k/u.data')

def pcs(utility, u1, u2):
        movies = {}
        for movie in utility[u1]:
            if movie in utility[u2]:movies[movie] = 1
        len_items = len(movies)

        if len_items == 0:
                return 0
        sum1 = sum([utility[u1][movie] for movie in movies])
        sum2 = sum([utility[u2][movie] for movie in movies])
        sum1Sq = sum([pow(utility[u1][movie], 2) for movie in movies])
        sum2Sq = sum([pow(utility[u2][movie], 2) for movie in movies])

        pSum = sum([utility[u1][movie]*utility[u2][movie] for movie in movies])

        # Calculate Pearson score
        num = pSum-(sum1*sum2/len_items)
        den = math.sqrt((sum1Sq-pow(sum1, 2)/len_items)*(sum2Sq-pow(sum2, 2)/len_items))
        if den == 0:
                return 0
        r = num/den
        return r
# utility = loadDataset()
# print pcs(utility, '1', '2')
# Returns the best 50 matches for user from utility dictionary
def topMatches(utility, user, n=50):
        sim = pcs
        scores = [(other, sim(utility, user, other)) for other in utility if other != user]
        scores.sort()
        scores.reverse()
        top = scores[0:n]
        new = {}
        new[user]=utility[user]
        for person in top:
            new[person[0]]=utility[person[0]]
        # print len(new)
        return new
# print topMatches(utility, '1', 50)
def recommend(new, user):
        total = {}
        # similaritySum = {}
        for other in new:
                if other == user:
                        continue
                similarity = pcs(new, user, other)
                if similarity <= 0:
                        continue
                for movie in new[other]:
                                total.setdefault(movie, 0)
                                total[movie]+= 1

        recmov = [(total[movie], movie)for movie in total]
        recmov.sort()
        recmov.reverse()
        return recmov
rec = loadDataset("dataset/ml-100k/u1.base")
top = topMatches(rec, '1', 40)
recos = recommend(top, '1')
# print recos
# print len(recos)


def execute(path, user, n=5, y=50):
        rec = loadDataset(path)
        top = topMatches(rec, user, y)
        recos = recommend(top, user)[0:n]
        return recos
print "The following are the recommendations for the user with user id 43. The algorithm gives top-5 recommendations from a neighborhood of size 50."
print execute('dataset/ml-100k/u1.base', '43', 10, 50)
