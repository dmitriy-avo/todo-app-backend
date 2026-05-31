# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        if not root:
            return False

        stack = [(root, targetSum)]

        while stack:
            cur, cur_sum = stack.pop()

            if not cur.left and not cur.right and cur_sum-cur.val == 0:
                return True


            if cur.left:
                stack.append((cur.left, cur_sum-cur.val))
            if cur.right:
                stack.append((cur.right, cur_sum-cur.val))

        return False