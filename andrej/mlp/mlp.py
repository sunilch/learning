
import torch
import torch.nn.functional as F 


def load_raw_data():
    input_dir = "/Users/schidara/repos/learningrepos/makemore/"
    names_file = "names.txt"
    with open(input_dir+names_file, "r") as f:
        names_lines = f.readlines()
    names_lines = [line.strip() for line in names_lines]
    return names_lines

# str to int encoders
def str_encoders(names_lines):
    chars = ['.']+sorted(list(set(''.join(names_lines))))
    stoi = {char:i for i, char in enumerate(chars)}
    itos = {i:s for s, i in stoi.items()}
    assert itos[stoi['j']]=='j'
    return stoi, itos
