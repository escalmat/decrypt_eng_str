import sys

from single_byte_XOR_cipher import freq_table_of, bigrams_fq_table_of, rearrange_dict_elms_h_to_l, get_xor_btw, hex_str_to_dec, decrypt_src
from frq_tables import freq_table, bigram_freq_table, eng_letters_fq_h_to_l, dic_data_std_dev

STD_DEV_DIFF_TOLERANCE = 1.30
LOWEST_HEX_FQ_TOLERANCE = 13.00
MAX_PAIR_ELMS_TOLERANCE = 5

# my way of seeing an english formated text is by letter and bigram frq.


# prob of c in hex being "a" in ascii

# get c frq. = c_frq

# since there's a prob that c_frq != its xored ascii
# c could be any ascii in the range of c_frq, range that is not known
# a match between c_frq ---> a_frq can not be made AND our algorithm should NOT relay on this data

# use the bigram fq. space to increace the prob. of finding c ---> a

# look at xc and cy
# get x_frq and y_frq

# if xc_frq close to ba_frq {in ascii} and x_frq and c_frq is in the range of b_frq and a_frq in ascii
# this is the highest prob. we can have that x ---> b and c ---> a, i think


# choose pair c - a by close_frq
# is a in some bigram?
# if 1: get its neighbour frq: a_n_frq
# this a_n_frq is close to the range of c neighbour: c_n_frq?
# if 1: c is a
# get xor dec
# decrypt the string

# if 0: choose another candidate for a, say d or another candidate for c?
# if we change c, the bigram we use to narrow down the error is always the same
# if we change a, the bigram changes
# what's better?
# it's better to change the bigram, since we can't assure which bigram is in the string
# then, we change the candidate for c

def sub_dic_by_key( key, _dict ):

    sub_dic = {}

    for k in _dict.keys():

        if key in k:
            sub_dic[ k ] = _dict[k]

    return sub_dic


def pair_bigrams( set1, set2, id1, id2, id1_fq_t, id2_fq_t ):

    pair = [None,None] # [c, a]

    for k in set1.keys():

        if k[:2] == id1: # form: cy

            for j in set2.keys():

                if j[:2] == id2:

                    if (set1[ k ] / set2[ j ]) < STD_DEV_DIFF_TOLERANCE: # if the difference btw bg fq. of c and bg fq. of a < STD_DEV_DIFF_TOLERANCE

                        if ( id1_fq_t( k[2:] ) / id2_fq_t( j[2:] ) ) < STD_DEV_DIFF_TOLERANCE: # if the difference btw fq. of neighbour of c and fq. of neighbour of a < STD_DEV_DIFF_TOLERANCE
                            # we can say that c is a
                            pair[0] = k[:2]
                            pair[1] = j[:2]

        if k[2:4] == id1: # form: yc

            for j in set2.keys():

                if j[2:4] == id2:

                    if (set1[ k ] / set2[ j ]) < STD_DEV_DIFF_TOLERANCE:

                        if ( id1_fq_t( k[2:4] ) / id2_fq_t( j[2:4] ) ) < STD_DEV_DIFF_TOLERANCE:
                            pair[0] = k[2:4]
                            pair[1] = j[2:4]


    return pair


def equal_fqs( source ):

    src_keys = source_keys()
    value = source[ src_keys[0] ]

    for k in source.keys():

        if source[ k ] != value:
            return False

    return True



def add_to_possible_pairing( pair_l, val1, val2, src_str ):

    poss_pairing = []

    poss_pairing.append( val1 )
    poss_pairing.append( val2 )
    poss_pairing.append( src_str )

    pair_l.append( poss_pairing )

    return pair_l

    

def pair_hex_with_ascii_char( pairs, enc_src, hex_fq_t, hex_bg_frq_t, h_to_l_hex_fq_list, ascii_fq_t, ascii_bg_fq_t, eng_letters_fq_h_to_l ):

    hex_bg_dict = {}
    ascii_bg_dict = {}
    hex_fq_t_std_dev, hex_bg_frq_t_std_dev, ascii_fq_t_std_dev, ascii_bg_fq_t_std_dev = (0, 0, 0, 0)
    hex_ascii_fq_diff = 0


    for n in range( 2 ): # first and second highest hex by fq.

        # get bigrams where hex is part of, could not be part of any known fq. bigram
        hex_bg_dict = sub_dic_by_key(  h_to_l_hex_fq_list[ n ], hex_bg_frq_t )

        for i in range( 5 ): # search for paring with the 5 highest fq. ascii

            # get hex_fq_t, hex_bg_frq_t, ascii_fq_t, ascii_bg_fq_t std. deviation
            
            hex_bg_frq_t_std_dev = dic_data_std_dev( hex_bg_frq_t )
            ascii_bg_fq_t_std_dev = dic_data_std_dev( ascii_bg_fq_t )

            hex_bg_fq_t_diff_amplitude = hex_bg_frq_t_std_dev / ascii_bg_fq_t_std_dev

            hex_fq_t_std_dev = dic_data_std_dev( hex_fq_t )
            ascii_fq_t_std_dev = dic_data_std_dev( ascii_fq_t )

            hex_fq_t_diff_amplitude = hex_fq_t_std_dev / ascii_fq_t_std_dev
            

            # get hex and ascii char fq. difference
            hex_ascii_fq_diff = round( hex_fq_t[ h_to_l_hex_fq_list[ n ] ] / ascii_fq_t[ eng_letters_fq_h_to_l[ i ] ], 2 )
            
            if (
                hex_bg_fq_t_diff_amplitude < STD_DEV_DIFF_TOLERANCE and
                hex_bg_fq_t_diff_amplitude > 1 - (STD_DEV_DIFF_TOLERANCE - 1) and
                hex_fq_t_diff_amplitude < STD_DEV_DIFF_TOLERANCE and
                hex_fq_t_diff_amplitude > 1 - (STD_DEV_DIFF_TOLERANCE - 1)
                ):
                
                # it's accurate to use bigram pairing, strong statistical relation" 

                # get bigrams where ascii char n is part of, could not be part of any known fq. bigram
                ascii_bg_dict = sub_dic_by_key(  eng_letters_fq_h_to_l[ i ], ascii_bg_fq_t )
                       
                # at this point we have the set of bigrams of hex and the set of bigrams of ascii char

                poss_pair = pair_bigrams( hex_bg_dict,
                                          ascii_bg_dict,
                                          hex_fq_t[ h_to_l_hex_fq_list[ n ] ],
                                          ascii_fq_t[ eng_letters_fq_h_to_l[ i ] ],
                                          hex_fq_t, ascii_fq_t )

                pairs = add_to_possible_pairing( pair,
                                                poss_pair[0],
                                                poss_pair[1],
                                                enc_src )

            elif (
                  hex_ascii_fq_diff < STD_DEV_DIFF_TOLERANCE and
                  hex_fq_t_diff_amplitude < (STD_DEV_DIFF_TOLERANCE - 0.15) and
                  hex_fq_t_diff_amplitude > 1 - (STD_DEV_DIFF_TOLERANCE - 1.15)
                  ):

                # it's accurate to pair hex - ascii char by em close fq.

                pairs = add_to_possible_pairing( pairs,
                                                h_to_l_hex_fq_list[ n ],
                                                eng_letters_fq_h_to_l[ i ],
                                                enc_src )

                

    return pairs




def eng_format( hex_fq_dict, hex_fq_h_to_l ):

    # in a non so distant future, this function will go through the list to validate every hex fq. against an avg hex fq. previously tested
    
    try:
    
        if hex_fq_dict[ hex_fq_h_to_l[0] ] < LOWEST_HEX_FQ_TOLERANCE:            
            return False

    except IndexError:
        return False

    except KeyError:
        return False
    
    return True

    

hex_dig_frq = {}
hex_bg_frq = {}
hex_dig_h_to_l_frq = []

src_strings = []

pairs = []

try:
    src_strings = open( "enc_file.txt").readlines()
except IOError:
    print("file not found ", IOError)

line = 0
enc_string_found = False
src_len = len( src_strings )

while line < src_len and len( pairs ) < MAX_PAIR_ELMS_TOLERANCE:

    if '\n' == src_strings[ line ][len( src_strings[ line ] )-1]:
        clean_str = src_strings[ line ][:len( src_strings[ line ] )-1]

    hex_dig_frq = freq_table_of( clean_str )
    hex_dig_h_to_l_frq = rearrange_dict_elms_h_to_l( hex_dig_frq )

    if not eng_format( hex_dig_frq, hex_dig_h_to_l_frq ):
        # since the avg number of letters in english is 4.7
        # there's a space every 4.7 letters
        # => should be len(str) / 5.0 spaces in avg
        # => should be at least one hex dig with fq close to len(str) / 5.0
        
        # if this condition don't test we can assure that it's not an english string format
        line += 1
        continue

    
    hex_bg_frq = bigrams_fq_table_of( clean_str )
    

    pairs = pair_hex_with_ascii_char( pairs,
                                      enc_src=clean_str,
                                      hex_fq_t=hex_dig_frq,
                                      hex_bg_frq_t=hex_bg_frq,
                                      h_to_l_hex_fq_list=hex_dig_h_to_l_frq,
                                      ascii_fq_t=freq_table,
                                      ascii_bg_fq_t=bigram_freq_table,
                                      eng_letters_fq_h_to_l=eng_letters_fq_h_to_l )

    line += 1




for pair in pairs:
    possible_key = ''

    try:
        possible_key = get_xor_btw( hex_str_to_dec( pair[0] ), int.from_bytes( pair[1].encode(), "big" ) )
        print( "pair: [{0}] ---> [{1}]: possible english string: {2}".format( pair[0], pair[1], decrypt_src( pair[2], possible_key ) ) )
    except IndexError:
        pass











    
