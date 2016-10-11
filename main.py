from pdf_miner import make_snippets, find_page_num
from screenshotter import take_snapshot
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

FILENAME = '/home/aok1425/Downloads/test.pdf'
# FILENAME = '/home/aok1425/Downloads/test_big.pdf'

s = make_snippets(FILENAME, page_num=None)
# q = make_question_snippets(s, 31)
# sq = make_sub_snippets(q)

# take_snapshot(FILENAME, q_snippets[-1].start, q_snippets[0].start)
# take_snapshot(FILENAME, 513, 566)
# take_snapshot(FILENAME, sq[1].start, sq[0].start)
# take_snapshot(FILENAME, q[-1].start, q[0].start)


# get_sub_snippets(q)
# print(*[i.text for i in q])
# print(*[i.text for i in s])