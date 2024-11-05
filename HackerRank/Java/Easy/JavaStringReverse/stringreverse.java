import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        
        Scanner sc=new Scanner(System.in);
        String A=sc.next();
        int j=A.length()-1;
        boolean isPalindrome = true;
        /* Enter your code here. Print output to STDOUT. */
        for(int i=0; i<A.length(); i++) {
            if(A.charAt(i) != A.charAt(j)) {
                System.out.printf("No");
                isPalindrome = false;
                break;
            }
            j--;
        }
        if(isPalindrome) System.out.printf("Yes");
    }
}



