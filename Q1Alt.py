#!/usr/bin/python
import time
import sys

# YOUR FUNCTIONS GO HERE -------------------------------------


def generateBacktrack(seq1, seq2, scoring):
    len_seq_1 = len(seq1) + 1
    len_seq_2 = len(seq2) + 1


    # Create cost and direction matrices
    cost_matrix = [x[:] for x in [[0] * len_seq_1] * len_seq_2]
    direction_matrix = [x[:] for x in [[0] * len_seq_1] * len_seq_2]


    # String are converted to tuple for faster reads
    enc_seq_1 = string_to_list(seq1)
    enc_seq_2 = string_to_list(seq2)

    
    # Used a lot so copied to var
    gap_score = scoring[0][0]


    # Set first row and column to gap scores
    for i in range(len_seq_1):
        cost_matrix[0][i] = i * gap_score
        direction_matrix[0][i] = 1

    for i in range(len_seq_2):
        cost_matrix[i][0] = i * gap_score
        direction_matrix[i][0] = 4


    # Do the dynamic programming
   
   # Itterator for inside loop saved
    seq1_itt = range(1,len_seq_1)

    # Preloaded so it can be moved to prev row
    cur_row = cost_matrix[0]

    for i in range(1,len_seq_2):
          
        # To avoid python subscript op[] the list are preloaded 
        prev_row = cur_row
        cur_row = cost_matrix[i]
        score_row = scoring[enc_seq_2[i-1]]
        dm_row = direction_matrix[i]

        # Used to keep track of this best score, consequently it can be used as left cell value in next calc
        # Provided its initialised first
        best_s = cur_row[0]

        # Use saved iterator rather than recreating every time
        for j in seq1_itt:
            
            j_prev = j-1
            
            # Calcute the score  for U, L and D
            U = prev_row[j] + gap_score
            L = best_s + gap_score
            D = prev_row[j_prev] + score_row[enc_seq_1[j_prev]]

            #print("[%d][%d] L: %d  D: %d  U: %d"%(i, j, L, D, U))
            # Find biggest and save direction 
            best_s = max(L, U, D)
            cur_row[j] = best_s
            
            # This was designed to store all paths and backtrack through all but I made a few modification to speed it up
            if best_s == L:
                dm_row[j] += 1
            
            elif best_s == D:
                dm_row[j] += 2
            
            elif best_s == U:
                dm_row[j] += 4

            
    #print("\nCost matrix")
    #print_nice(cost_matrix)

    #print("\nDirection matrix")
    #print_nice(direction_matrix)


    return (cost_matrix[len_seq_2-1][len_seq_1-1], direction_matrix)

def back_track(direction_matrix, seq_1, seq_2):
    j = len(direction_matrix)-1
    i = len(direction_matrix[0])-1

    alignment = ["",""]
   
    while i > 0 or j > 0:
        curr_square = direction_matrix[j][i]

        # Directions are stored in bits 
        if (curr_square&1) != 0:
            #L
            alignment[0]+=seq_1[i-1] 
            alignment[1]+="-"
            i -= 1
        elif (curr_square&2) != 0:
            #D
            alignment[0]+=seq_1[i-1]
            alignment[1]+=seq_2[j-1]
            i -= 1
            j -= 1
        elif (curr_square&4) != 0:
            #U
            alignment[0]+="-"
            alignment[1]+=seq_2[j-1]
            j = j-1


    return alignment

# Converts strings to tuples
'''def string_to_tuple(stng):
    letter_code = [0] * len(stng)
    for i in range(len(stng)):
        if stng[i] == "A":
             letter_code[i] = 1
        elif stng[i] == "C":
             letter_code[i] = 2
        elif stng[i] == "G":
             letter_code[i] = 3
        elif stng[i] == "T":
             letter_code[i] = 4

    return tuple(letter_code)
'''

def string_to_list(stng):
    letter_code = [0] * (len(stng)+1)
    for i in range(len(stng)):
        if stng[i] == "A":
             letter_code[i] = 1
        elif stng[i] == "C":
             letter_code[i] = 2
        elif stng[i] == "G":
             letter_code[i] = 3
        elif stng[i] == "T":
             letter_code[i] = 4

    return letter_code


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

'''practical_scoring_matrix = [[-2, -2, -2, -2, -2],
                            [-2,  1, -1, -1, -1],
                            [-2, -1,  1, -1, -1],
                            [-2, -1, -1,  1, -1],
                            [-2, -1, -1, -1,  1]]
'''

scoring_matrix = ((-2, -2, -2, -2, -2),
                 (-2,  4, -3, -3, -3),
                 (-2, -3,  3, -3, -3),
                 (-2, -3, -3,  2, -3), 
                 (-2, -3, -3, -3,  1))



# Do dynamic programming
best_score, back_track_matrix =  generateBacktrack(seq1, seq2, scoring_matrix)

# Backtrack
best_alignment = back_track(back_track_matrix, seq1, seq2)

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

