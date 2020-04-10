#!/usr/bin/env sh

str=$1
# edit this path to where the model rests in your file structure
model_path="/c/Users/robert/Documents/zeeko_nlp/nlp/g2p-seq2seq-master/g2p-seq2seq-model-6.2-cmudict-nostress"

g2p_path="../g2p_files/"
word_list_path="${g2p_path}${str}_word_list.txt"
output_path="${g2p_path}${str}_phonemes.txt"

g2p-seq2seq --decode $word_list_path --model_dir $model_path --output "$output_path"