#!/usr/bin/env python3
import sys
import os

# Var syntax:
    # Array: starts with [ and ends with ]
    #   array_name = [1,2,3,4,5]

    # String: starts with " and ends with \"
    #   string_name = "   test      -=+&4%12#@,./'    $colorSomethingWithColor\$     
    #         test2     test3 <>;'`"`                   
    #        blablabla             1234567890                   \"


# ***************** DONT TRY TO PRINT \" OR \$ *****************


# Input and output archives
if len(sys.argv) < 3:
    print(f"Error, use {sys.argv[0]} input.vars output.asm", file=sys.stderr)
inp = open(sys.argv[1], "r")
out = open(sys.argv[2], "w")

# Replace special chars
special_chars = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
                '@', '[', '\\', ']', '^', '_', '`', '{', '|', ']', '~']
subst_chars = ["space","exclamation","doublequote","hashtag","dollar","percent","ampersand","singlequote",
                "openpar","closepar","asterisk","plus","comma","minus","dot","slash","colon","semicolon","lessthan",
                "equal","greaterthan","questionmark","at","opensquareb","backslash","closesquareb","caret","underscore",
                "graveaccent","openbrackets","vslash","closebrackets","tilda"]

# Store input archive in text
text = inp.read()
cur_pos = 0

# Print with color
# Syntax: starts with $ and ends with \$ 
#   $colorSomething\$
# color : 2 letters
def print_color(char, color):
    colors = ["white", "darkred", "green", "mossgreen", "darkblue", "purple", "cyan", "lightgray", "grey", "red", "grassgreen", "yellow", "blue", "pink", "poolgreen", "black"]
    array = ["wh", "dr", "ge", "mg", "db", "pu", "cy", "lg", "gy", "re", "gg", "ye", "bl", "pk", "pg", "bk"]
    if color in array:
        count = 0
        for i in array:
            if i == color:
                pos = count
            else:
                count += 1
        # Verufy special chars
        try:
            value_index = special_chars.index(char)
        except:
            value_index = -1

        if value_index != -1:
            out.write("${}_{}\n".format(colors[pos],subst_chars[value_index]))
        else:
            out.write("${}_{}\n".format(colors[pos],char))
        return
    else:
        print("Cor errada")
        inp.close()
        out.close()
        os.remove(sys.argv[2])
        sys.exit(-1)

# Read input archive
while cur_pos < len(text):
    
    # Var
    equal_pos = text.find("=", cur_pos)
    if equal_pos == -1:
        break
    var = text[cur_pos:equal_pos]
    var = var.strip()

    cur_pos = equal_pos + 1
    
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
                    print_color(text[cur_pos],color)
                    i += 1
                    cur_pos += 1
                cur_pos = dollar_pos + 1
            else:
                out.write("\tstatic {} + #{}, ".format(var, i))
                print_color(text[cur_pos],"wh")
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