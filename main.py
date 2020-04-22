
def get_text():
    with open("shakespeare-complete-works.txt", "r+", encoding="utf-8-sig") as f:
        return ''.join(e for e in f.read().lower() if e in "qwertyuiopasdfghjklzxcvbnm -'")


class Node:
    def __init__(self, char="*", key=-1):
        self.char = char
        self.children = {}
        self.key = key

    def is_not_key(self):
        return self.key == -1

    def is_key(self):
        return self.is_not_key() is False


class suffix_tree:
    def __init__(self, txt):
        self.root = Node()
        self.txt = txt + "$"

        # Get every "word" in the txt
        for w_idx in range(len(txt)):
            self.add_node(self.root, w_idx)

    def validate_tree(self, p=False):
        count = {"count": 0}
        ca = []

        def iterate_tree(n, d):
            d["count"] = d["count"] + 1
            if n.is_key():
                ca.append(n.key)
                if p:
                    print(n.key, self.txt[n.key:])
            for n in n.children.values():
                iterate_tree(n, d)

        iterate_tree(self.root, count)

        r1 = len(set(ca))
        r2 = len(self.txt) - 1
        r3 = max(ca) + 1
        valid = r1 == r2 == r3
        if p:
            print("")
        print("Nodes:        ", count["count"])
        print("Text length:  ", r2)
        print("Words in tree:", r1)
        print("\nTree valid:", valid)
        if p:
            print("\nFirst 100 keys:", ca[:100])

        return valid

    def add_node(self, node, w_idx):

        # Get every "char_index" of word
        for i in range(len(self.txt) - w_idx):

            # Extend its properties into a child
            if node.is_key():

                nnc = self.txt[node.key + i]
                node.children[nnc] = Node(nnc, node.key)
                node.key = -1

            # Desired char
            char = self.txt[w_idx + i]

            # if child doesnt exist create it and break
            if char not in node.children:

                node.children[char] = Node(char, w_idx)
                break

            node = node.children[char]

    def search(self, word):

        node = self.root
        s = f"({node.char})"

        # Find deepest node containing our "word"
        for char in word:

            if char in node.children:
                node = node.children[char]
                s += f" ({node.char})"
            else:
                break

        print(s, list(map(lambda x: x.char, node.children.values())))

        node_idxs = []

        def iterate_tree(n, node_idxs):
            if n.is_key() and word == self.txt[n.key:n.key + len(word)]:  # and word == self.txt[n.key:len(word)]:
                #print(word, n.key, "-" + self.txt[n.key:n.key + len(word)] + "-")
                node_idxs.append(n.key)

            for n in n.children.values():
                iterate_tree(n, node_idxs)

        iterate_tree(node, node_idxs)

        return node_idxs


txt = "ATTAGTACA"
#txt = "lars elsker at spise pizza med sin son daniel, lars er en fisk"
txt = get_text()[:100000]
# txt = "banana"
# txt = "lars er gift med gitte og har en fisk ved navn lars"
st = suffix_tree(txt)
st.validate_tree()


print("\n--------------------\n")

# n = st.search("larsl")
# print(n)


# ATTAGTACA$ -> w_idx 0:
# 1. c_idx 0 doesnt exist -> create Node A -> set w_idx to 0
#      (*)
#     /
#   (A)
#    T
#    T
#    A
#    G
#    T
#    A
#    C
#    A
#    $

# TTAGTACA$ -> w_idx 1:
# 1. c_idx 1 doesnt exist -> create Node T -> set w_idx to 1
#      (*)
#     /   \
#   (A)   (T)
#    T     T
#    T     A
#    A     G
#    G     T
#    T     A
#    A     C
#    C     A
#    A     $
#    $

# TAGTACA$ -> w_idx 2:
# 1. c_idx 2 already exist -> jump into Node T
# 2. ("T" != "A") -> split into Node(T) and Node(A)
# 3. create Node(T) and add to parrent Node(T) -> set w_idx to parrent Node(T)s w_idx
# 4. create Node(A) and add to parrent Node(T) -> set w_idx to curent w_idx 2
#      (*)
#     /   \
#   (A)   (T)
#    T   /   \
#    T  (T)  (A)
#    A   A    G
#    G   G    T
#    T   T    A
#    A   A    C
#    C   C    A
#    A   A    $
#    $   $

# AGTACA$ -> w_idx 3:
# 1. c_idx 3 already exist -> jump into Node A
# 2. ("G" != "T") -> split into Node(G) and Node(T)
#       (*)
#      /   \
#     /     \
#   (A)     (T)
#  /   \   /   \
# (G) (T) (T) (A)
#  T   T   A   G
#  A   A   G   T
#  C   G   T   A
#  A   T   A   C
#  $   A   C   A
#      C   A   $
#      A   $
#      $

# etc ...

#-------------------------------------


# BBBB$ -> w_idx 0:
#
# c_idx 0/4: doesnt exist
#            -> create Node(B) -> set w_idx to 0
#            -> set Node(B) as child of current active Node(*)
#            -> break
# (*) <-BEFORE
#   \
#   (B) [0]
#    B
#    B
#    B
#    $
#
#-------------------------------------
# BBB$ -> w_idx 1:
#
# c_idx 1/4: already exist -> jump into Node B
#          (c_idx(1, B) == Node.char)
#          (len(Node.children) == 0)
#          -> Create Node(B) set w_idx to active Node(B)s w_idx
#          -> Set current active Node as Child of new Node(B)
#          -> Set new Node(B) as active
#  (*) <-BEFORE
#    \
#    (B) <-AFTER
#      \
#      (B) [0]
#       B
#       B
#       $
#
# c_idx 2/4: already exist -> jump into Node B
#          (c_idx(2, B) == Node.char)
#          (len(Node.children) == 0)
#          -> Create Node(B) set w_idx to active Node(B)s w_idx
#          -> Set current active Node as Child of new Node(B)
#          -> Set new Node(B) as active
# (*)
#   \
#   (B) <-BEFORE
#     \
#     (B) <-AFTER
#       \
#       (B) [0]
#        B
#        $
#
# c_idx 3/4: already exist -> jump into Node B
#          (c_idx(3, B) == Node.char)
#          -> Create Node(B) set w_idx to active-Node(B)s w_idx
#          -> Set current active Node as Child of new Node(B)
#          -> Set new Node(B) as active
# (*)
#   \
#   (B)
#     \
#     (B) <-BEFORE
#       \
#       (B) <-AFTER
#         \
#         (B) [0]
#          $
#
# c_idx 4/4: doesnt exist
#           -> create Node($) -> set w_idx to 1
#           -> set Node($) as child of current active Node(B)
#           -> break
# (*)
#   \
#   (B)
#     \
#     (B)
#       \
#       (B) <-BEFORE
#       / \
# [1] ($) (B) [0]
#          $
#
#-------------------------------------
# BB$ -> w_idx 2:
#
# c_idx 2/4: (txt[c_idx] in node.children)
#            (node.is_key == false)
#             -> set node = node.children[txt[c_idx]]
# (*) <-BEFORE
#   \
#   (B) <-AFTER
#     \
#     (B)
#       \
#       (B)
#       / \
# [1] ($) (B) [0]
#          $
#
# c_idx 3/4: (txt[c_idx] in node.children)
#            (node.is_key == false)
#             -> set node = node.children[txt[c_idx]]
# (*)
#   \
#   (B) <-BEFORE
#     \
#     (B) <-AFTER
#       \
#       (B)
#       / \
# [1] ($) (B) [0]
#          $
#
# c_idx 4/4: (txt[c_idx] not in node.children)
#            -> create Node($) -> set key to 2
#            -> set Node($) as child of current active Node(B)
#            -> break
#   (*)
#     \
#     (B)
#       \
#       (B) <-BEFORE
#       / \
# [2] ($) (B)
#         / \
#   [1] ($) (B) [0]
#            $
#
#-------------------------------------
# B$ -> w_idx 3:
#
# c_idx 3/4: (txt[c_idx] in node.children)
#            (node.is_key == false)
#             -> set node = node.children[txt[c_idx]]
#   (*) <-BEFORE
#     \
#     (B) <-AFTER
#       \
#       (B)
#       / \
# [2] ($) (B)
#         / \
#   [1] ($) (B) [0]
#            $
#
# c_idx 4/4: (txt[c_idx] not in node.children)
#            -> create Node($) -> set key to 3
#            -> set Node($) as child of current active Node(B)
#            -> break
#     (*)
#       \
#       (B) <-BEFORE
#       / \
# [3] ($) (B)
#         / \
#   [2] ($) (B)
#           / \
#     [1] ($) (B) [0]
#              $
#
#-------------------------------------
# $ -> w_idx 4:
#
# c_idx 4/4: (txt[c_idx] not in node.children)
#            -> create Node($) -> set key to 4
#            -> set Node($) as child of current active Node(*)
#            -> break
#
#       (*)<-BEFORE
#       / \
# [4] ($) (B)
#         / \
#   [3] ($) (B)
#           / \
#     [2] ($) (B)
#             / \
#       [1] ($) (B) [0]
#                $


# PHILOSOPHI
#                (Does Node have desired Child)
#               /                              \
#           NO /                                \ YES
#             /                                  \
#   {Create Child & break}             (Does Node have a key)
#                                     /                      \
#                                 NO /                        \ YES
#                 __________________/______              ______\________________________________________
#                | Set desired child       |            | Create a new Node as a child of current Node. |
#                |_as_our_new_active_Node__|            | Give this new node, the current next char of  |
#                                                       | the active node and its key, and remove key   |
#                                                       | from current active node.                     |
#                                                       |_Set_the_new_Node_as_our_active_Node.__________|
#
#  (*)          .  (*)                 .  (*)
#    \          .    \                 .    \
#    (B) [0]    .    (B) [0] --------- .    (B)
#      \        .      \             | .      \
#      (B)      .      (B)           | .      (B)
#        \      .        \           | .        \
#        (B)    .        (B)         | .        (B)
#        / \    .        / \         | .        / \
#      ($) (B)  .      ($) (B)  <----- .  [1] ($) (B) [0]
#           $   .           $          .           $


# B->B->B->B->$
# B->B->B->$


#####

#(*)
#  \
#   (B -> BBB$)
#

#(*)                    (*)
#  \                      \
#   (B -> BBB$)           (B)
#                           \
#                            ()


# If note doesnt have child:
#   we create the child and return
# Else:
#   note = note.children[c]
#
#   if

#                                            (*)
#    (*)      (*)         (*)               / | \
#   /        /   \       / | \             /  |  \
# (L)      (L)   (A)   (L)(A)(R)         (L) (A) (R)
#  A        A     R     A  R  L          /  R
#  R        R     L     R  L  A        (A)
#  L        L     A     L  A  R        /
#  A        A     R     A  R  $      (R)
#  R        R     $     R  $ [2]     / \
#  $        $    [1]    $ [1]      ($) (L)
# [0]      [0]         [0]         [3]  A
#                                       R
#                                       $
#                                      [0]

# import PySimpleGUI as sg

# layout: list = [
#     [sg.InputText('', size=(16, 1), background_color='black', text_color='red', font=('Digital-7', 51), key="searchbar")],
#     [sg.Text('Start typing!', size=(50, 10), background_color="#272533", text_color='white', font=('Franklin Gothic Book', 14), key="result")],
# ]

# window: object = sg.Window('At være eller ikke at være', layout=layout, margins=(10, 20), background_color="#272533", return_keyboard_events=True)

# while True:
#     event, values = window.read()

#     if event is None and type(event) is not str:
#         break
#     else:
#         try:
#             if len(values["searchbar"]) > 0:
#                 n = st.search(values["searchbar"])
#                 s = ""
#                 for i in n[:10]:
#                     s += str(i) + " -> " + txt[i:i + 40] + "\n"
#                 window['result'].update(value=s)
#         except:
#             window['result'].update(value="")