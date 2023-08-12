
class Bottle:
    
    def verse(self, num):
        if num == 98:
            return f"""2 bottles of beer on the wall, 2 bottles of beer.\nTake one down and pass it around, 1 bottle of beer on the wall."""
        elif num == 99:
            return f"1 bottle of beer on the wall, 1 bottle of beer.\nTake one down and pass it around, no more bottles of beer on the wall."
        elif num == 100:
            return f"No more bottles of beer on the wall, no more bottles of beer.\nGo to the store and buy some more, 99 bottles of beer on the wall."
        else:
            return f"{100-num} bottles of beer on the wall, {100-num} bottles of beer.\nTake one down and pass it around, {99-num} bottles of beer on the wall."
    
    def verses(self, start, end):
        all_lines = []
        for i in range(start, end+1):
            all_lines.append(self.verse(i))
        return "\n\n".join(all_lines)
    
    def song(self):
        return self.verses(0, 100)
    