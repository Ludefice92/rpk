import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int n, negSubArrays=0;
        n = sc.nextInt();
        int arr[] = new int[n];
        for(int i=0; i<n; i++) {
            arr[i] = sc.nextInt();
        }
        for(int i=0; i<n; i++) {
            int sumSubArr = 0;
            for(int j=i; j<n; j++) {
                sumSubArr += arr[j];
                if(sumSubArr<0) negSubArrays++;
            }
        }
        System.out.println(negSubArrays);
        sc.close();
    }
}
