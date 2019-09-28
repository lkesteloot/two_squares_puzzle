# Copyright 2019 Lawrence Kesteloot
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://www.futilitycloset.com/2019/09/28/the-two-squares-puzzle/

import sys, random

# Use "NO" for zero so that we don't introduce the "Z" letter. It hasn't
# shown up in any cycles to date.
NUMBER_NAMES = [
    "NO", "ONE", "TWO", "THREE", "FOUR",
    "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
    "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN",
    "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN",
    "TWENTY", "TWENTY-ONE", "TWENTY-TWO", "TWENTY-THREE", "TWENTY-FOUR",
    "TWENTY-FIVE", "TWENTY-SIX", "TWENTY-SEVEN", "TWENTY-EIGHT", "TWENTY-NINE",
    "THIRTY", "THIRTY-ONE", "THIRTY-TWO", "THIRTY-THREE", "THIRTY-FOUR",
    "THIRTY-FIVE", "THIRTY-SIX", "THIRTY-SEVEN", "THIRTY-EIGHT", "THIRTY-NINE",
    "FORTY", "FORTY-ONE", "FORTY-TWO", "FORTY-THREE", "FORTY-FOUR",
    "FORTY-FIVE", "FORTY-SIX", "FORTY-SEVEN", "FORTY-EIGHT", "FORTY-NINE",
    "FIFTY", "FIFTY-ONE", "FIFTY-TWO", "FIFTY-THREE", "FIFTY-FOUR",
    "FIFTY-FIVE", "FIFTY-SIX", "FIFTY-SEVEN", "FIFTY-EIGHT", "FIFTY-NINE",
    "SIXTY", "SIXTY-ONE", "SIXTY-TWO", "SIXTY-THREE", "SIXTY-FOUR",
    "SIXTY-FIVE", "SIXTY-SIX", "SIXTY-SEVEN", "SIXTY-EIGHT", "SIXTY-NINE",
    "SEVENTY", "SEVENTY-ONE", "SEVENTY-TWO", "SEVENTY-THREE", "SEVENTY-FOUR",
    "SEVENTY-FIVE", "SEVENTY-SIX", "SEVENTY-SEVEN", "SEVENTY-EIGHT", "SEVENTY-NINE",
    "EIGHTY", "EIGHTY-ONE", "EIGHTY-TWO", "EIGHTY-THREE", "EIGHTY-FOUR",
    "EIGHTY-FIVE", "EIGHTY-SIX", "EIGHTY-SEVEN", "EIGHTY-EIGHT", "EIGHTY-NINE",
    "NINETY", "NINETY-ONE", "NINETY-TWO", "NINETY-THREE", "NINETY-FOUR",
    "NINETY-FIVE", "NINETY-SIX", "NINETY-SEVEN", "NINETY-EIGHT", "NINETY-NINE" ]

# Compute the set of letters and non-letters.
CHARACTERS = sorted(list(set("".join(NUMBER_NAMES))))
LETTERS = "".join(letter for letter in CHARACTERS if letter.isalpha())
PUNCTUATION = "".join(letter for letter in CHARACTERS if not letter.isalpha()) + " '"
assert(len(LETTERS) == 16)
assert(len(PUNCTUATION) == 3)

# Cycle of length 2.
CYCLE2 = [21, 4, 2, 5, 7, 2, 10, 6, 6, 19, 8, 3, 4, 3, 3, 1]

# Describe a count of a certain letter (e.g., "FIVE V'S").
def describe_count(letter, count):
    return NUMBER_NAMES[count] + " " + letter + ("'S" if count != 1 else "")

# Represents the 16 letters and their counts.
class Square:
    def __init__(self):
        self.set_to([0]*len(LETTERS))

    # Update our own phrases with the counts from another square.
    def update_with(self, other):
        counts = [0]*len(LETTERS)

        for phrase in other.box:
            for letter in phrase:
                index = LETTERS.find(letter)
                if index == -1:
                    assert letter in PUNCTUATION
                else:
                    counts[index] += 1

        self.set_to(counts)

    # Set our phrases using these counts.
    def set_to(self, counts):
        self.counts = tuple(counts)
        self.box = [describe_count(letter, count) for letter, count in zip(LETTERS, counts)]

    # Dump box to output.
    def dump(self, out):
        for i in range(len(self.box)):
            out.write("%-20s" % self.box[i])
            if i % 4 == 3:
                out.write("\n")
        out.write("\n")

# Find cycle starting with a randomly-generated square.
def find_cycle(out):
    s = Square()

    # s.set_to(CYCLE2)

    s.set_to([random.randint(0,99) for letter in LETTERS])

    history = []
    for i in range(100000):
        s.update_with(s)
        # s.dump(out)

        # Check if we've seen this before.
        if s.counts in history:
            recent = list(reversed(history))
            cycle_length = recent.index(s.counts) + 1
            # out.write("Found cycle of length %d after %d iterations.\n" % (cycle_length, i))
            return recent[0:cycle_length]

        history.append(s.counts)

    assert False

def main(out):
    # All the cycles we've ever seen.
    cycles = set()

    while True:
        # Find a random cycle.
        cycle = find_cycle(out)

        # Sort cycle so that cycles of different phases don't come up
        # multiple times.
        cycle = sorted(cycle)

        # Make into a tuple so we can put it into a set.
        cycle = tuple(cycle)

        # Dump if we've not seen it before.
        if cycle not in cycles:
            out.write("---- Found cycle of length %d:\n\n" % len(cycle))
            for counts in cycle:
                s = Square()
                s.set_to(counts)
                s.dump(out)
            out.flush()
            cycles.add(cycle)

if __name__ == "__main__":
    main(sys.stdout)

