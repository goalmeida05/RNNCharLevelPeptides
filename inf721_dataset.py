# -*- coding: utf-8 -*-
"""INF721_Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jDTJqKIgfDsdQcnadCKP7H8jU0CjY2B5
"""

import torch
import sys
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

#------------------------------------------------------------------------------#
#----------------------------Definição do DataSet------------------------------#
#------------------------------------------------------------------------------#
class PeptideosDataset(Dataset):
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_text = file.read()

        self.vocab = sorted(set(self.raw_text + ' []'))
        self.ch2ix = {ch: ix for ix, ch in enumerate(self.vocab)}
        self.ix2ch = {ix: ch for ix, ch in enumerate(self.vocab)}

        self.sequences = self.raw_text.split('\n')
        self.max_len = max(len(seq) for seq in self.sequences)

    def one_hot_encode(self, ix):
      one_hot = torch.zeros(len(self.vocab))
      one_hot[ix] = 1.0
      return one_hot

    def encode(self, seq_ch):
      return torch.stack([self.one_hot_encode(self.ch2ix[ch]) for ch in seq_ch])

    def decode(self, seq_ix):
      return ''.join(self.ix2ch[ix] for ix in seq_ix)

    def __len__(self):
      return len(self.sequences)

    def __getitem__(self, index):
      seq_ch = self.sequences[index]

      pad_len = self.max_len - len(seq_ch)
      seq_ch = '[' + seq_ch + ']' + ' ' * pad_len

      x = seq_ch[:-1]
      y = [self.ch2ix[ch] for ch in seq_ch[1:]]

      x_encoded = self.encode(x)
      y_tensor = torch.tensor(y, dtype=torch.long)

      return x_encoded, y_tensor

    @property
    def vocab_size(self):
	    return len(self.vocab)
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
#--------Verificando se o arquivo está sendo processado corretamente-----------#
#------------------------------------------------------------------------------#
text_dataset = PeptideosDataset('Dados.txt')
x, y = text_dataset[0]
print("Tamanho do vocabulário:", text_dataset.vocab_size)
print("Número de peptídeos:", len(text_dataset))
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#



#------------------------------------------------------------------------------#
#---------------------------Criação do DataLoader------------------------------#
#------------------------------------------------------------------------------#
train_loader = DataLoader(text_dataset,
                          batch_size=32,
                          shuffle=True, drop_last=True)
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#