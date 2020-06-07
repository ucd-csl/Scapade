
file_path = '../g2p_files/cmu_missing_phonemes.txt'

with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    with open('cmu_missing_formatted.txt', 'a') as update_file:

        for line in lines:
            word = line.split()[0]
            phoneme = ' '.join(line.split()[1:])
            new_line = word + ',' + phoneme + ',1\n'
            update_file.write(new_line)