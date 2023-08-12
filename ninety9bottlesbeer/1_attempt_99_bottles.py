
"""
99 bottles of beer on the wall, 99 bottles of beer.
Take one down and pass it around, 98 bottles of beer on the wall.

98 bottles of beer on the wall, 98 bottles of beer.
Take one down and pass it around, 97 bottles of beer on the wall.


...and so on, until it reaches 1 bottle.

Rules:

- The lyrics are case-sensitive; make sure to match the exact capitalization.
- Pay attention to singular and plural forms ("1 bottle" vs. "2 bottles").
- The last verse should end with "1 bottle of beer on the wall" (singular form).
"""

# My solution:

def bottles_of_beer(num):
    return f"{num} bottles of beer" if num > 1 else f"{num} bottle of beer"

def on_the_wall():
    return f"on the wall"

def take_down():
    return f"Take one down and pass it around"

def main():
    all_lines = []
    for i in range(99, 1, -1):
        first_line = bottles_of_beer(i)+" "+on_the_wall() + ", " + bottles_of_beer(i) + "."
        second_line = take_down() + ', ' + bottles_of_beer(i-1) + " " + on_the_wall() + "."
        all_lines.append(first_line)
        all_lines.append(second_line)
    return "\n".join(all_lines)

print(main())