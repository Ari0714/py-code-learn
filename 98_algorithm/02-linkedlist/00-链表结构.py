
class Node:
    def __init__(self,data=None,next=None):
        self.data = data
        self.next = next

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node1.next = node2
node2.next = node3

print(node1.next.next.data)