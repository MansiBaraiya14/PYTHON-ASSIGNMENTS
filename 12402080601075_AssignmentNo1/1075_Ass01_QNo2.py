class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = False


def build_automaton(words):
    root = TrieNode()

    # Build Trie
    for word in words:
        node = root

        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.output = True

    # Build failure links
    from collections import deque

    queue = deque()

    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        current = queue.popleft()

        for ch, child in current.children.items():
            queue.append(child)

            fail_node = current.fail

            while fail_node != root and ch not in fail_node.children:
                fail_node = fail_node.fail

            if ch in fail_node.children and fail_node.children[ch] != child:
                child.fail = fail_node.children[ch]
            else:
                child.fail = root

            if child.fail.output:
                child.output = True

    return root


def contains_banned(password, root):
    node = root

    for ch in password.lower():

        while node != root and ch not in node.children:
            node = node.fail

        if ch in node.children:
            node = node.children[ch]
        else:
            node = root

        if node.output:
            return True

    return False


def has_repeated_character(password):
    count = 1

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1

            if count > 3:
                return True
        else:
            count = 1

    return False


def classify_password(password, root):

    # Length check
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    # Repeated character check
    if has_repeated_character(password):
        return "WEAK_PATTERN"

    # Banned word check
    if contains_banned(password, root):
        return "COMPROMISED"

    # Character requirements
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "$#@":
            has_special = True

    if has_lower and has_upper and has_digit and has_special:
        return "STRONG"

    return "WEAK_PATTERN"


# Input
b = int(input())

banned_words = []

for _ in range(b):
    banned_words.append(input().strip())

root = build_automaton(banned_words)

n = int(input())

for i in range(1, n + 1):
    password = input().strip()

    result = classify_password(password, root)

    print(f"{i}: {result}")