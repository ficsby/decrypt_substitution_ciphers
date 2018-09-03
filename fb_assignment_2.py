import random
import re
import math
import copy
#   Disclaimer: My attempted algorithm for ciphers 3 and 4 derives from a machine learning concept called Genetic Algorithm
#               this algorithm takes the concept of Evolution and the sruvival of the fittest. By utilizing the fact that
#               a random key can decipher the cipher text partially right (even by a little), it builds upon its mistakes
#               and bad keys by minimizing the population size to the best fit keys. After a series of iteration, the ideal
#               result is when the final output shows the correct decrypted message. However, my algorithm gets stuck at what is called the
#               local optima (60%-80%) for most cases where it stops learning and assumes it is right (even if it's not).
#               http://ikuz.eu/2017/06/30/breaking-substitution-cipher-using-genetic-algorithm/  <-- one source I used to help


#Wordbank function takes in my text file containing the book I used as my dictionary
#Builds an array containing all words in the book "Pride and Prejudice"
def wordbank():
    file = open('pride_prejudice.txt')
    wordbank = set(re.findall('\w+', file.read().lower()))
    file.close()
    return wordbank

#Wordblock function takes in my text file containing the book I used as my dictionary
#Builds a string with no spaces containing meshing all words in the book "Pride and Prejudice"
def wordblock():
    file = open('pride_prejudice.txt')
    wordbank = re.findall('\w+', file.read().lower())
    wordblock = ""
    for i in wordbank:
        wordblock += i
    return wordblock

#Make unigrams function takes in a string parameter in which it will create a dictionary of all unigrams in the passed in text
#which the key is the unigram and the value is the frequency the unigram appears in the text
def make_unigrams(text):
    text = text.replace(" ", "")
    let_freq = dict()
    for c in text:
        if(c in let_freq):
            let_freq[c] += 1
        else:
            let_freq[c] = 1
    return let_freq

#Make digrams function takes in a string parameter in which it will create a dictionary of all digrams in the passed in text
#which the key is the digram and the value is the frequency the digram appears in the text
def make_digrams(text):
    text = text.replace(" ", "")
    digrams = dict()
    while len(text) > 1:
        digram_pattern = text[0:2]
        if digram_pattern not in digrams:
            digrams[digram_pattern] = 1
        else:
            digrams[digram_pattern] += 1
        text = text[1::]
    return digrams

#Make trigrams function takes in a string parameter in which it will create a dictionary of all trigrams in the passed in text
#which the key is the trigram and the value is the frequency the trigram appears in the text
def make_trigrams(text):
    text = text.replace(" ", "")
    trigrams = dict()
    while len(text) > 2:
        trigram_pattern = text[0:3]
        if trigram_pattern not in trigrams:
            trigrams[trigram_pattern] = 1
        else:
            trigrams[trigram_pattern] += 1
        text = text[1::]
    return trigrams

cipher_1 = "fqjcb rwjwj vnjax bnkhj whxcq nawjv nfxdu mbvnu ujbbf nnc"
cipher_2 = "oczmz vmzor jocdi bnojv dhvod igdaz admno ojbzo rcvot jprvi oviyv aozmo cvooj ziejt dojig toczr dnzno jahvi fdiyv xcdzq zoczn zxjiy"
cipher_3 = "ejitp spawa qleji taiul rtwll rflrl laoat wsqqj atgac kthls iraoa twlpl qjatw jufrh lhuts qataq itats aittk stqfj cae"
cipher_4 = "iyhqz ewqin azqej shayz niqbe aheum hnmnj jaqii yuexq ayqkn jbeuq iihed yzhni ifnun sayiz yudhe sqshu qesqa iluym qkque aqaqm oejjs hqzyu jdzqa diesh niznj jayzy uiqhq vayzq shsnj jejjz nshna hnmyt isnae sqfun dqzew qiead zevqi zhnjq shqze udqai jrmtq uishq ifnun siiqa suoij qqfni syyle iszhn bhmei squih nimnx hsead shqmr udquq uaqeu iisqe jshnj oihyy snaxs hqihe lsilu ymhni tyz"

alphabet = "abcdefghijklmnopqrstuvwxyz"
def decrypt_caesar(cipher):
    decrypted_message = ""
    cipher = cipher.replace(" ", "")
    words = wordbank()
    #used to count how many words in each decryption
    shift_words = {}
    decrypted_messages = {}
    offset = 0
    sum = 0
    for i in range(26):
        shift_words[i] = 0
        decrypted_messages[i] = ""
    #caesar cipher
    for shift in range(26):  #brute forces by shifting encrypted message (0 shifts to 26 shifts)
        for c in cipher:
            d_num = (ord(c) - shift - 97) % 26 + 97
            decrypted_message += chr(d_num)

        decrypted_messages[shift] = decrypted_message

        #counts how many english words in decrypted text --> (most is the correct decryption)
        for w in words:
            if w in decrypted_message:
                shift_words[shift] += 1     #amount of words in decrypted message
        offset = sorted(shift_words, key=shift_words.get, reverse = True)[0]
        sum += shift_words[shift]
        decrypted_message = ""

    print("Offset: ", offset, "\nMessage: ", decrypted_messages[offset],"\n")

#Takes in a key string and makes a dictionary mapping of that string
#Ex: key = "abcdefghijklmnopqrstuvwxyz"
#Return: {"a": 'e', "b": 'd', "c": 'f',...., "z": 'x'}
def create_dict_key(key_text):
    dict_key = dict()
    for i in range(len(alphabet)):
        dict_key[alphabet[i]] = key_text[i]
    return dict_key

#Takes in the cipher text to be decrypted and a dictionary key to base its decryption on
def decrypt_cipher(cipher_text, key_dict):
    potential_text = cipher_text.replace(" ", "")
    for cipher_letter in potential_text:
        potential_text = potential_text.replace(cipher_letter, key_dict[cipher_letter].upper())
    return potential_text.lower()

#Fitness is defined as how well the decrypted text matches the plaintext
#This is calculated by taking the difference of the amount of each unigram, digram, and trigram values from the reference text by the
#amount of unigram, digram, trigram values from the cipher text. The sum of all these values results the decrypted_text's fitness
def calculate_fitness(decrypted_text, unigrams, digrams, trigrams):
    unigrams_in_decrypted = make_unigrams(decrypted_text)
    digrams_in_decrypted = make_digrams(decrypted_text)
    trigrams_in_decrypted = make_trigrams(decrypted_text)
    fitness = 0

    #Unigram Summation
    for i in unigrams_in_decrypted:
        if i in unigrams:
            fitness += unigrams[i] - unigrams_in_decrypted[i]

    #Digram Summation
    for i in digrams_in_decrypted:
        if i in digrams:
            fitness += digrams[i] - digrams_in_decrypted[i]

    #Trigram Summation
    for i in trigrams_in_decrypted:
        if i in trigrams:
            fitness += trigrams[i] - trigrams_in_decrypted[i]
    return fitness

#Crossover serves the purpose of 'mating' or combining two different parents with the possibility of mutating the children
#Side Note: Genetic Algorithm works on the fact that you use best fit parents which are the best fit keys and creates
#           children or variations of these best fit keys. These child keys are then used to decipher the text and through iteration,
#           the decrypted plaintext will be correct.
def crossover(parent_key1, parent_key2):
    # Create dictionary mapping for Parent 1
    parent_key1 = create_dict_key(parent_key1)
    parent_key2 = create_dict_key(parent_key2)

    #Set up children so the merging of parents can occur
    new_child_1 = {chr(i):'' for i in range(97, 123)}
    new_child_2 = {chr(i): '' for i in range(97, 123)}
    new_children = []

    crossover_pt = random.randrange(0, 26) #crossover point determines the point in which the parent keys are sliced
                                           #the children then take half of each parent in its respected positions
                                           #repeated elements are filled in afterwards

    #Initialize child 1 with the first slice of parent 1
    for i in range(0, crossover_pt):
        curr_letter = chr(i+97)
        new_child_1[curr_letter] = parent_key1[curr_letter]

    #Fill the second half of child 1 with second slice of parent 2
    for j in range(crossover_pt, len(parent_key2)):
        curr_letter = chr(j+97)
        if parent_key2[curr_letter] not in new_child_1.values() and new_child_1[curr_letter] == '':
            new_child_1[curr_letter] = parent_key2[curr_letter]

    #If some blanks are still present (due to repeated elements), fill the rest in alphabetical order
    for a in alphabet:
        for k in new_child_1:
            if a not in new_child_1.values() and new_child_1[k] == '':
                new_child_1[k] = a

    new_child_1 = list(new_child_1.values())    #Take values from the dictionary i.e. the key of the new_child_1

    #Initialize child 2 with the first slice of parent 2
    for i in range(0 , crossover_pt):
        curr_letter = chr(i+97)
        new_child_2[curr_letter] = parent_key2[curr_letter]

    #Fill in the second half of child 2 with second slice of parent 1
    for j in range(crossover_pt, len(parent_key1)):
        curr_letter = chr(j + 97)
        if parent_key1[curr_letter] not in new_child_2.values() and new_child_2[curr_letter] == '':
            new_child_2[curr_letter] = parent_key1[curr_letter]

    #If some blanks are still present (due to repeated elements), fill the rest in alphabetical order
    for a in alphabet:
        for k in new_child_2:
            if a not in new_child_2.values() and new_child_2[k] == '':
                new_child_2[k] = a

    new_child_2 = list(new_child_2.values())    #Take values from the dictionary i.e. the key of the new_child_1

    isMutated = random.randrange(0, 10)     #Random number represents probability for a mutation

    # Mutation sequence
    # Children are mutated by having random bit array in which if a 1 is present, the value from the parent stays in same position
    # if a 0 is present, a value from parent 2 replaces it
    if(isMutated < 7):
        mutated = [random.randint(0, 1) for i in range(26)]
        mutated_children = []
        mutated_child_1 = ["*" for i in range(26)]      #initialize with filler characters
        mutated_child_2 = ["*" for i in range(26)]

        #for child 1
        for i in range(len(parent_key1)):
            curr_letter = chr(i+97)
            if mutated[i] == 1:
                mutated_child_1[i] = parent_key1[curr_letter]
        for p in parent_key1:
            for k in range(len(mutated_child_1)):
                if parent_key2[p] not in mutated_child_1 and mutated_child_1[k] == "*":
                    mutated_child_1[k] = parent_key2[p]

        #for child 2
        for j in range(len(parent_key2)):
            curr_letter = chr(j+97)
            if mutated[j] == 1:
                mutated_child_2[j] = parent_key2[curr_letter]
        for p in parent_key2:
            for k in range(len(mutated_child_2)):
                if parent_key1[p] not in mutated_child_2 and mutated_child_2[k] == "*":
                    mutated_child_2[k] = parent_key1[p]

        #An additional mutation randomly occurs to attempt the population to break out of local optima
        if(isMutated < 3):
            random.shuffle(mutated_child_1)
            random.shuffle(mutated_child_2)

        mutated_children.append(''.join(mutated_child_1))
        mutated_children.append(''.join(mutated_child_2))
        return mutated_children

    new_children.append(''.join(new_child_1))
    new_children.append(''.join(new_child_2))

    return new_children

#Sorts dictionary by value in descending order (highest value on top)
def sort_dict(dictionary):
    sorted_dict_list = sorted(copy.deepcopy(dictionary), key=dictionary.get, reverse=True)
    return sorted_dict_list

#Genetic algorithm that works in these stages:
#   Initailize text statistics (unigram, digram, trigram frequencies)
#   Create a population of randomly generated keys (population size = 20)
#   For each population, keep the top 20% to stay in next population, Crossover remaining members
#   Mutate some children
#   Replace existing population so the new population would have the "more fitted" population
def genetic_algorithm(cipher_text):
    gen_num = 0
    training_text = wordblock() #text from the book "Pride and Prejudice" to serve as data for n-gram frequencies
    #Gathering text data may take some time to load
    print("GATHERING STATISTIC INFORMATION....")
    training_unigrams = make_unigrams(training_text)
    training_digrams = make_digrams(training_text)
    training_trigrams = make_trigrams(training_text)    #trigram patterns found in "Pride and Prejudice" used to calculate the fitness of decrypted messages (this portion will take some time to process)
    decryptions = {}                                    #dictionary for the decrypted text and its fitness score
    hold_text = {}
    parents = [''.join(random.sample(alphabet, len(alphabet))) for i in range(20)] #generates random key (parents)

    print("DECRYPTING MESSAGE...")
    while gen_num < 1000:   #1000 is the generation size

        for parent in parents:
            parent_key = create_dict_key(copy.deepcopy(parent))
            decrypted_text = decrypt_cipher(cipher_text, parent_key)
            fitness = calculate_fitness(decrypted_text, training_unigrams, training_digrams, training_trigrams)
            decryptions[parent] = fitness
            hold_text[parent] = decrypted_text

        parents_sorted = sort_dict(copy.deepcopy(decryptions))[:20]  #takes the top 20 keys that produce the best fit decrypted text
        selection_wheel = []
        new_generation = []

        #This section randomly chooses pairs that will crossover
        for i in parents_sorted:
                for j in range(int(math.floor(decryptions[i]))//1000):
                    selection_wheel.append(i)                           #creates an array to draft parents from, those with high fitness values have more chances to be drafted

        starting_point = random.randrange(0, len(selection_wheel))
        selected = []
        while len(selected) < 16:                               #16 numer of parents
            if starting_point >= len(selection_wheel):
                starting_point = 0 + (len(selection_wheel) - starting_point)
            selected.append(selection_wheel[starting_point])
            starting_point += (len(selection_wheel) // 16)       #16  number of parents

        random.shuffle(selected)

        #This section calls the crossover on parent pairs, or transfers parents to the next generation
        for i in range(0,len(selected),2):
            parent1 = selected[i]
            parent2 = selected[i+1]
            cross_chance = random.randrange(0, 10)
            if cross_chance > 7:
                new_generation += crossover(parent1, parent2)
            else:
                transfer = [parent1, parent2]
                new_generation += transfer

        parents = new_generation    #set population to the new generated population
        gen_num += 1
    print("Key: ", parents_sorted[0])
    print("Message: ", hold_text[parents_sorted[0]],"\n")

decrypt_caesar(cipher_1)
decrypt_caesar(cipher_2)
genetic_algorithm(cipher_3)
genetic_algorithm(cipher_4)


