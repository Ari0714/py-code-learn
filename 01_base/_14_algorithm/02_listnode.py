
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# 创建各个节点
node3 = ListNode(3)
node5 = ListNode(5)
node6 = ListNode(6)
node1 = ListNode(1)

# 构建链表
node3.next = node5
node5.next = node6
node6.next = node1

# 链表构建完成，现在 node3 是链表的头节点
head = node3

# 打印链表以验证
current_node = head
while current_node:
    print(current_node.val, end='->')
    current_node = current_node.next
print('None')  # 打印链表的结尾

