import java.util.Scanner;

public class Solution {

    public static String getSmallestAndLargest(String s, int k) {
        String smallest = "";
        String largest = "";
        
        // Complete the function
        // 'smallest' must be the lexicographically smallest substring of length 'k'
        // 'largest' must be the lexicographically largest substring of length 'k'
        for(int i=0; i<s.length()-k+1; i++) {
            String newStr = s.substring(i, i+k);
            if(i==0) {
                smallest = newStr;
            } else {
                if(smallest.compareTo(newStr) > 0) smallest = newStr;
            }
            if(largest.compareTo(newStr) < 0) largest = newStr;
        }
        
        
        return smallest + "\n" + largest;
    }


    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.next();
        int k = scan.nextInt();
        scan.close();
      
        System.out.println(getSmallestAndLargest(s, k));
    }
}