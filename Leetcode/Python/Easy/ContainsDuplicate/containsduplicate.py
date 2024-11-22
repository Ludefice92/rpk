class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        setver = set(nums)
        if len(nums) != len(setver): return True
        else: return False
        