
import time
import math
import os

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    upper=0.0
    for keys in vec1:
        if keys in vec2:
            upper += vec1[keys]*vec2[keys]
    return upper / (norm(vec1)*norm(vec2))



def build_semantic_descriptors(sentences):
    count = {}
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            if not sentences[i][j] in count:
                count[sentences[i][j]] = { }
                for k in range(len(sentences[i])):
                    if sentences[i][j] != sentences[i][k]:
                        if sentences[i][k] in count[sentences[i][j]]:
                            count[sentences[i][j]][sentences[i][k]] += 1
                        else:
                            count[sentences[i][j]][sentences[i][k]] = 1
            else:
                for k in range(len(sentences[i])):
                    if sentences[i][j] != sentences[i][k]:
                        if sentences[i][k] in count[sentences[i][j]]:
                            count[sentences[i][j]][sentences[i][k]] += 1
                        else:
                            count[sentences[i][j]][sentences[i][k]] = 1
    return count               


def build_semantic_descriptors_from_files(filenames):
    text=""
    L = []
    for i in range (len(filenames)):
        text += open(filenames[i], "r", encoding="utf-8").read().lower()
        text +=" "
    text=text.replace("!",".").replace("?",".").replace(","," ").replace("-"," ").replace("--"," ").replace(":"," ").replace(";"," ").replace("'"," ").replace('"'," ")
    text = text.split(".")
    for i in range (len(text)-1):
        L.append(text[i].split(" "))

    while [''] in L:
        L.remove([''])

    for i in L:
        for j in i:
            while ''in i:
                i.remove('')
    ans=build_semantic_descriptors(L)
    return ans

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    counter,similar_score=0,-100000000
    for i in range(len(choices)):
        if word in semantic_descriptors and choices[i] in semantic_descriptors:
            if similarity_fn(semantic_descriptors[choices[i]],semantic_descriptors[word])>similar_score:
                counter = i
                similar_score = similarity_fn(semantic_descriptors[choices[i]],semantic_descriptors[word])

        else:
            return -1
    return choices[counter]
    


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    L=[]
    counter = 0
    text = open("test.txt", "r", encoding="utf-8").read().lower()
    text=text.split("\n")
    for i in range(len(text)):
        L.append(text[i].split(" "))    
    while [''] in L:
        L.remove([''])    

    for i in range(len(L)):
        if L[i][1]==most_similar_word(L[i][0], L[i][2:], semantic_descriptors,similarity_fn):
            counter += 1
    res = (counter*100)/(len(L))
    return res
    
def Euclidean(vec1,vec2):
    sum=0
    for key in vec1:
        if key in vec2:
            sum += ((vec1[key]-vec2[key])*(vec1[key]-vec2[key]))
        else:
            sum += (vec1[key]*vec1[key])
    for key in vec2:
        if key not in vec1:
            sum += (vec2[key]*vec2[key])
    ans = -(sum)**(1/2)
    return ans
    


def norm_Euclidean(vec1,vec2):
    sum=0
    for key in vec1:
        if key in vec2:
            sum += ((vec1[key]/norm(vec1))-(vec2[key]/norm(vec2)))**2
        else:
            sum += (vec1[key]/norm(vec1))**2
    for key in vec2:
        if key not in vec1:
            sum += (vec2[key]/norm(vec2))**2
    ans = -((sum)**(1/2)) 
    return ans


if __name__ == '__main__':
#print(Euclidean({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
# sentences=[["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
# print(build_semantic_descriptors(sentences))
# vec1={"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
# vec2={"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}
# print(cosine_similarity(vec1,vec2))

#["lalala1.txt","lalala2.txt"]
    t1 = time.time()
    os.chdir("/u/c/songya25/Desktop")
    #build_semantic_descriptors_from_files(["lalala1.txt", "lalala2.txt"])
    print(run_similarity_test("test.txt", build_semantic_descriptors_from_files(["lalala1.txt","lalala2.txt"]), cosine_similarity))
    t2=(time.time()-t1)
    print(t2)
