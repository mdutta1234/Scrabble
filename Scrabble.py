"""
Here we have list of words.So we first ask no. of letters they want to play with(the hand). Then we ask them how many times do they want to play the game with the given hand.
In each hand we have a * that can be replaced with any vowel that is we can replace the star with any vowel. 
the game allows us to either exchange a letter or replay a given hand . The word we enter is evaluated based on a formula which evaluates based on the letters used.
"""
import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = int(input("enter the hand size u want "))

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,'*': 0}

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	
def get_word_score(word, n):
   s=0
   word=word.lower()
   for i in word:
       if i in SCRABBLE_LETTER_VALUES:
           s+=SCRABBLE_LETTER_VALUES[i]
           
       else:
           print("wrong input")
	   return 0	
    
    
       
   return (s*max(1,7 * len(word) - 3 * (n-len(word))))

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    hand['*']=1
    
    return hand

def update_hand(hand, word):
    word=word.lower()
    y=get_frequency_dict(word)
   
    z=hand.copy()
    for i in y.keys():
        for k in range(y[i]):
            if z.get(i,0)>=1:
                
                    z[i]-=1
                    
    return z


def isstarthere(word):
    t=False
    for i in word:
        if i=="*":
            t=True
            break
    return t


def possiblewords(word):
    l=[]
    word=word.lower()
    n=word.find("*")
    for i in VOWELS:
        t=word[:n]+i+word[n+1:]
        l.append(t)
    return l
            
def is_valid_word(word, hand, word_list):
    word=word.lower()
    z=get_frequency_dict(word)
    if not isstarthere(word):
        if word in word_list:
            for i in z.keys():
                if z[i]<=hand.get(i,0):
                    t=True
                else:
                    t=False
                    break
        else:
            t=False
        return t
    else:
        y=possiblewords(word)
        
        
        for idk in y:
            I=0
            cam=hand.copy()
            z=get_frequency_dict(idk)
            uwu=finding(word,"*")
            if idk in word_list:
                if idk[uwu:uwu+1] in hand.keys():
                    cam[idk[uwu]]+=1
                else:
                    cam[idk[uwu]]=1
                    
                for i in z.keys():
                    if z[i]<=cam.get(i,0):
                        t=True
                        I+=z[i]
                        
                    else:
                        t=False
                        break
                if I==len(word):
                    break
                
            else:
                t=False
        return t
    
    
def finding(word,x):
    i=0
    for c in word:
        if c==x:
            break
        i+=1
    return i
            
            

def calculate_handlen(hand):
    s=0
    for i in hand.keys():
        s+=hand[i]
    return s

def play_hand(hand, word_list):
    t=0
    while calculate_handlen(hand)!=0:
        print("Current hand :")
        display_hand(hand)
        word=input("Enter word, or !! to indicate you are finished ")
        if word=="!!":
            print("Total Score for this hand:",t,"points")
            break
        else:
            
            if is_valid_word(word, hand, word_list):
                t+=get_word_score(word, HAND_SIZE)
                print(word+" "+"earned "+str(get_word_score(word, HAND_SIZE))+" Points."+"Total for this hand:"+str(t)+" points")
            else:
                print("That is not a valid word .Please choose another word.")
            hand=update_hand(hand, word)
        print()
        print()
        print()
        
    if calculate_handlen(hand)<=0:
        print("Ran out of letters.Total score for this hand: "+str(t)+" points.")
    return t


def substitute_hand(hand, letter):
    y=CONSONANTS+VOWELS
    x=letter
    if x != "*":
        if letter in hand.keys():
            while letter==x:
                x=random.choice(y)
            hand[x]=hand[letter]
            del(hand[letter])
            return hand
        else:
             return hand
    else:
        while x==letter:
            x=random.choice(CONSONANTS)
        hand[x]=hand[letter]
        del(hand[letter])
        return hand
        


       
    
def play_game(word_list):
    score=0
    n=int(input("Enter a no.(no. of games u want to play) "))
    sub=1
    rep=1
    for iterable in range(n):
        print()
        print()
        hand=deal_hand(HAND_SIZE)
        if sub>0 and rep>0: 
            print("Current Hand:", end = " ")
            display_hand(hand)
            w=input("Would you like to substitute a letter?(yes/no): ")
            if w.lower()!="yes":
                print()
                print()
                print()
                z=play_hand(hand, word_list)
                score+=z
            elif w.lower()=="yes":
                letter=input("Which letter would you like to substitute? ")
                hand=substitute_hand(hand, letter)
                sub=0
                print()
                print()
                print()
                z=play_hand(hand, word_list)
                score+=z
            print("--------------")
        else:
            print()
            print()
            print()
            z=play_hand(hand, word_list)
            score+=z
            print("--------------")
        if rep>0 and sub>0:
            ans=input("Would you like to replay?(yes/no): ")
            if ans=="yes":
                score2=play_hand(hand, word_list)
                rep=0
                z=max(z,score2)
                score+=z
                print("Total score for this hand :",score)
                print("--------------")
    print("--------------")
    print("Total score over all hands: ",score)
            
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
