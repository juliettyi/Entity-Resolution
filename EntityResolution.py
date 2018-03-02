#import libraries needed

import collections
import csv
import string

# constant: file names.
# Both files has the following columns, in the same order:
# column 0: id
# column 1: title
# column 2: authors
# column 3: venue
# column 4: year
# column 5: ROW_ID

F1='DBLP1.csv'
F2='Scholar.csv'



#remove puctuations in a string

remove_punctuation = str.maketrans('', '', string.punctuation)

def Normalize(orig):
  """ String Normalization.
  
    Lower case
    Remove excessive spaces

    Args:
      orig: string before normalization.

    Returns:
      normalized string.
  """
  r = orig.lower()
  # remove excessive spaces.
  return ' '.join(r.split())


def NormalizeTitle(orig_title):
  """ Title Normalization.
  
    call function Normalize to 
    -Lower case
    -Remove excessive spaces

    Remove punctuations

    Args:
      orig_title: title before normalization.

    Returns:
      normalized title.
  """
  title = Normalize(orig_title)
  # do not change n/a to na.
  if title == 'n/a':
    return title
  # remove punctuation
  title = title.translate(remove_punctuation)
  return title


# Known venue mapping
VENUE_MAP = {
  'proceedings of the international conference on very large hellip': 'vldb',
  'proceedings of the 25th international conference on very hellip': 'vldb',
  'proceedings of the 26th international conference on very hellip': 'vldb',
  'proceedings of the 27th international conference on very hellip': 'vldb',
  'proceedings of the acm sigmod international conference on hellip': 'sigmod conference',
  'proceedings of the 1995 acm sigmod international conference hellip': 'sigmod conference',
  'proceedings of the 1994 acm sigmod international conference hellip': 'sigmod conference',
  'proceedings of the 1996 acm sigmod international conference hellip': 'sigmod conference',
  'the vldb journal the international journal on very large hellip': 'vldb j',
  'acm transactions on database systems': 'acm transactions on database syst',
  'acm trans database syst': 'acm transactions on database syst',
  'acm sigmod record': 'sigmod record',
    
}

def NormalizeVenue(orig_venue):
  """Venue Normalization
     
      
     call function NormalizaTitle to
     -Lower case
     -Remove excessive spaces
     -Remove punctuations
         
     
  """
  
  venue = NormalizeTitle(orig_venue)
  if venue in VENUE_MAP:
    return VENUE_MAP[venue]
  return venue


def AuthorsToSet(authors):
  """Break a string of authors into set after normalizing the name.

    Args:
      authors: string of author names

    Returns:
      a set of normalized author names.

  """
  """
    Normalize each author's name to First Name initial + ' ' + Last Name
  """
  
  author_list = authors.lower().split(',')
  author_set = set()
  for author in author_list:
    if not author:
      continue
    name_parts = author.strip().split(' ')
    if len(name_parts) == 1:
      name = author
    else:
      name = name_parts[0][0] + ' '.join(name_parts[1:])
    if name:
      author_set.add(name)
  return author_set


def NormalizeAuthors(orig_authors):
  """ Author Normalization.
  
    Lower case
    Remove excessive spaces
    Split author list by comma, then
      for each author, take first letter of first name and keep last name.

    Args:
      orig_authors: authors before normalization.

    Returns:
      set() of authors after normalization
  """
  authors = Normalize(orig_authors)
  if not authors or authors == 'n/a':
    return None
  return AuthorsToSet(authors)


# define Entry object.
Entry = collections.namedtuple(
  'Entry',
  ['title_normalized', 'id', 'title', 'authors', 'venue', 'year', 'row_id'])


def RowToEntry(row, title_normalized):
  """ Convert a row into an entry.
  """
  return Entry(title_normalized=title_normalized,
               id=row[0],
               title=row[1],
               authors=NormalizeAuthors(row[2]),
               venue=NormalizeVenue(row[3]),
               year=Normalize(row[4]),
               row_id=row[5])


def ProcessFile(fn, content_map):
  """ Load a file into content_map.

    At the same time, print out most frequent authors, venue and year.

    Args:
      fn: name of file.
      content_map: map from normalized title to list of matched rows.
  """
  print("Processing", fn)
  authors_cnt = collections.Counter()
  venue_cnt = collections.Counter()
  year_cnt = collections.Counter()
  with open(fn, 'r', encoding='latin1') as f1:
    f1_reader = csv.reader(f1)
    # skip header
    header = next(f1_reader)
    for row in f1_reader:
      normalized_title = NormalizeTitle(row[1])
      if not normalized_title:
        continue
      content_map[normalized_title].append(RowToEntry(row, normalized_title))
      if row[2]:
        authors_cnt[row[2]] += 1
      if row[3]:
        venue_cnt[row[3]] += 1
      if row[4]:
        year_cnt[row[4]] += 1
  print(authors_cnt.most_common(10))
  print(venue_cnt.most_common(10))
  print(year_cnt.most_common(10))

#fuction to check if at lease one author matches
def MatchAuthors(authors1, authors2):
  """Returns True if authors1 and authors2 overlaps."""
  return len(set1 & set2) > 0


def MatchData(entry1, entry2):
  """ Matching two entries.

    After knowing that 2 entries has the same normalzied title,
    check whether authors, venue, year agrees.

    See Readme.md for detail.

    Args:
      entry1: entry from first file.
      entry2: entry from second file.

    Returns:
      if match, return the row [id1, id2], "pass"
      else return None, reject_reason
  """
  # Note authors is a set.
  if entry1.authors and entry2.authors:
    if len(entry1.authors & entry2.authors) == 0:
      print('Rejected because authors')
      print(entry1)
      print(entry2)
      print(entry1.authors & entry2.authors)
      l = ''
      for a in entry1.authors:
        l += a
        l += ','
      l += '|'
      for a in entry2.authors:
        l += a
        l += ','
      return None, 'author', l
  
  if entry1.venue and entry2.venue and entry1.venue != 'n/a' and entry2.venue != 'n/a':
    if entry1.venue != entry2.venue:
      print('Rejected because venue')
      print(entry1)
      print(entry2)
      return None, 'venue', '|'.join([entry1.venue, entry2.venue])
   
  if entry1.year and entry2.year and entry1.year != 'n/a' and entry2.year != 'n/a':
    if entry1.year != entry2.year:
      print('Rejected because year')
      print(entry1)
      print(entry2)
      return None, 'year', '|'.join([entry1.year, entry2.year])
    
  return [entry1.id, entry2.id, 
          entry1.row_id, entry2.row_id,
          '_'.join([entry1.row_id, entry2.row_id])], 'pass', ''


# use dictionary of list to hold all rows from each file
# the key is normalized title.
# the value is the list of rows under with the title.
f1_content = collections.defaultdict(list)
f2_content = collections.defaultdict(list)

ProcessFile(F1, f1_content)
ProcessFile(F2, f2_content)


# Print out counters as we go through the records.
print('# of keys:')
print(len(f1_content.keys()))
print(len(f2_content.keys()))

# Get counters by matching title only
f1_rows = 0
f2_rows = 0
f1_rows_in_f2 = 0
f2_rows_in_f1 = 0
f1_keys_in_f2 = 0
f2_keys_in_f1 = 0

for title in f1_content:
  f1_record_size = len(f1_content[title])
  f1_rows += f1_record_size
  if title in f2_content:
    f1_rows_in_f2 += f1_record_size
    f1_keys_in_f2 += 1

for title in f2_content:
  f2_record_size = len(f2_content[title])
  f2_rows += f2_record_size
  if title in f1_content:
    f2_rows_in_f1 += f2_record_size
    f2_keys_in_f1 += 1

print(f1_rows)
print(f2_rows)
print(f1_rows_in_f2)
print(f2_rows_in_f1)
print(f1_keys_in_f2)
print(f2_keys_in_f1)

num_output = 0
header_row=['idDBLP', 'idScholar', 'DBLP_Match', 'Scholar_Match', 'Match_ID']
reason_cnt = collections.Counter()
reject_cnt = collections.Counter()
with open('DBLP_Scholar_perfectMapping_YiChen.csv', 'w') as out_f:
  csv_writer = csv.writer(out_f)
  csv_writer.writerow(header_row)
  for title in f2_content:
    if title in f1_content:
      # found a title match, check further
      for f1_entry in f1_content[title]:
        for f2_entry in f2_content[title]:
          match_record, reason, reject_data = MatchData(f1_entry, f2_entry)
          if match_record:
            csv_writer.writerow(match_record)
            num_output +=1
          reason_cnt[reason] += 1
          if reject_data:
            reject_cnt[reject_data] += 1

print(num_output, 'rows in output')
print(reason_cnt.most_common(10))
print(reject_cnt.most_common(50))
