from mrjob.job import MRJob
import re

class NGramsMapReduce(MRJob):
  regex = "^[A-Za-z+'-]+$"

  def mapper(self, _, line):
    values = line.split("\t")
    ngram = str(values[0])

    year = values[1]
    decade = year[0:3]

    occurrences = int(values[2])

    if re.match(self.regex, ngram) and year > 1900:
      yield ngram+"#"+decade, occurrences

  def reducer(self, ngramDecade, occurrences):
    yield ngramDecade, sum(occurrences)

if __name__ == '__main__':
    NGramsMapReduce.run()
