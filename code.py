from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time
import keyboard
import pyautogui

def solve_sudoku(grid):
    '''
    0: represents empty squares
    1-9: numbers used by sudoku
    arrays indexed by n-1 (ie number 5 is index 4)
    '''
    
    
    # define 2D arrays to keep track whether each row/col/region needs number
    row = [[True] * 9 for i in range(9)]
    col = [[True] * 9 for i in range(9)]
    regions = [[True] * 9 for i in range(9)]
    
    
    # list of tuples containing coordinates of empty locations
    to_add = []
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # mark row/col/region as False, meaning we don't need that number anymore
                d = grid[i][j] - 1
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = False
            else:
                # need to find number of this spot
                to_add.append((i, j))
                
    def backtrack():
        if not to_add:
            # all squares full - we did it!
            return True
        
        # get next empty square
        i, j = to_add.pop()
        for d in range(9):
            # if number d can be legally inserted
            if row[i][d] and col[j][d] and regions[i // 3 * 3 + j // 3][d]:
                grid[i][j] = d + 1
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = False
                
                # try next empty spot
                if backtrack():
                    # success!
                    return True
                
                # backtrack failed, so reset and try next number
                grid[i][j] = 0
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = True
                
        # found no legal move - something went wrong in previous iterations!
        to_add.append((i, j))
        return False

    backtrack()
    
    
### let adblock work (if you know how to do this)
# path_to_adblock = r'C:\Users\mykyt\Desktop\YouTube\Videos\Videos\Sudoku\4.33.0_0'
# options = webdriver.ChromeOptions()
# options.add_argument('load-extension=' + path_to_adblock) 
# browser = webdriver.Chrome(ChromeDriverManager().install(), options = options)'''
browser = webdriver.Chrome(ChromeDriverManager().install())


### Puzzle Baron Sudoku Code
# get the page
'''browser.get("https://sudoku.puzzlebaron.com/init.php?d=e") # last letter is diffulty (e=easy, i=intense, etc)
default_delay = 1

# press 'q' to start game (to give me time to login, etc)
while True:
    if keyboard.is_pressed('q'):
        break
        
while True:
    # start competitive game
    start_button = browser.find_element_by_class_name("button_orange")
    start_button.click()
    time.sleep(default_delay)
    
    # read all numbers
    sudoku_table = browser.find_element_by_id("sudoku")
    numbers = []
    
    rows = sudoku_table.find_elements_by_css_selector('tr')
    for r in range(len(rows)):
        # %4 allows us to skip bold borders inside table, which are trs and tds for some reason
        if r % 4 == 0: continue
        row = rows[r]
        
        elements = row.find_elements_by_tag_name('td')
        
        for c in range(len(elements)):
            if c % 4 == 0: continue
            cell = elements[c]
            num = 0 if cell.text == '' else int(cell.text)
            numbers.append(num)
      
    unknown = [num == 0 for num in numbers]
    
    # reshape to 9x9 grid
    numbers = np.reshape(numbers, (9, 9))
    
    # solve and reshape to 1D again
    solve_sudoku(numbers)
    numbers = numbers.flatten()
    cur_idx = 0
    
    for r in range(len(rows)):
        if r % 4 == 0: continue
        row = rows[r]
        
        elements = row.find_elements_by_tag_name('td')
        for c in range(len(elements)):
            if c % 4 == 0: continue
        
            # skip element if known from given problem
            if not unknown[cur_idx]:
                cur_idx += 1
                continue
            
            # click elements and type correct number
            cell = elements[c]
            cell.click()
            keyboard.write(str(numbers[cur_idx]))
            cur_idx += 1
        
    # submit answer
    submit_button = browser.find_element_by_class_name("button_green")
    submit_button.click()
    time.sleep(default_delay)
    
    # play again
    again_button = browser.find_element_by_class_name("button_green")
    again_button.click()
    
    time.sleep(default_delay)
        
    # to halt program
    if keyboard.is_pressed('q'):
        break'''
   
        
# Elite Sudoku Code
browser.get("https://www.elitesudoku.com/")

# press 'q' to start game (to give me time to login, etc)
while True:
    if keyboard.is_pressed('q'):
        break

# start competitive game
start_button = browser.find_element_by_id("start-game")
start_button.click()

# read all numbers
cells = browser.find_elements_by_class_name("cell")
raw_numbers = []

for cell in cells:
    raw_numbers.append(0 if cell.get_attribute('value') == '' else int(cell.get_attribute('value')))
    
raw_numbers = np.reshape(raw_numbers, (9, 9))
numbers = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            numbers.extend(raw_numbers[3 * i + k][3 * j : 3 * j + 3])
numbers = np.reshape(numbers, (9, 9))

solve_sudoku(numbers)
solution_numbers = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            solution_numbers.extend(numbers[3 * i + k][3 * j : 3 * j + 3])
            
cur_idx = 0
for cell in cells:
    cell.click()
    
    # keyboard library doesn't work on this site
    pyautogui.write(str(solution_numbers[cur_idx]), _pause = False)
    cur_idx += 1

    