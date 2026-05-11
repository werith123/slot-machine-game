import random
import time

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

MAX_LINES  = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "@": 2,
    "#": 4,
    "$": 6,
    "%": 8
}

symbol_value = {
    "@": 5,
    "#": 4,
    "$": 3,
    "%": 2
}

ascii_art = r"""
                            .____                         .__  __  .__        ____.                            
                            |   _|   __  _  __ ___________|__|/  |_|  |__    |_   |                            
  ______   ______   ______  |  |     \ \/ \/ // __ \_  __ \  \   __\  |  \     |  |   ______   ______   ______ 
 /_____/  /_____/  /_____/  |  |      \     /\  ___/|  | \/  ||  | |   Y  \    |  |  /_____/  /_____/  /_____/ 
                            |  |_      \/\_/  \___  >__|  |__||__| |___|  /   _|  |                            
                            |____|                \/                    \/   |____|                         
"""

print(f"\033[32m{ascii_art}\033[0m")

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []

    for line in range(lines):
        symbol = columns[0][line]

        for column in columns:
            if symbol != column[line]:
                break
        else:
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)

    return winnings, winnings_lines     

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)

    columns = []

    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]

        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns      

def print_slot_machine(columns, winning_lines):
    for row in range(len(columns[0])):

        if (row + 1) in winning_lines:
            color = GREEN
        else:
            color = RED

        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(f"{color}{column[row]}{RESET}", end=" | ")
            else:
                print(f"{color}{column[row]}{RESET}", end="")

        print()

        # ⏳ animation delay per row
        time.sleep(row + 1)

def deposit():
    while True:
        amount = input(f"{YELLOW}what would you like to deposit? ${RESET}")

        if amount.isdigit():
            amount = int(amount)

            if amount > 0:
                break
            else:
                print(f"{RED}Amount must be greater then 0.{RESET}")
        else:
            print(f"{RED}Please enter a number.{RESET}")

    return amount      

def get_number_of_lines():
    while True:
        lines = input(f"{YELLOW}Enter the number of lines to bet on (1-{MAX_LINES})? {RESET}")

        if lines.isdigit():
            lines = int(lines)

            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f"{RED}Enter a valid number of lines{RESET}")
        else:
            print(f"{RED}Please enter a number.{RESET}")

    return lines

def get_bet():
    while True:
        amount = input(f"{YELLOW}what would you like to bet on each line? ${RESET}")

        if amount.isdigit():
            amount = int(amount)

            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"{RED}Amount must be between ${MIN_BET} - ${MAX_BET}.{RESET}")
        else:
            print(f"{RED}Please enter a number.{RESET}")

    return amount

def spin(balance):
    lines = get_number_of_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"{RED}You do not have that amount, your current amount is {balance}{RESET}")
        else:
            break    

    print(f"{YELLOW}you are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}{RESET}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    winnings, winnings_lines = check_winnings(slots, lines, bet, symbol_value)

    print_slot_machine(slots, winnings_lines)

    if winnings > 0:
        print(f"{GREEN}You won ${winnings}.{RESET}")
        print(f"{GREEN}you won on lines:{RESET}", *winnings_lines)
    else:
        print(f"{RED}You lost!{RESET}")

    return winnings - total_bet

def main():
    balance = deposit()
    start_balance = balance

    while True:
        if balance < start_balance:
            print(f"{RED}Current balance is ${balance}{RESET}")
        else:
            print(f"{GREEN}Current balance is ${balance}{RESET}")

        answer = input(f"{YELLOW}press enter to play(q to quit).{RESET}")

        if answer == "q":
            break

        balance += spin(balance)

    if balance < start_balance:
        print(f"{RED}You left with ${balance}{RESET}")
    else:
        print(f"{GREEN}You left with ${balance}{RESET}")

main()            
