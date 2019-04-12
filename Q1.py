#!/usr/bin/python
import time
import sys
#import dis

# YOUR FUNCTIONS GO HERE -------------------------------------
# 1. Populate the scoring matrix and the backtracking matrix

def generateBacktrack(seq1, seq2, scoring, scoring_translation):
    print("\n Initialising")
    len_seq_1 = len(seq1) + 1
    len_seq_2 = len(seq2) + 1
    initial_val = 0
    initial_direction = [0,0,0] # [L,D,U]
 

    #cost_matrix = [[0 for i in range(len_seq_1)] for j in range(len_seq_2)]
    #direction_matrix = [[0 for i in range(len_seq_1)] for j in range(len_seq_2)]
    cost_matrix = [x[:] for x in [[0] * len_seq_1] * len_seq_2]
    direction_matrix = [x[:] for x in [[0] * len_seq_1] * len_seq_2]

    gap_score = scoring[0][0]

    enc_seq_1 = string_to_turple(seq1)
    enc_seq_2 = string_to_turple(seq2)

    print("\n Initialising the first rows")
    for i in range(len_seq_1):
        cost_matrix[0][i] = i * gap_score
        direction_matrix[0][i] = 1

    for i in range(len_seq_2):
        cost_matrix[i][0] = i * gap_score
        direction_matrix[i][0]=4


    print("\n Calculating costs")
    
   # print("\nCost matrix")
   # print_nice(cost_matrix)

    for i in range(1,len_seq_2):
        for j in range(1,len_seq_1):
            U = cost_matrix[i-1][j] + gap_score
            L = cost_matrix[i][j-1] + gap_score
            
            #t_1 = scoring_translation[seq1[j-1]]
            #t_2 = scoring_translation[seq2[i-1]]
            #D = cost_matrix[i-1][j-1] + scoring[t_1][t_2]
            D = cost_matrix[i-1][j-1] + scoring[enc_seq_1[j-1]][enc_seq_2[i-1]]


            cost_matrix[i][j] = max(L, U, D)
            
            if cost_matrix[i][j] == L:
                direction_matrix[i][j] += 1

            elif cost_matrix[i][j] == D:
                direction_matrix[i][j] += 2

            elif cost_matrix[i][j] == U:
                direction_matrix[i][j] += 4

         
  
    #print("\nCost matrix")
    #print_nice(cost_matrix)

    #print("\nDirection matrix")python

    #print_nice(direction_matrix)
    return (cost_matrix[len_seq_2-1][len_seq_1-1], direction_matrix)
    #return cost_matrix[len_seq_2-1][len_seq_1-1]

def back_track(direction_matrix, seq_1, seq_2):
    j = len(direction_matrix)-1
    i = len(direction_matrix[0])-1

    alignment = ["",""]
   
    while i > 0 or j > 0:
        if (direction_matrix[j][i]&1) != 0:
            #L
            alignment[0]+=seq_1[i-1] 
            alignment[1]+="-"
            i -= 1
            
        elif (direction_matrix[j][i]&2) != 0:
            #D
            alignment[0]+=seq_1[i-1]
            alignment[1]+=seq_2[j-1]
            i -= 1
            j -= 1

        elif (direction_matrix[j][i]&4) != 0:
            #U
            alignment[0]+="-"
            alignment[1]+=seq_2[j-1]
            j = j-1


    return alignment

def string_to_turple(stng):
    scoring_translation = {"A":1, "C":2, "G":3, "T":4}

    letter_code = [0] * len(stng)
    for i in range(len(stng)):
        letter_code[i] = scoring_translation[stng[i]]
        '''if stng[i] == "A":
             letter_code[i] = 1
        elif stng[i] == "C":
             letter_code[i] = 2
        elif stng[i] == "G":
             letter_code[i] = 3
        elif stng[i] == "T":
             letter_code[i] = 4'''

    return tuple(letter_code)

def print_nice(A):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in A]))

# ------------------------------------------------------------



# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()

start = time.time()

#-------------------------------------------------------------
#     Gap A  C  G  T
# Gap -2 -2 -2 -2 -2
#   A -2  4 -3 -3 -3
#   C -2 -3  3 -3 -3
#   G -2 -3 -3  2 -3
#   T -2 -3 -3 -3  1

#seq1 = 'TGGTCCGCT'
#seq2 = 'TCTGGGC'

practical_scoring_matrix = [[-2, -2, -2, -2, -2],
                            [-2,  1, -1, -1, -1],
                            [-2, -1,  1, -1, -1],
                            [-2, -1, -1,  1, -1],
                            [-2, -1, -1, -1,  1]]

scoring_matrix = ((-2, -2, -2, -2, -2),
                 (-2,  4, -3, -3, -3),
                 (-2, -3,  3, -3, -3),
                 (-2, -3, -3,  2, -3), 
                 (-2, -3, -3, -3,  1))

scoring_translation = {"A":1, "C":2, "G":3, "T":4}

print("Doing dynamic programming")
temp = generateBacktrack(seq1, seq2, scoring_matrix, scoring_translation)
best_score = temp[0]
back_track_matrix = temp[1]

print("Starting backtrack")
best_alignment = back_track(back_track_matrix, seq1, seq2)
#print(string_to_turple(seq1))

#dis.dis(generateBacktrack)

#-------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
#displayAlignment(best_alignment)

#-------------------------------------------------------------

