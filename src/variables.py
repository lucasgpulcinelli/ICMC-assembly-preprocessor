#!/usr/bin/env python3
import sys
import os

# Replace special chars
special_chars = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
                 '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', ']', '~']
subst_chars = ["space","exclamation","doublequote","hashtag","dollar","percent","ampersand","singlequote",
                "openpar","closepar","asterisk","plus","comma","minus","dot","slash","colon","semicolon","lessthan",
                "equal","greaterthan","questionmark","at","opensquareb","backslash","closesquareb","caret","underscore",
                "graveaccent","openbrackets","vslash","closebrackets","tilda"]

def print_with_color(char, color):
    '''
    print_with_color compares the color provided in the function input with the array with the color abbreviations
    and prints in the output file the char with the color format: $char_color

    To print something in this format, the substring in the input file must be like: "... $colorSomethingWithColor\$...\"
    with color being one of the abbreviations in the array below

    Example of output: First letter of "var_name" (char = a, color = white)
        static var_name + #0, $white_a
    '''

    colors = ["white", "darkred", "green", "mossgreen", "darkblue", "purple", "cyan", "lightgray", "grey", "red",
              "grassgreen", "yellow", "blue", "pink", "poolgreen", "black"]
    abbreviations = ["wh", "dr", "ge", "mg", "db", "pu", "cy", "lg", "gy", "re", "gg", "ye", "bl", "pk", "pg", "bk"]
    
    # Search color position in colors array
    if color in abbreviations:
        count = 0
        for i in abbreviations:
            if i == color:
                color_pos = count
            else:
                count += 1
        # Verify if char is a special character
        try:
            value_index = special_chars.index(char)
        except:
            value_index = -1
        # Print char with the color format
        if value_index != -1:
            out.write("${}_{}\n".format(colors[color_pos],subst_chars[value_index]))
        else:
            out.write("${}_{}\n".format(colors[color_pos],char))
        return
    else:
        print("Wrong color")
        inp.close()
        out.close()
        os.remove(sys.argv[2])
        sys.exit(-1)

def read_var_name(text, cur_pos):
    '''
    read_var_name defines the variable name and returns it as a string. Also returns the positon after the equal sign.
    '''
    # Finds the next equal sign and defines the substring before it as the variable
    equal_pos = text.find("=", cur_pos)
    if equal_pos == -1: # TRATAR ESTE ERRO DE MANEIRA DECENTE
        return "error", -1
    var = text[cur_pos:equal_pos].strip()
    return var, (equal_pos + 1)


def read_input_file(input_fle):
    '''
    read_input_file reads all the input file, defines the variables, their lenght and uses the print_with_color function
    to print in the output file all the variables provided, with the following format:
    
    # COLOCAR OS EXEMPLOS EM UM ARQUIVO .VARS SEPARADO

    Numeric Arrays:         
        Example:
        
            Input file:     array = [12, 23,..., 47]    (10 numbers)
    
            Output file:    #define array_len 10
                            array : var #10
	                            static array + #0, #12
	                            static array + #1, #23
	                            ...
	                            static array + #9, #47

    Strings:
        Example:

            Input file:     something = "abc...$dbHello\$
                            ...xz\"
            
            Output file:    #define something_len 25
                            something : var #25
	                            static something + #0, $white_a
	                            static something + #1, $white_b
	                            static something + #2, $white_c
	                            ...
	                            static something + #10, $darkblue_H
	                            static something + #11, $darkblue_e
	                            static something + #12, $darkblue_l
	                            static something + #13, $darkblue_l
	                            static something + #14, $darkblue_o
	                            static something + #15, #'\n'
                                ...
                                static something + #, $white_x
	                            static something + #, $white_z
	                            static something + #24, #'\0'
    '''
    # Current position at input file
    cur_pos = 0

    # Read input archive
    while cur_pos < len(text):

        var, cur_pos = read_var_name(text, cur_pos)
        # MUDAR ISSO PARA UM ERRO NA FUNCAO
        if cur_pos == -1:
            break

        while (text[cur_pos] != '"') and (text[cur_pos] != '['):
            cur_pos += 1

        # Array
        if text[cur_pos] == '[':
            bracket_pos = text.find("]", cur_pos)
            array = text[cur_pos+1:bracket_pos]
            array = array.split(",")
            array = [int(e) for e in array]

            size_array = len(array)

            cur_pos = bracket_pos + 1

            # Print define array
            out.write("#define {}_len {}\n".format(var, size_array))
            # Print array name and size
            out.write("{} : var #{}\n".format(var, size_array))

            # Print array
            i = 0
            while i < size_array:
                out.write("\tstatic {} + #{}, #{}\n".format(var, i, array[i]))
                i += 1

            if cur_pos >= len(text):
                 break

            while text[cur_pos] == ' ' or text[cur_pos] == '\n':
                cur_pos += 1
                if cur_pos >= len(text):
                    break
            continue
        
        # String
        elif text[cur_pos] == '"':
            size_string = 0
            quot_pos = cur_pos
            loop = 1
            # Find string end
            while loop:
                quot_pos = text.find('"', quot_pos + 1)
                if text[quot_pos-1] != '\\':
                    quot_pos += 1
                    continue
                else:
                    loop = 0
            # String size
            count = 0
            j = cur_pos+1
            while j < quot_pos-1:
                if text[j] == '$' and text[j-1] == '\\':
                    count += 1
                j += 1
            size_string = (quot_pos-1) - cur_pos - 5*(count)
            cur_pos += 1

            # Print string define
            out.write("#define {}_len {}\n".format(var, size_string))
            # Print string size
            out.write("{} : var #{}\n".format(var, size_string))

            # Find string end and print string
            i = 0
            while i < size_string-1:
                # \n
                if text[cur_pos] == '\n':
                    out.write("\tstatic {} + #{}, #'\\n'\n".format(var, i))
                    i += 1
                    cur_pos += 1
                    continue
                # Colors
                if text[cur_pos] == '$':
                    dollar_pos = cur_pos
                    loop = 1
                    # Find color end
                    while loop:
                        dollar_pos = text.find('$', dollar_pos + 1)
                        if text[dollar_pos-1] != '\\':
                            dollar_pos += 1
                            continue
                        else:
                            loop = 0

                    color = text[cur_pos+1:cur_pos+3]
                    cur_pos += 3
                    # Print string with colors
                    while cur_pos < dollar_pos-1:
                        out.write("\tstatic {} + #{}, ".format(var, i))
                        print_with_color(text[cur_pos],color)
                        i += 1
                        cur_pos += 1
                    cur_pos = dollar_pos + 1
                else:
                    out.write("\tstatic {} + #{}, ".format(var, i))
                    print_with_color(text[cur_pos],"wh")
                    i += 1
                    cur_pos += 1

            # \0    
            out.write("\tstatic {} + #{}, #'\\0'\n".format(var, i))
            cur_pos = quot_pos
            cur_pos += 1

            if cur_pos >= len(text):
                 break

            while text[cur_pos] == ' ' or text[cur_pos] == '\n':
                cur_pos += 1
                if cur_pos >= len(text):
                    break
            continue
        cur_pos += 1

    inp.close()
    out.close()


if __name__ == "__main__":
    # Input and output archives
    if len(sys.argv) < 3:
        print(f"Error, use {sys.argv[0]} input.vars output.asm", file=sys.stderr)
    inp = open(sys.argv[1], "r")
    out = open(sys.argv[2], "w")
    
    # Store input archive in text
    text = inp.read()
    
    read_input_file(text)

    