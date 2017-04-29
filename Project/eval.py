from recommender import execute
import matplotlib.pyplot as plt
# data=shelve.open("data")
def train_rec(user, neigborhood):
    train = execute('Dataset/ml-100k/u1.base', user, 10, neigborhood)
    return train
def load_test():
        movies = {}
        for line in open("Dataset\ml-100k\u.item"):
                (id, movie) = line.split("|")[0:2]
                movies[id] = movie
        test = {}
        for line in open("Dataset\ml-100k\u1.test"):
                (userId, movieId, rating, ts) = line.split("\t")
                test.setdefault(userId, {})
                test[userId][movies[movieId]] = float(rating)
        return test
def find_hit(user,train):
    test = load_test()
    # print train, test['1']
    count_hit = 0
    for i in train:
        for j in test[user]:
            #print j,i[1]
            if j == i[1]:
                count_hit+=1
    return count_hit
def hit_set():
    hits = {}
    test = load_test()
    for neighborhood in range(10, 200, 10):
        hits[neighborhood]={}
        #print neighborhood
        for user in test:
            temp=[]
            temp=train_rec(user, neighborhood)
            hits[neighborhood][user]=find_hit(user,temp)
    return hits
    # print hits[10]['1']
    # data['hits']=hits
def plots():
    precision = {}
    recall = {}
    f1 = {}
    hits = hit_set()
    test = load_test()
    # print hits[10]['1']
    for i in hits:
        precision[i] = sum([float(hits[i][j]) for j in hits[i]])
        precision[i] = precision[i]/(10.0*len(hits[i]))
        recall[i] = sum([float(hits[i][j])/len(test[j]) for j in hits[i] if j in test])
        f1[i] = ((2.0*(precision[i]*recall[i]))/(precision[i]+recall[i]))
    # plt.plot([i for i in sorted(precision)], [precision[i] for i in sorted(precision)], "ro")
    fig1 = plt.figure(1)
    ax11 = fig1.add_subplot(311)
    plt.xlabel('neighbourhood size')
    plt.ylabel('precision')
    plt.plot([i for i in sorted(precision)], [precision[i] for i in sorted(precision)], "ro")
    for i, j in sorted(precision.items()):
        ax11.annotate(format(j, '.4f'), xy=(i, j))
    ax12 = fig1.add_subplot(312)
    plt.xlabel('neighbourhood size')
    plt.ylabel('recall')
    plt.plot([i for i in sorted(recall)],[recall[i] for i in sorted(recall)])
    for i, j in sorted(recall.items()):
        ax12.annotate(format(j, '.4f'), xy=(i, j))
    ax13 = fig1.add_subplot(313)
    plt.xlabel('neighbourhood size')
    plt.ylabel('f1 metric')
    # plt.yticks(np.arange(0.09, 0.25, 0.02))
    plt.plot([i for i in sorted(f1)], [f1[i] for i in sorted(f1)], "ro")
    # plt.plot([i for i in range(10,200,10)],[0.09 for i in range(1,20)], "ro")
    for i, j in sorted(f1.items()):
        ax13.annotate(format(j, '.2f'), xy=(i, j))
    plt.show()

plots()




