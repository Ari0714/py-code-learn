# easy
# 反转链表

class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

def reverse_linkedLise(head):
    if (not head or not head.next):
        return head   # 终止条件：返回新头节点

    new_head = reverse_linkedLise(head.next)  # 递归反转
    head.next.next = head  # 反转指向
    head.next = None   # 断开原来链接

    return new_head   # 返回新头节点

def print_list(head):
    while head:
        print(head.data,end='->')
        head = head.next
    print('None')


if __name__ == '__main__':
    head = Node(1, Node(2, Node(3, Node(4, Node(5)))))
    print_list(reverse_linkedLise(head))



