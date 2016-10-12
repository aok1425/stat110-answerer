from pdf_miner import make_snippets, TextSnippet, open_document, find_question_page_num
from screenshotter import take_snapshots
import re

def make_question_snippets(snippets, question_num):
    """Given question_num, get the snippets (and their positions) for the pertaining snippets."""
    start_index = None
    end_index = None

    for i,s in enumerate(snippets):
        if s.text == '{}.\n'.format(question_num):
            start_index = i
            break

    if start_index is None:
        raise Exception("question_num not on page")

    for i,s in enumerate(snippets[start_index + 1:]):
        if bool(re.search(r'^\d+\.\n', s.text)):
            end_index = start_index + 1 + i
            break

    if end_index is None:
        end_index = -2
        # raise Exception("next question not found")

    return snippets[start_index:end_index + 1]

def make_sub_snippets(q_snippets):
    """Check if question snippets has sections (a), (b), (c), etc. If so, return list of them."""
    answer_start_index = None
    sections = []

    for i,s in enumerate(q_snippets):
        if s.text[:8] == 'Solution':
            answer_start_index = i
            break

    if answer_start_index is None:
        return q_snippets # means that there are no sections

    for i,s in enumerate(q_snippets[answer_start_index:]):
        if bool(re.search(r'^\([a-z]\)', s.text[:3])):
            sections.append(s)

    return q_snippets[:1] + sections + q_snippets[-1:]

def add_page_break_indices(sq):
    sq = sq.copy()
    page_break_indices = []
    correction_factor = 0 # bc .insert() changes the indices

    for i,_ in enumerate(sq):
        if i > 0 and sq[i].page > sq[i-1].page:
            page_break_indices.append(i)

    for j in page_break_indices:
        sq.insert(j + correction_factor, TextSnippet(None, sq[j + correction_factor].page - 1, 0, None, None))
        sq.insert(j + 1 + correction_factor, TextSnippet(None, sq[j + 1 + correction_factor].page, 792, None, None)) # TODO: don't hardcode this
        correction_factor += 2

    return sq

FILENAME = '/home/aok1425/Downloads/test_big.pdf'
CHAPTER = 1
QUESTION_NUM = 9
# FILENAME = '/home/aok1425/Downloads/test_big.pdf'

init = open_document(FILENAME)
starting_page = find_question_page_num(init, chapter=CHAPTER, question=QUESTION_NUM) # 11.4s
s = make_snippets(init, page_num=starting_page) # 2.2s
q = make_question_snippets(s, QUESTION_NUM)
sq = make_sub_snippets(q)
a = add_page_break_indices(sq)
take_snapshots(a, FILENAME) # 32.2s

# print(*[i.text for i in q])
print(*[i.text for i in s[:20]])
# print(*[i.text for i in sq])
print(*[i.text for i in a])

###

# take_snapshot(FILENAME, q_snippets[-1].start, q_snippets[0].start)
# take_snapshot(FILENAME, '/home/aok1425/Downloads/tempa.png', 576, 704)
# take_snapshot(FILENAME, sq[1].start, sq[0].start)
# take_snapshot(FILENAME, q[-1].start, q[0].start)