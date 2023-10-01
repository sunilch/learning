

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

# tensor preps
def make_input_output(num_lines=None):
    names_lines = load_raw_data()
    stoi, itos = str_encoders(names_lines)
    names_to_iter = names_lines[:num_lines] if num_lines else names_lines
    xs, ys = [], []
    for name in names_to_iter:
        name = '.' + name + '.'
        for fc, sc in zip(name, name[1:]):
            xi = stoi[fc]
            yi = stoi[sc]
            xs.append(xi)
            ys.append(yi)
    return torch.tensor(xs), torch.tensor(ys), stoi, itos




class BigramModel:
    
    @staticmethod
    def nll(likelihood):
        return -1*torch.log(likelihood)
    
    def __init__(self, xs, ys, stoi, itos) -> None:
        self.xs = xs
        self.ys = ys
        self.stoi = stoi
        self.itos = itos
        self.x_enc = F.one_hot(xs, num_classes=len(stoi)).float()
        self.g = torch.Generator().manual_seed(1234)
        self.W = torch.randn(len(self.stoi), len(self.stoi), generator=self.g, requires_grad=True)
        self.W.grad = None
        
    def forward(self):
        logits = self.x_enc @ self.W
        self.counts = logits.exp()
        self.probs = self.counts/self.counts.sum(1, keepdim=True)
        
    def loss(self):
        likelihood = self.probs[torch.arange(len(self.ys)), self.ys]
        return self.nll(likelihood=likelihood).mean()
        
    def step(self, lr):
        self.W.data -= lr*self.W.grad
        
    def run(self, iters, lr):
        losses = []
        for i in range(iters):
            self.W.grad = None
            self.forward()
            loss = self.loss()
            loss.backward()
            self.step(lr)
            losses.append(loss.item())
        return losses
    
    def sample(self, n_words):
        with torch.no_grad():
            names = []
            for i in range(n_words):
                curr_ind = self.stoi['.']
                name = ''
                while(True):
                    gen_ind = torch.multinomial(self.probs[curr_ind], num_samples=1).item()
                    if gen_ind == self.stoi['.']:
                        break
                    else:
                        name += self.itos[gen_ind]
                    curr_ind = gen_ind
                names.append(name)
        return names
                
        

if __name__=="__main__":
    xs , ys, stoi, itos = make_input_output()
    model = BigramModel(xs, ys, stoi, itos)
    losses = model.run(10, 0.1)
    print(losses)
    print("halt!")
    losses = model.run(10, 1)
    print(f"new losses are {losses}")
    print("halt!")
    losses = model.run(10, 10)
    print(f"new losses are {losses}")
    print("halt!")
    
    print(model.sample(5))
    print("stop!")
    