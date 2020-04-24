import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# Letters variable for the entire alphabet.
letters = 'abcdefghijklmnopqrstuvwxyz'

# Create the dict to use to store the 
# counts for the individual letters of the alphabet.
letters_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0,\
'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, \
'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, \
'w': 0, 'x': 0, 'y': 0, 'z': 0}


# There are several defines below, the first one is to calculate the
# probability of a letter appearing in the book. It returns each percentage
# of the letter in question passed into the function.
def percent_of(ltr_ky,ltr_cnts):
    prct_of = ltr_cnts[ltr_ky]*100/sum(ltr_cnts.values())
    return prct_of

# This second define is to populate a blank dictionary with the probability
# of each letter appearing in the book, calling the previous define to
# calculate for each letter. It returns a new dictionary of percetages
# of each letter.    
def pop_perct(ltrs_counts):    
    perct = {}
    for ch in ltrs_counts:
        perct.update({ch.upper():percent_of(ch,ltrs_counts)})
    return perct

# This third define is to graph the actual probabilities of the book, which
# first passes the dict of all letter counts into the pop_perct define. 
# The x and y values are determined and graphed with the y_maximum being just
# a bit higher than the highest value. Finally, the y-axis is formatted, 
# the graph is titled, the x axis labeled. Then the define goes into an if
# else loop; in the first option the graph is shown to the viewer and
# in the second option the graph is saved into the same directory as the app
# before being closed.
def Graph_the_book(ltrs_counts,opt):
    percent = pop_perct(ltrs_counts)
        
    x_values = np.arange(len(percent))
    plt.bar(x_values, list(percent.values()), align = 'center', width= 0.7)
    plt.xticks(x_values,percent.keys())
    y_max = max(percent.values())+ 1
    plt.ylim(0, y_max)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:g} %'))
    plt.title('Percentage of Each Letter\'s Appearance in \n{}\'s {}' .format(bk_author,bk_title), fontsize=12)
    plt.xlabel('Letters of the Alphabet')
    if opt == 1:
        plt.show()
    else:
        plt.savefig('Graph of {}.png'.format(bk_title), dpi = 150)
        plt.cla()
        plt.clf()
        plt.close()
        

# Fourth define is to get the novel title or author of the novel chosen,
# it passes the raw book text and the choice of author or title as 'string.'
def Get_title_or_author(bk_txt,string):
    for i in range(15):
        mod_book_text = bk_txt.split('\n')
        if mod_book_text[i].find(string) == 0:
            temp = mod_book_text[i]
            item = temp[len(string)+1:].title().strip() 
    return(item)

# Last but not least, the fifth define is to get the correct text based on user
# selection. it returns a dictionary of all letter counts, and gets the book
# title and author, by calling the previous define.
def Get_text(bk_chc,ltrs_cnts):
    if bk_chc == 'a':
        bookURL = 'http://www.gutenberg.org/cache/epub/21839/pg21839.txt'
    elif bk_chc == 'b':
        bookURL = 'https://www.gutenberg.org/files/84/84-0.txt'
    elif bk_chc == 'c':
        bookURL = 'https://www.gutenberg.org/files/996/996-0.txt'
    elif bk_chc == 'd':
        bookURL = 'https://www.gutenberg.org/files/1661/1661-0.txt'
    elif bk_chc == 'e':
        bookURL = input('\n  Paste a Gutenberg Plain Text Novel URL: ').strip()
        print('  Please hold while we\'re getting your book...')
    else:
        print('\n  wrong entry, we'' stay with Sense and Sensibility!')
        bookURL = 'http://www.gutenberg.org/cache/epub/21839/pg21839.txt'

    
    # Get the raw text for the novel in question as a request from the website.
    response = requests.get(bookURL)

    # Make sure the requested data is all in lower case.
    book_text = response.text.lower()
    
    # Call the previous define to get the titel or author, passing in a portion of 
    # the book and the 'title: ' or 'author: ' as search term.
    _title = Get_title_or_author(book_text[0:700],'title:')
    _author = Get_title_or_author(book_text[0:700],'author:')
    
    # A loop to search through text and populate the lts_cnts
    # dictionary with a count for each letter.
    for ch in book_text:
        if ch in ltrs_cnts:
            ltrs_cnts[ch] += 1
    return (ltrs_cnts,_title,_author)


# Setting the flags for catching improper user entry 
flag1 = False
flag2 = False

# Typing out how the menus would look.
book_menu = '''
    a. Sense and Sensibility by Jane Austen.
    b. Frankestine by Mary Wollstonecraft (Godwin) Shelly.
    c. The History of Don Quixote by Miguel de Cervantes.
    d. The Adventures of Sherlock Holmes by Arther Canon Doyle.
    e. Gutenberg novel of your choice!
'''
menu = '''
   1. Probability of a single letter in novel.
   2. Graph of Probability of all letters in the novel.
   3. Save the Graph of Probability in same directory as this app. 
   4. Quit.
'''

# Display the header and first menu on the users end.
print('\n'+' Welcome to Graph a Novel! '.center(70,'='))
print('\n'+' Please select a novel '.center(70,'-'))
print(book_menu)

# first while loop to get the book text based on user selection
# asking users to hold while the program does so for the first four
# options. With the last option, the hold message is displayed 
# within the Get_text define. In all cases of selections a, b , c, d
# and e. The empty letters_counts dictionary gets filled, and so too
# are the book title and book author assigned. If the user enters in
# a wrong selection- the while loop will prompt them again until
# they select a, b, c, d, or e and then set the first flag as true to
# exit the loop
while not flag1:
    book_choice = input('\n\tYour book selection? ').strip().lower()
    if book_choice == 'a' or book_choice == 'b'or book_choice == 'c' or book_choice == 'd' :
        print('\t Please hold while we get your book...')
        letters_counts, bk_title, bk_author = Get_text(book_choice,letters_counts)
        flag1 = True
    elif book_choice == 'e':
        letters_counts, bk_title, bk_author = Get_text(book_choice,letters_counts)
        flag1 = True
    else:
        print('\n'+'Sorry that is an incorrect selection, please try again!'.center(70,'*'))


# print a thank you message for waiting for book selection. Displays
# the second menu of options to chose from.
print('\n'+'Thanks for waiting! Select an option below '.center(70,'-'))
print(menu)
print('-'*70)

# Starting the second while loop asking for user input based on second menu selection.
# There is similar while loop structure as before, wrong entry will loop back to asking
# for a selection. selection 1 calculates the probability of a letter selected for the 
# book selected. Option two and three call on the Graph_the_book define to graph it,
# though with option 3, the graph isn't shown to the viewer. Option four is the option
# to quit, which thanks the user for their use and exits the loop.
while not flag2:
    menu_selection = input('\n\tYour selection? ')

    if menu_selection == '1':
        ltr_key =input('\n Which letter do you wish to find the probability of? ').strip().lower()            

        print('\n   Count for all letters is {}.'.format(sum(letters_counts.values())))
        print('   Count for letter \'{}\' is {}.'.format(ltr_key,letters_counts[ltr_key]))
        print('\n   The probability of letter {} appearing in {}\'s'\
              .format(ltr_key,bk_author) + '\n   {} is %{:.2f}'.format(bk_title,percent_of(ltr_key,letters_counts)))
    elif menu_selection == '2':
        Graph_the_book(letters_counts,1)
     
    elif menu_selection == '3':
        Graph_the_book(letters_counts,0)
        
    elif menu_selection == '4':          
        flag2 = True
        print('\n'+'Thanks for using this \'Graph a Novel!\' program!'.center(70,'='))
        
    else:
        print('\n'+'Sorry that is an incorrect selection, please try again!'.center(70,'*'))
