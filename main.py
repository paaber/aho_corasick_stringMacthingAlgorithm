from collections import deque


class StringMatch():
    def __init__(self):
        super(StringMatch, self).__init__()
        self.Adjacency_list = []

    def initialise_trie(self, keywords):
        """ creates a trie of keywords, then sets fail transitions """

        self.creat_empty_trie()
        self.add_Keywords(keywords)

        self.set_fail_transitions()

    def creat_empty_trie(self):
        """ create's an empty trie to initalize the root of the trie """
        self.Adjacency_list.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []})

    def add_Keywords(self, keywords):
        """ adds all keywords to the lists of keywords """

        for keyword in keywords:
            self.add_keyword(keyword)
            pass

    def find_next_state(self, current_state, value):

        for node in self.Adjacency_list[current_state]["next_states"]:

            if self.Adjacency_list[node]["value"] == value:
                return node

        return None

    def add_keyword(self, keyword):

        """ add a keyword to the trie and mark output at the last node
        :type keyword: str
        """

        self.current_state = 0

        j = 0

        self.keyword = keyword.lower()

        self.child = self.find_next_state(self.current_state, self.keyword[j])

        while self.child != None:

            self.current_state = self.child

            j = j + 1

            if j < len(self.keyword):

                self.child = self.find_next_state(self.current_state, self.keyword[j])
            else:

                break

        for i in range(j, len(self.keyword)):
            node = {'value': self.keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}

            self.Adjacency_list.append(node)

            self.Adjacency_list[self.current_state]["next_states"].append(len(self.Adjacency_list) - 1)

            self.current_state = len(self.Adjacency_list) - 1

        self.Adjacency_list[self.current_state]["output"].append(self.keyword)

    def set_fail_transitions(self):

        q = deque()

        self.child_ft = 0

        for node in self.Adjacency_list[0]["next_states"]:
            q.append(node)

            self.Adjacency_list[node]["fail_state"] = 0

        while q:

            r = q.popleft()

            for self.child_ft in self.Adjacency_list[r]["next_states"]:

                q.append(self.child_ft)

                state = self.Adjacency_list[r]["fail_state"]

                while self.find_next_state(state, self.Adjacency_list[self.child_ft]["value"]) == None and state != 0:
                    state = self.Adjacency_list[state]["fail_state"]

                self.Adjacency_list[self.child_ft]["fail_state"] = self.find_next_state(state, self.Adjacency_list[
                    self.child_ft]["value"])

                if self.Adjacency_list[self.child_ft]["fail_state"] is None:
                    self.Adjacency_list[self.child_ft]["fail_state"] = 0

                self.Adjacency_list[self.child_ft]["output"] = self.Adjacency_list[self.child_ft]["output"] + \
                                                               self.Adjacency_list[
                                                                   self.Adjacency_list[self.child_ft]["fail_state"]][
                                                                   "output"]

    def get_keywords_found(self, line):

        """ returns true if line contains any keywords in trie """
        self.line = line.lower()
        current_state = 0
        self.searched_keywords = []
        for i in range(len(self.line)):

            while self.find_next_state(current_state, self.line[i]) is None and current_state != 0:
                current_state = self.Adjacency_list[current_state]["fail_state"]
            current_state = self.find_next_state(current_state, self.line[i])

            if current_state is None:

                current_state = 0
            else:
                for j in self.Adjacency_list[current_state]["output"]:
                    self.searched_keywords.append({"index": i - len(j) + 1, "word": j})

        return self.searched_keywords


c = StringMatch()
c.initialise_trie(['b', 'c', 'aa', 'd', 'b'])
print(c.get_keywords_found("caaab"))
# print(c.Adjacency_list)
