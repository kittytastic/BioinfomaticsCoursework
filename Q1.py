#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------
# 1. Populate the scoring matrix and the backtracking matrix

def generateBacktrack(seq1, seq2, scoring, scoring_translation):
    len_seq_1 = len(seq1) + 1
    len_seq_2 = len(seq2) + 1
    initial_val = 0
    initial_direction = [0,0,0] # [L,D,U]


    cost_matrix = [[initial_val for i in range(len_seq_1)] for j in range(len_seq_2)]
    direction_matrix = [[list(initial_direction) for i in range(len_seq_1)] for j in range(len_seq_2)]

    gap_score = scoring[0][0]

    print("\n Initialising the first rows")
    for i in range(len_seq_1):
        cost_matrix[0][i] = i * gap_score
        direction_matrix[0][i][0] = 1

    for i in range(len_seq_2):
        cost_matrix[i][0] = i * gap_score
        direction_matrix[i][0][2]=1

    #print_nice(cost_matrix)


    print("\n Calculating costs")

    for i in range(1,len_seq_2):
        for j in range(1,len_seq_1):
            U = cost_matrix[i-1][j] + gap_score
            L = cost_matrix[i][j-1] + gap_score
            
            t_1 = scoring_translation[seq1[j-1]]
            t_2 = scoring_translation[seq2[i-1]]
            D = cost_matrix[i-1][j-1] + scoring_matrix[t_1][t_2]


            cost_matrix[i][j] = max(L, U, D)
            
            if cost_matrix[i][j] == L:
                direction_matrix[i][j][0] = 1

            if cost_matrix[i][j] == D:
                direction_matrix[i][j][1] = 1

            if cost_matrix[i][j] == U:
                direction_matrix[i][j][2] = 1 
  
    #print("Cost matrix")
    #print_nice(cost_matrix)

    #print("Direction matrix")
    #print_nice(direction_matrix)
    return (cost_matrix[len_seq_2-1][len_seq_1-1], direction_matrix)

'''def back_track(direction_matrix, i, j, prev_1, prev_2):
    #print("in  (i,j) = (%d, %d)"%(i,j))
    if i == 0 and j == 0:
        print()
        print("seq 1: %s"%prev_1[::-1])
        print("seq 2: %s"%prev_2[::-1])
        return
    
    if direction_matrix[j][i][0] == 1:
        #print("Contains an L reccing into (i,j) = (%d, %d)"%(i-1,j))
        prev_new_1 = prev_1 + seq_1[i-1] 
        prev_new_2 = prev_2 + "-"
        back_track(direction_matrix, i-1, j, prev_new_1, prev_new_2)
    
    if direction_matrix[j][i][1] == 1:
        #print("Contains an D reccing into (i,j) = (%d, %d)"%(i-1,j-1))
        prev_new_1 = prev_1 + seq_1[i-1]
        prev_new_2 = prev_2 + seq_2[j-1]
        back_track(direction_matrix, i-1, j-1, prev_new_1, prev_new_2)

    if direction_matrix[j][i][2] == 1:
        #print("Contains an U reccing into (i,j) = (%d, %d)"%(i,j-1))
        prev_new_1 = prev_1 + "-"
        prev_new_2 = prev_2 + seq_2[j-1]
        back_track(direction_matrix, i, j-1, prev_new_1, prev_new_2)
'''
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

#seq1 = 'TGGTCTCT'
#seq2 = 'TCTGGGCTC'

practical_scoring_matrix = [[-2, -2, -2, -2, -2],
                            [-2,  1, -1, -1, -1],
                            [-2, -1,  1, -1, -1],
                            [-2, -1, -1,  1, -1],
                            [-2, -1, -1, -1,  1]]


scoring_matrix = [[-2, -2, -2, -2, -2],
                 [-2,  4, -3, -3, -3],
                 [-2, -3,  3, -3, -3],
                 [-2, -3, -3,  2, -3], 
                 [-2, -3, -3, -3,  1]]

scoring_translation = {"A":1, "C":2, "G":3, "T":4}

temp = generateBacktrack(seq1, seq2, scoring_matrix, scoring_translation)
best_score = temp[0]
back_track_matrix = temp[1]



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

