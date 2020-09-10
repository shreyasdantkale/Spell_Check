from Levenshtein import distance as levenshtein_distance

DEL_WORDS = {}
DEL_WORDS_2 = {}

## Calculate probability
def get_probability(WORDS):
    words_sum = sum(WORDS.values())
    for w in WORDS.keys():
        WORDS[w] = WORDS[w]/words_sum
    return WORDS

WORDS = get_probability(WORDS)
WORDS = {k: v for k, v in sorted(WORDS.items(), key=lambda item: item[1], reverse = True)}

## compute 1 char deletion words
def e1(word, vowel = False):
    splits = [(word[:i], word[i:])    for i in range(1, len(word) +1)]
    deletes = [L + R[1:]              for L, R in splits if R and (not vowel or (vowel and R[0] in ("aeiou") + (R[0] if L[-1] not in "aeoiu" and L[-1]==R[0] else '')))]
    return deletes

## for second edit we will reomve only vowels and repeated chars
def e2(word, vowel = True):
    words_2 = []
    words_1 = e1(word)
    words_2.extend(words_1)
    for w in words_1:
        words_2.extend(e1(w, vowel))
    return words_2

## generate dictionary for storing deletion words 
def del_dict(WORDS, e):
    DEL_WORDS = {}
    for word in WORDS.keys():
        all_alt = e(word)
        ## add all 1 delete words as key and correct word as value
        for alt in all_alt:
            if DEL_WORDS.get(alt):
                if word not in DEL_WORDS[alt]:
                    DEL_WORDS[alt].append(word)
            else:
                DEL_WORDS[alt] = [word]
    return DEL_WORDS

## find most suited words from candidates with probability of word
def P(word):
    return WORDS.get(word, 0)

## Most probable spelling correction for word
def correction(word): 
    correction_word = max(candidates(word), key=P)
    if (levenshtein_distance(word, correction_word) < 3):
        return correction_word
    else:
        return word

## look for candidate words
def candidates(word):
    if len(word)<=4:
        return (known([word]) or known(candidate_words(word, 1)) or [word])
    else:
        return (known([word]) or known(candidate_words(word, 1)) or (known(candidate_words(word, 2))) or [word])

## "The subset of `words` that appear in the dictionary of WORDS."
def known(words): 
    return set(w for w in words if w in WORDS)

## compare all candidate words
def candidate_words(word, edit_dist = 1):
    all_candidates = []
    if edit_dist == 1:
        del_w = e1(word)
        DEL_WORDS = DEL_WORDS_1
    else:
        del_w = e2(word)
        DEL_WORDS = DEL_WORDS_2

    insert_w = DEL_WORDS.get(word, [])
    delete_w = [w for w in del_w if WORDS.get(w)]
    transition_replace_w = [cand for w in del_w if DEL_WORDS.get(w) for cand in DEL_WORDS[w]]

    all_candidates.extend(insert_w)
    all_candidates.extend(delete_w)
    all_candidates.extend(transition_replace_w)

    # print(all_candidates)
    return all_candidates

DEL_WORDS_1 = del_dict(WORDS, e1)
DEL_WORDS_2 = del_dict(WORDS, e2)
