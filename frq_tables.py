import math

eng_letters_fq_h_to_l = [ "e",
        "t",
        "a",
        "o",
        "n",
        "r",
        "i",
        "s",
        "h",      
        "d",
        "l",
        "f",   
        "c",   
        "m",
        "u",
        "g",
        "y",
        "p",
        "w",
        "b",
        "v",
        "k",
        "x",
        "j",
        "q",
        "z"   ]


freq_table = {
        "e":13.11,
        "t":10.47,
        "a":8.15,
        "o":8.00,
        "n":7.10,
        "r":6.83,
        "i":6.35,
        "s":6.10,
        "h":5.26,      
        "d":3.79,
        "l":3.39,
        "f":2.92,   
        "c":2.76,   
        "m":2.54,
        "u":2.46,
        "g":1.99,
        "y":1.98,
        "p":1.97,
        "w":1.54,
        "b":1.44,
        "v":0.92,
        "k":0.42,
        "x":0.17,
        "j":0.13,
        "q":0.12,
        "z":0.08     
}

bigram_freq_table = {
        "th":16.8,
        "he":13.2,
        "an":0.92,
        "re":0.91,
        "er":0.88,
        "in":0.86,
        "on":0.71,
        "at":0.68,
        "nd":0.61,
        "st":0.53,
        "es":0.52,
        "en":0.51,
        "of":0.49,
        "te":0.46,
        "ed":0.45
}


def data_width( data ):

    max_val = data[ data.keys()[0] ] # set >= 0
    min_val = -1
    
    for k in data.keys():
        if data[ k ] > max_val:
            max_val = data[ k ]
        elif data[ k ] < min_val:
            min_val = data[ k ]

    return [ min_val, max_val ]
    
    


def dic_data_std_dev( data ):

    summation = 0.0

    for k in data.keys():
        summation += data[ k ]

    mean = summation / len( data )

    summation = 0.0

    for k in data.keys():
        summation += data[ k ]**2 - (2*mean*data[ k ]) + mean**2

    return round( math.sqrt( summation / (len( data ) - 1) ), 2 )

    

    
    
