# decode a string which has been encode by XORing against a single character


import sys

sys.path.insert( 1, '#' ) # frq_tables path

from frq_tables import freq_table, bigram_freq_table, dic_data_std_dev, eng_letters_fq_h_to_l


def clean_hex( hex_num ):

    clean_hex_num = 0

    _dict = {
        'A':10,
        'a':10,
        'B':11,
        'b':11,
        'C':12,
        'c':12,
        'D':13,
        'd':13,
        'E':14,
        'e':14,
        'F':15,
        'f':15
        }

    try:
        clean_hex_num = _dict[ hex_num ]
    except KeyError:
        clean_hex_num = int( hex_num )

    return clean_hex_num



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

        n += 2


    for k in bg_freq_table.keys():

        bg_freq_table[ k ] = round( ( float( bg_freq_table[ k ] ) / float( source_len/2 ) ) * float( 100 ), 2 )
        #print( "hex dig: {0} ------> fq.: {1}".format( k, freq_table[ k ] ) )

    return bg_freq_table


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

     
