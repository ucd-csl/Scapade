#!/usr/bin/env sh

source ~/Documents/zeeko_nlp/nlp/Scripts/activate

word_list_path="/c/Users/robert/Documents/zeeko_nlp/nlp/g2p-seq2seq-master/word_list.txt"
model_path="/c/Users/robert/Documents/zeeko_nlp/nlp/g2p-seq2seq-master/g2p-seq2seq-model-6.2-cmudict-nostress"
output_path="/c/Users/robert/Documents/zeeko_nlp/g2p_output/results.txt"

g2p-seq2seq --decode $word_list_path --model_dir $model_path --output "$output_path"
