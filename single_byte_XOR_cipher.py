# decode a string which has been encode by XORing against a single character

# the string is suppoced to be in english format
# we need to know if the cippher is injective. if so, different hex digit represent different english letter
# so, we work with english format features lika, the frequency of the characters

import sys

sys.path.insert( 1, 'C:\\Users\\User\\Documents\\training day\\sec_engineering\\crypto_lab\\the cryptopals crypto challenges\\set 1\\1' )

from hex_to_base64_cryptopal_version import clean_hex
from frq_tables import freq_table, bigram_freq_table, dic_data_std_dev, eng_letters_fq_h_to_l


def freq_table_of( source ):

    freq_table = {}
    source_len = len( source )

    if source_len % 2 != 0:
        return freq_table

    n = 0

    while n < source_len:

        hex_dig = source[n] + source[n+1]

        if hex_dig not in freq_table.keys():
            freq_table[ hex_dig ] = 1
        else:
            freq_table[ hex_dig ] += 1

        n += 2


    for k in freq_table.keys():

        freq_table[ k ] = round( ( float( freq_table[ k ] ) / float( source_len/2 ) ) * float( 100 ), 2 )


    return freq_table



def rearrange_dict_elms_h_to_l( _dict ):

    dict_elms_h_to_l = []
    _dict_keys = _dict.keys()
    highest_value_found = -1
    highest_elm_of_the_cycle = ''

    for cycle in range( len( _dict ) ):


        for k in _dict_keys:
            
            if  ( _dict[ k ] >= highest_value_found ) and not( k in dict_elms_h_to_l ):
                highest_value_found = _dict[ k ]
                highest_elm_of_the_cycle = k

        
        dict_elms_h_to_l.append( highest_elm_of_the_cycle )
        highest_value_found = -1

    return dict_elms_h_to_l



def bigrams_fq_table_of( source ):

    bg_freq_table = {}
    source_len = len( source )

    if source_len % 2 != 0:
        return -1

    n = 0

    while n < source_len-2: # n = source_len - 4 is the last n processed, cause when it's n += 2 in the next cycle n = source_len-2 

        hex_dig = source[n] + source[n+1]
        # hex digs have struct n + n+1
        # we add bigrams with n + n+1 + n+2 + n+3 structure,
        # so all hex dig but the first and the last, will be at the left side of the bg and at the right side
        # since this is true for the entire string we can count the repeated bigrams with any hex dig at the left or the right side
        bg_right = hex_dig + source[ n+2 ] + source[ n+3 ] 
        
        if bg_right not in bg_freq_table.keys():
            bg_freq_table[ bg_right ] = 1
        else:
            bg_freq_table[ bg_right ] += 1

            
        """
        if n > 1 and n < source_len - 3:
            # middle

            bg_left = source[ n-2 ] + source[ n-1 ] + hex_dig
            bg_right = hex_dig + source[ n+2 ] + source[ n+3 ]

            if bg_left not in bg_freq_table.keys():
                bg_freq_table[ bg_left ] = 1
            else:
                bg_freq_table[ bg_left ] += 1

            if bg_right not in bg_freq_table.keys():
                bg_freq_table[ bg_right ] = 1
            else:
                bg_freq_table[ bg_right ] += 1
                

        if n == source_len - 1:
            # end
            
            bg_left = source[ n-2 ] + source[ n-1 ] + hex_dig
            if bg_left not in bg_freq_table.keys():
                bg_freq_table[ bg_left ] = 1
            else:
                bg_freq_table[ bg_left ] += 1

        """    

        n += 2


    for k in bg_freq_table.keys():

        bg_freq_table[ k ] = round( ( float( bg_freq_table[ k ] ) / float( source_len/2 ) ) * float( 100 ), 2 )
        #print( "hex dig: {0} ------> fq.: {1}".format( k, freq_table[ k ] ) )

    return bg_freq_table


def h_at( source ):

    h_frq_limits = [ 4.00, 6.00 ]
    th_frq_limits = [ 15, 17 ]
    he_frq_limits = [ 14, 15 ]
    t_frq_limits = [ 9.00, 11.00 ]
    e_frq_limits = [ 12.00, 14.00 ]

    src_len = len( source )

    hex_digits_fq_table = freq_table_of( source )


    possible_h_blocks = {}

    for hex_dig in hex_digits_fq_table.keys():
        
        if hex_digits_fq_table[ hex_dig ] > h_frq_limits[0] and hex_digits_fq_table[ hex_dig ] < h_frq_limits[1]: # get digits, FROM SOURCE, with the freq close to h's freq

            n = 0

            while n < src_len/2:

                # go thought source str looking for blocks of a[posible h] and [posible h]b; count em 

                if n > 3: # we can get "a" from a[hex_dig]
                        
                    if source[n-2] + source[n-1] + hex_dig is not possible_h_blocks.keys():    
                        possible_h_blocks[ source[n-2] + source[n-1] + hex_dig ] = 1
                    else:
                        possible_h_blocks[ source[n-2] + source[n-1] + hex_dig ] += 1

                if n < (src_len/2)-2: # we can get "b" from [hex_dig]b

                    if hex_dig + source[n+1] + source[n+2] is not possible_h_blocks.keys():    
                        possible_h_blocks[ hex_dig + source[n+1] + source[n+2] ] = 1
                    else:
                        possible_h_blocks[ hex_dig + source[n+1] + source[n+2] ] += 1
                        

                n += 2

    if len( possible_h_blocks ) == 0:
        print("no possible h block found for {0}% < h freq. < {1}%".format(h_frq_limits[0], h_frq_limits[1]))
        print("maybe you should broden the frq. interval limits")


    p_h_blocks_len = len( possible_h_blocks )


    for p_h_block in possible_h_blocks.keys(): # go through pair a[possible h] or [possible h]b

        # float freq. %

        float_frq_perc = round( ( float( possible_h_blocks[ p_h_block ] ) / float( p_h_blocks_len ) ) * float( 100 ), 2 )
        
        if th_frq_limits[0] < float_frq_perc and th_frq_limits[1] > float_frq_perc : 
            # if here   ---> a[possible h] 

            try:
                # check if p_h_block[:2] = t
            
                if hex_digits_fq_table[ p_h_block[:2] ] < 11 and hex_digits_fq_table[ p_h_block[:2] ] > 9:
                    
                    #IF HERE ---> pair th
                    print("beautiful, you've found the hidden th")
                    
                    # t ^ XOR = p_h_block[0]
                    # h ^ XOR = p_h_block[1]

                    continue

            except KeyError:
                print("no t, wrong guess pal")

        else:
            print("no possible th block found for {0}% < th freq. < {1}%".format( th_frq_limits[0], th_frq_limits[1] ))
            

        if he_frq_limits[0] < float_frq_perc and he_frq_limits[1] > float_frq_perc:
            # if 15 >   this pair fq   > 11   ---> [possible h]b ---> pair he

            try:

                if hex_digits_fq_table[ p_h_block[2:] ] > 12:
                        
                    #IF HERE ---> pair he
                    print("beautiful, you've found the hidden he")


            except KeyError:
                print("no e, wrong guess pal")

        else:

            print("no possible he block found for {0}% < he freq. < {1}%".format( he_frq_limits[0], he_frq_limits[1] ))


def reallocate_elms_on_list( l, n_s ):

    l_len = len( l )

    for n in range( n_s ):

        l.append( l[ l_len - (n_s - n) ] )

    for n in range( l_len ):

        l[ l_len-1-n ] = l[ l_len-2-n ]

    return l


def get_xor_btw(decimal1, decimal2):

    # xor throws 1 if and only if both bits're different
    return decimal1 ^ decimal2


def hex_str_to_dec( hex_str ):

    dec = 0
    n = 4
    str_len = len( hex_str )

    for strxdig in hex_str:
        # (len * 4) - (n += 4)
        dec = dec | clean_hex( strxdig ) << ( (str_len*4) - n )
        n += 4

    return dec
    



def most_fq_letters_at( encrypted_src ):

    len_enc_src = len( encrypted_src )

    hex_digits_fq_table = freq_table_of( encrypted_src )

    # list of higher to lower hex_digit by fq.

    hex_digits_fq_h_to_l = []

    higher_value_found = -1
    higher_hex_dig_of_the_cycle = ''

    last_hex_dig_fq = 0

    possible_key_fq = {}

    hex_digits_fq_table_keys = hex_digits_fq_table.keys()

    for cycle in range( len( hex_digits_fq_table ) ):


        for j in hex_digits_fq_table_keys:
            
            if  ( hex_digits_fq_table[ j ] >= higher_value_found ) and not( j in hex_digits_fq_h_to_l ):
                higher_value_found = hex_digits_fq_table[ j ]
                higher_hex_dig_of_the_cycle = j

        
        hex_digits_fq_h_to_l.append( higher_hex_dig_of_the_cycle )
        higher_value_found = -1


    # get xor of hex dig/ascii char in same possition on em lists
    # if it happens to have many count its fq.
    # if there are many possible keys is because some hex dig/ascii char in same possition on em lists does not match

    for n in range(len(eng_letters_fq_h_to_l)):

        possible_key = get_xor_btw( hex_str_to_dec( hex_digits_fq_h_to_l[1] ), int.from_bytes( eng_letters_fq_h_to_l[n].encode(), "big" ) )

        """
        print("btw {0} and {1}, possible key: {2}".format( hex_str_to_dec( hex_digits_fq_h_to_l[1] ), int.from_bytes( eng_letters_fq_h_to_l[n].encode(), "big" ), possible_key) )
        print("")
        print("possible dcy msg: ---------------------------------> ", decrypt_src( encrypted_src, possible_key ) )
        print("")
        
        """
        


    # if many possible keys, that with the higher fq. should be the key


    highest_val = -1
    most_fq_k = 0

    for k in possible_key_fq.keys():
        if  possible_key_fq[ k ] > highest_val:
            highest_val = possible_key_fq[ k ]
            most_fq_k = k

    


def decrypt_src( source, key ):

    len_enc_src = len( source )
    n = 0

    decrypted_msg = ''

    while n < len_enc_src:

        pair_hex_dig = source[n:n+2]

        # from dec to ascii char
        decrypted_msg += chr( hex_str_to_dec( pair_hex_dig ) ^ key )

        n += 2

    return decrypted_msg

    



decrypted_msg = most_fq_letters_at( "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736" )



        









        
