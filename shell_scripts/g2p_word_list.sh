#!/usr/bin/env sh

source ~/Documents/zeeko_nlp/nlp/Scripts/activate

str=$1
model_path="/c/Users/robert/Documents/zeeko_nlp/nlp/g2p-seq2seq-master/g2p-seq2seq-model-6.2-cmudict-nostress"

if [ "$str" == "birkbeck" ]; then
  word_list_path="/c/Users/robert/Documents/zeeko_nlp/g2p_files/birkbeck_word_list.txt"
  output_path="/c/Users/robert/Documents/zeeko_nlp/g2p_files/birkbeck_phonemes.txt"
elif [ "$str" == "holbrook" ]; then
  word_list_path="/c/Users/robert/Documents/zeeko_nlp/g2p_files/holbrook_word_list.txt"
  output_path="/c/Users/robert/Documents/zeeko_nlp/g2p_files/holbrook_phonemes.txt"
fi
g2p-seq2seq --decode $word_list_path --model_dir $model_path --output "$output_path"