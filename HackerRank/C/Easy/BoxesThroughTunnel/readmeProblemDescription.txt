You are transporting some boxes through a tunnel, where each box is a parallelepiped, and is characterized by its length, width and height.

The height of the tunnel  feet and the width can be assumed to be infinite. A box can be carried through the tunnel only if its height is strictly less than the tunnel's height. Find the volume of each box that can be successfully transported to the other end of the tunnel. Note: Boxes cannot be rotated.

Input Format

The first line contains a single integer , denoting the number of boxes.
 lines follow with three integers on each separated by single spaces  ,  and  which are length, width and height in feet of the -th box.

Constraints

Output Format

For every box from the input which has a height lesser than  feet, print its volume in a separate line.

Sample Input 0

4
5 5 5
1 2 40
10 5 41
7 2 42
Sample Output 0

125
80
Explanation 0

The first box is really low, only  feet tall, so it can pass through the tunnel and its volume is .

The second box is sufficiently low, its volume is .

The third box is exactly  feet tall, so it cannot pass. The same can be said about the fourth box.