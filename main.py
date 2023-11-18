class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def suggest_words(self, word):
        suggestions = set()
        current_row = list(range(len(word) + 1))

        for char, child_node in self.root.children.items():
            self.suggest_words_recursive(child_node, char, word, [0] * (len(word) + 1), suggestions)

        return list(suggestions)

    def suggest_words_recursive(self, node, char, target, previous_row, suggestions):
        columns = len(target) + 1
        current_row = [0] * columns

        for i in range(columns):
            current_row[i] = i

        for next_char, next_node in node.children.items():
            self.suggest_words_recursive(next_node, next_char, target, current_row, suggestions)

        for i in range(1, columns):
            insert_cost = current_row[i - 1] + 1
            delete_cost = previous_row[i] + 1
            replace_cost = previous_row[i - 1] + (char != target[i - 1])

            current_row[i] = min(insert_cost, delete_cost, replace_cost)

        if node.is_end_of_word and current_row[-1] <= 2:
            suggestions.add(target)

        for i in range(1, columns - 1):
            if i + 1 < columns:
                transposition_cost = previous_row[i - 1] + (char != target[i]) + (char != target[i + 1])
                current_row[i + 1] = min(current_row[i + 1], transposition_cost)

        if node.is_end_of_word and columns > 1 and current_row[-1] <= 2:
            suggestions.add(target)

def load_dictionary(file_path):
    trie = Trie()
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            trie.insert(word)
    return trie

def save_dictionary(file_path, trie):
    with open(file_path, 'w') as file:
        pass

def main():
    dictionary_path = "words.txt"
    trie = load_dictionary(dictionary_path)

    while True:
        user_input = input("Enter a word (type 'exit' to quit): ").lower()

        if user_input == 'exit':
            break

        if user_input.isalpha():
            if trie.search(user_input):
                print(f'{user_input} is a valid word.')
            else:
                suggestions = trie.suggest_words(user_input)
                if suggestions:
                    print(f'Did you mean: {suggestions}?')
                else:
                    print('No suggestions available.')

    save_dictionary(dictionary_path, trie)

if __name__ == "__main__":
    main()
