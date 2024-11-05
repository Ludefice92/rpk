import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        ArrayList<ArrayList<Integer>> arr = new ArrayList<ArrayList<Integer>>();
        Scanner sc = new Scanner(System.in);
        int n, d;
        n = sc.nextInt();
        for(int i=0; i<n; i++) {
            d = sc.nextInt();
            ArrayList<Integer> line = new ArrayList<Integer>();
            for(int j=0; j<d; j++) {
                line.add(j, sc.nextInt());
            }
            arr.add(i,line);
        }
        n = sc.nextInt();//now used for queries
        int x,y;
        for(int i=0; i<n; i++) {
            x = sc.nextInt();
            y = sc.nextInt();
            try {
                System.out.println(arr.get(x-1).get(y-1));         
            } catch(IndexOutOfBoundsException e) {
                System.out.println("ERROR!");
            }
        }
        
        sc.close();
    }
}
