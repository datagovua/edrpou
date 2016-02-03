# encoding=utf-8
import re,sys,itertools;

pages = re.compile('\f').split(sys.stdin.read().decode('utf-8'))

def transpose(list_of_lists):
  return list(itertools.izip_longest(*list_of_lists,fillvalue=' '))

def join_letters(letter_matrix):
  return ''.join(map(lambda x: ''.join(x).rstrip() + '\n', letter_matrix))

def pairwise(iterable):
  "s -> (s0,s1), (s2,s3), (s3, s4), ..."
  args = [iter(iterable)] * 2
  return itertools.izip(*args)

def join_cols(page):
  # find empty column of text
  # transpose page
  letter_matrix = map(list, page.splitlines())
  if not letter_matrix:
    return ''
  longest_length = max(map(len, letter_matrix))
  letter_matrix = map(lambda row: row + [u' ' * (longest_length - len(row))], letter_matrix)

  transposed_matrix = transpose(letter_matrix)
  # find row with all spaces
  last_empty_column = None
  for i,row in enumerate(transposed_matrix):
    if ''.join(row).isspace():
      last_empty_column = i
      break
  col1 = transposed_matrix[:last_empty_column]
  col2 = transposed_matrix[last_empty_column:]
  col1_text = join_letters(transpose(col1))
  col2_text = join_letters(transpose(col2))
  return col1_text + col2_text

joined_pages = "".join(map(join_cols, pages[1:-2]))


res = re.sub(u"\n\n(.*\n)?.* УПРАВЛІННЯ ЮСТИЦ(І|И)Ї\n.* ОБЛАСТІ", "", joined_pages)
res = re.sub(u"\n\n(.*\n)?.* УПРАВЛІННЯ ЮСТИЦ(І|И)Ї .*\n.*ОБЛАСТІ", "", res)
res = re.sub(u"\n\n.*\n.*УПРАВЛІННЯ ЮСТИЦ(І|И)Ї.*ОБЛАСТІ", "", res)
res = re.sub(u"\n\n.*УПРАВЛІННЯ\n.*ЮСТИЦІЇ", "", res)
res = re.sub(u"\n\n.*\n.*УПРАВЛІННЯ\n.*ЮСТИЦІЇ.*ОБЛАСТІ", "", res)
res = re.sub(u"\n\n.*\n.*\n.*УПРАВЛІННЯ.*ЮСТИЦІЇ.*У МІСТІ.*(\n\s+КИЄВІ)?", "", res)
res = re.sub(u"\n\n.*\n.*\n.*УПРАВЛІННЯ.*ЮСТИЦІЇ.*У М\.(\n\s+(?![0-9]+\.)*)?", "", res)

res = re.sub(u"\n\n.*ОБЛ\.", "", res)

without_eol = re.sub('\n', ' ', res)

print "\n".join(map(lambda x: x[0].strip() + ';' + x[1], pairwise(re.split("\s+(\d+?)\. (?:.*?)", without_eol, flags=re.DOTALL)[1:]))).encode('utf-8')
