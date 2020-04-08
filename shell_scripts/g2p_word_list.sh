#!/usr/bin/env sh

str=$1
# edit this path to where the model rests in your file structure
model_path="/c/Users/robert/Documents/zeeko_nlp/nlp/g2p-seq2seq-master/g2p-seq2seq-model-6.2-cmudict-nostress"

if [ "$str" == "birkbeck" ]; then
  word_list_path="../g2p_files/birkbeck_word_list.txt"
  output_path="../g2p_files/birkbeck_phonemes.txt"
elif [ "$str" == "holbrook" ]; then
  word_list_path="../g2p_files/holbrook_word_list.txt"
  output_path="../g2p_files/holbrook_phonemes.txt"
elif [  "$str" == "zeeko" ]; then
  word_list_path="../g2p_files/zeeko_word_list.txt"
  output_path="../g2p_files/zeeko_phonemes.txt"
elif [ "$str" == "aspell" ]; then
  word_list_path="../g2p_files/aspell_word_list.txt"
  output_path="../g2p_files/aspell_phonemes.txt"
elif [ "$str" == "wiki" ]; then
  word_list_path="../g2p_files/wiki_word_list.txt"
  output_path="../g2p_files/wiki_phonemes.txt"
fi

g2p-seq2seq --decode $word_list_path --model_dir $model_path --output "$output_path"