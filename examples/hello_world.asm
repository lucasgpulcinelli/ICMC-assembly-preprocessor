; Hello World with Sugar!

; this program prints a "Hello, World" message in the middle of the screen
; with some characters around it for formatting

#define msg_len 13
msg: string "Hello, World!"


#define width_start_print $eval(sw//2-int(defs["msg_len"])//2-1)

#define starting_pos $position(width_start_print,eval(sh//2-1))


main:
    loadn r0, $position(0,eval(sh//2-1)); initial position for text
    loadn r1, $position(screen_width,eval(sh//2-1)); end of screen
    loadn r2, $starting_pos; start position of string
    loadn r3, $sum(starting_pos,msg_len); end position of string
    loadn r4, #msg; message
    ;r5 is the character to print

print_loop:
    cmp r0, r2
    jle load_hello_if1
    cmp r0, r3
    jeg load_hello_if2

    loadi r5, r4
    inc r4
    jmp main_endif
load_hello_if2:
    loadn r5, $green_lessthan
    jmp main_endif
load_hello_if1:
    loadn r5, $green_greaterthan
main_endif:
    outchar r5, r0
    inc r0
    cmp r0, r1
    jne print_loop

    halt
