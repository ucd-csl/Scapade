import aspell

missing_targets_path = 'aspell_missing_targets.txt'
s = aspell.Speller('lang', 'en')

with open(missing_targets_path, 'r') as missing_targets:
    lines = missing_targets.read().splitlines()
    for word in lines:
        try:
            if not s.check(word):
                s.addtoPersonal(word)
        except:
            ''
s.saveAllwords()
