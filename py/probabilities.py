"""
This project analyses a data text in terms of empirical 
probability of transition between all encountered strings
of fixed length k and symbols belonging to the text alphabet
to produce a matrix of conditional probabilities.

This matrix can then be used in the script random_text.py to
generate a text respecting the same probabilities, and hence
the same "style"

Author: Balthazar Rouberol @BaltoRouberol
License : DWTFYWWI (Do What The Fuck You Want With It) 
"""

import pickle
import sys
from os.path import exists

def alphabet(datafile_lines):
    """
    Returns all used characters in a given text
    """

    alph = set()
    for line in datafile_lines:
        alph.update(line)

    return sorted(alph)

def empirical_entropy_rate(datafile_lines, k, alpha, result_filename, debug=False):
    """
    Given a datafile lines and a order k, returns the
    empirical entropy rate for a Markov chain of order k
    """

    if debug:
        print datafile_lines

    res = 0

    # -- split text in ak chunks of length k
    ak_chunks = [datafile_lines[i:i+k] for i in xrange(len(datafile_lines))] 
    if debug:
        print ak_chunks

    # -- remove final chunk if not of size k
    if len(ak_chunks[-1]) != k:
        ak_chunks.remove(ak_chunks[-1]) 
        if debug:
            print ak_chunks

    # -- Extract unique values from list
    ak_chunks = list(set(ak_chunks)) #set: reduce to unique values
    if debug:
        print ak_chunks
    
    # Initialization of matrix
    prob = {}       
    
    for ak in ak_chunks: 
        # New matrix line
        prob[ak] = {}

        # number of times ak encountered in text
        nak = n_ak(datafile_lines, ak)

        # -- calculate *cumulative* p(b|a^k)  for each symbol of the alphabet
        pbak_cumul = 0
        for symbol in alpha:
            pbak = conditional_empirical_proba(datafile_lines, ak, symbol, nak)
            pbak_cumul += pbak

            # if sucession ak+symbol is encountered in text, add probability to matrix
            if pbak != 0.0: # Very important, if pbak = 0.0, the combination ak+symbol will not be randomly generated 
                prob[ak][symbol] = pbak_cumul

    # Results storage
    proba_file = open(result_filename, 'w')
    pickle.dump(prob, proba_file)
    proba_file.close()
    print 'Output file %s has been successfully created.'%(result_filename)
        
    return 0
    

def conditional_empirical_proba(chain, ak, symbol, n_ak): # p(b|a^k)
    """
    Returns the proportion of symbols after the ak string (contained
    in chain string and of length k) which are equal to the value 
    of given parameter 'symbol'
    Ex : conditional_empirical_proba('ABCABD', 2, 'AB', 'C', n_ak) --> 0.5 
    """

    nb_ak = n_b_ak(chain, ak, symbol)
    if n_ak != 0:
        return float(nb_ak)/n_ak
    else:
        return 0
 

def n_ak(chain, ak): # n_(a^k)
    """
    Given a string chain and a strink ak,
    returns the number of times that ak
    is found in chain
    """

    return chain.count(ak)

def n_b_ak(chain, ak, symbol): # n_(b|a^k)
    """
    Given a string chain, returns the number of 
    times that a given symbol is found 
    right after a string ak inside the chain one
    """
 
    if k != 0:
        res = chain.count(ak+symbol)
    else:
        # if k=0, p(b|a^k) = p(b), because the past has no influence
        res = chain.count(symbol)
    return res
    

if __name__=='__main__':

    EXIT_MSG = 'The program will now end.'
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]

        if exists(filepath):
            f = open(filepath,'r')
            f_lines = ' '.join(f.readlines()) # all text in a big string
            f.close()
            
            # deduce alphabet from text
            alph = alphabet(f_lines)
 
            k_list = [10]
            for k in k_list: 
                print 'Generating probability matrix for text %s '%(filepath)
                result_filename = '../results/distribs/distrib_k%d.txt'%(k)
                # Put debug = True to enable print operations
                # Use only with small data, otherwise, useless >_<
                empirical_entropy_rate(f_lines, k, alph, result_filename, debug=False)
        
        else:
            print 'The given file path %s leads to no valid file.' %(filepath)
            print EXIT_MSG
            exit(2)
    else:
        print 'No file path given in argument.'
        print EXIT_MSG
        exit(2)
