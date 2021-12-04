


# genetic algorithm search for continuous function optimization
from numpy.random import randint
from numpy.random import rand



# decode bitstring to numbers
def decode(bounds, n_bits, bitstring):
	decoded = list()
	largest = 2**n_bits
	for i in range(len(bounds)):
		# extract the substring
		start, end = i * n_bits, (i * n_bits)+n_bits
		substring = bitstring[start:end]
		# convert bitstring to a string of chars
		chars = ''.join([str(s) for s in substring])
		# convert string to integer
		integer = int(chars, 2)
		# scale integer to desired range
		value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
		# store
		decoded.append(value)
	return decoded
 

# tournament selection
def selection(pop, scores, k=3):
	# first random selection
	selection_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		# check if better (e.g. perform a tournament)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]
 

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if rand() < r_cross:
		# select crossover point that is not on the end of the string
		pt = randint(1, len(p1)-2)
		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]
 

# mutation operator
def mutation(bitstring, r_mut):
	for i in range(len(bitstring)):
		# check for a mutation
		if rand() < r_mut:
			# flip the bit
			bitstring[i] = 1 - bitstring[i]
 

# genetic algorithm
def genetic_algorithm(objective=None, target=None, bounds=None, break_accuracy=0.005, digits=5, n_bits=16, n_iter=199, n_pop=100, r_cross=0.9, r_mut=None):
    if r_mut == None and bounds != None:
        r_mut = 1.0 / (float(n_bits) * len(bounds))
    else:
        r_mut = 0.5
    # initial population of random bitstring
    pop = [randint(0, 2, n_bits*len(bounds)).tolist() for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = 0, objective(target=target, X= decode(bounds, n_bits, pop[0]))
    # enumerate generations
    for gen in range(n_iter):
        if best_eval<= break_accuracy:
            break
        else:
            # decode population
            decoded = [decode(bounds, n_bits, p) for p in pop]
            # evaluate all candidates in the population
            scores = [objective(target=target, X= d) for d in decoded]
            # check for new best solution
            for i in range(n_pop):
                if scores[i] < best_eval:
                    best, best_eval = pop[i], scores[i]
                    print(">%d, new best f(%s) = %f" % (gen,  decoded[i], scores[i]))
            # select parents
            selected = [selection(pop, scores) for _ in range(n_pop)]
            # create the next generation
            children = list()
            for i in range(0, n_pop, 2):
                # get selected parents in pairs
                p1, p2 = selected[i], selected[i+1]
                # crossover and mutation
                for c in crossover(p1, p2, r_cross):
                    # mutation
                    mutation(c, r_mut)
                    # store for next generation
                    children.append(c)
            # replace population
            pop = children
    print('Done!')
    # return [best, best_eval]
    decoded = decode(bounds, n_bits, best)
    rounded_values = [round(element,digits) for element in decoded]
    return rounded_values





# define the total iterations
#n_iter = 100
# bits per variable
#n_bits = 16
# define the population size
#n_pop = 100
# crossover rate
#r_cross = 0.9
# mutation rate
#r_mut = 1.0 / (float(n_bits) * len(bounds))
#r_mut 

#digits = 5

#break_accuracy = 0.005



# define range for input
#bounds = [[1, 3.6], [9.6, 22.2], [50.1, 79.1]]

#target = 201



# objective function
#def objective(target, model, x):
#    M_per=x[0]
#    Xf=x[1]
#    SA=x[2]
#    idata = create_df_testing(M_per, Xf, SA)
#    modeloutput = model.predict(idata)
#    diff = abs(target-modeloutput)
#    return diff



# perform the genetic algorithm search
#rounded_values = genetic_algorithm(objective, target, break_accuracy, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)



#idata = create_df_testing(rounded_values[0], rounded_values[1], rounded_values[2])
#print(idata)
#imodel.predict(idata)[0]


#idata = create_df_testing(1.96, 11.92, 64.16)  #199.66
#idata = create_df_testing(2.57, 13.90, 77.52)   #200.00
#idata = create_df_testing(3.17, 14.67, 50.11)   #210.00


