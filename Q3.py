#!/usr/bin/python
import time
import sys
import networkx as nx
import matplotlib.pyplot as plt



#-------------------------------------------------------------

def WPGMA(file_name):
    start = time.time()
    file1 = open(file_name, 'r')
    txt_mat = file1.read()
    file1.close()

    # To store original names
    labels = {}

    rows = txt_mat.splitlines()
    dim = len(rows) -1
    mat = []

    # Make the matrix from file
    for i in range(1,len(rows)):
        cols = rows[i].split()
        mat.append([])
        labels[(i-1)]=cols[0]
        for j in range(1, len(cols)):
            mat[i-1].append(float(cols[j]))
            
    # keeps track of what rows in the reduced matrix 
    # corespond to what node
    row_node_trans = list(range(dim))

   # Keeps track of where the nodes should be positioned 
    total_nodes = 2*dim -1
    height = [0]*total_nodes
    x_pos = [0]*total_nodes
    next_availabe_floor = 0

    # Adds species nodes
    G = nx.Graph()
    for i in range(dim):
        G.add_node(i)

    node_count = dim

    print_nice_w_lables(mat, labels)
    
    
    for i in range(dim-2):
        # Find minimum value in matrix
        val, x, y = find_min(mat)
        
        # Connect new nodes in graph
        n_id_1 = row_node_trans[x]
        n_id_2 = row_node_trans[y]
        G.add_node(node_count)
        G.add_edge(node_count, n_id_1)
        G.add_edge(node_count, n_id_2)

         # Set height new node
        height[node_count] = max(height[n_id_1], height[n_id_2])+1
        
        # Set x positions for any species nodes
        if n_id_1 < dim:
            x_pos[n_id_1] = next_availabe_floor
            next_availabe_floor +=1

        if n_id_2 < dim:
            x_pos[n_id_2] = next_availabe_floor
            next_availabe_floor += 1
        
        # Set x position for current node
        x_pos[node_count] = (x_pos[n_id_1] + x_pos[n_id_2])/2.0 
        
        # Update the row node translation
        row_node_trans[x] = node_count
        del row_node_trans[y]

        node_count += 1
        
        # Combine the rows
        combine_groups(x, y, mat)

        # Print matrix for that iteration
        print_nice(mat)

   # Finished 
    print_nice(mat)

    # Connect the last 2 graph entities
    n_id_1 = row_node_trans[0]
    n_id_2 = row_node_trans[1]
    G.add_node(node_count)
    G.add_edge(node_count, n_id_1)
    G.add_edge(node_count, n_id_2)

    # Set height new node
    height[node_count] = max(height[n_id_1], height[n_id_2])+1
        
    # Set x positions for any species nodes
    if n_id_1 < dim:
        x_pos[n_id_1] = next_availabe_floor
        next_availabe_floor +=1

    if n_id_2 < dim:
        x_pos[n_id_2] = next_availabe_floor
        next_availabe_floor += 1
    
    # Set x position for current node
    x_pos[node_count] = (x_pos[n_id_1] + x_pos[n_id_2])/2.0 

    # Generate positions out of height and x pos
    pos = [0]*total_nodes
    for i in range(0, dim*2 -1):
        x = x_pos[i]
        y = height[i]
        pos[i] = (x, y)

    # Draw and save graph
    plt.title(file_name) 
    nx.draw(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=12)
    plt.savefig("%s.png"%file_name[:-4])

    # Stop timer, print time
    stop = time.time()
    time_taken=stop-start
    print('Time taken: '+str(time_taken))


# Find minimum value in matrix (excluding 0's)
def find_min(mat):
    dim = len(mat)
    
    # Check we haven't been passed 1x1 matrix
    if(dim<2):
        print("You've gone too far!")
        return
    
    # Set initial min value and location
    min_val = mat[0][1]
    min_val_x = 1
    min_val_y = 0

    # Finds minimum value only checking the top right half
    # Note this could be significantly faster if only half the matrix was stored
    # last row at [0] working backwards, but it makes it much more effort to print every iteration 
    
    # for every row
    for i in range(0, dim-1):

        # Finds the row minimum - turns out this is much faster than the obvious way (thanks python)
        row_min = min(mat[i][i+1:])
        row_min_i = mat[i].index(row_min)
        
        # Check if this row min is the min
        if row_min < min_val:
            min_val = row_min
            min_val_x = row_min_i
            min_val_y = i
        
    return (min_val, min_val_x, min_val_y)

            

# combines group a and b in matrix and removes extra row/col
def combine_groups(a, b, mat):
    low_r = min(a,b)
    high_r = max(a,b)

    for i in range(len(mat)):
        # If ensures we preserve 0's
        if i != low_r and i != high_r:
            cur_r = mat[i]
            # calc unweighted sum
            uw_sum = (cur_r[high_r] + cur_r[low_r])/2.0
            cur_r[low_r] = uw_sum
            mat[low_r][i] = uw_sum

    del_row_col(high_r, mat)

# Deletes row and column of specified matrix
def del_row_col(r_c, mat):
    del mat[r_c]

    for r in mat:
        del r[r_c]


def print_nice(mat):
    print('\n'.join([''.join(['{:7.6}'.format(item) for item in row]) for row in mat]))
    print()

def print_nice_w_lables(A, labels):
    out_s = '{:7}'.format('')
    out_s += ''.join(['{:7}'.format(labels[i]) for i in range(len(A))])
    for i in range(len(A)):
        out_s += '\n{:7}'.format(labels[i])
        for j in range(len(A[i])):
            out_s += '{:7.6}'.format(A[i][j])

    print(out_s)
    #print('\n{:7}'.format(labels[i]).join([''.join(['{:7.6}'.format(item) for item in A[i]]) 
     # for i in range(len(A))]))
    print()
#-------------------------------------------------------------

WPGMA("./matrix2.txt")




#-------------------------------------------------------------

