import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int i = 1;
        String s;
        for(;;) {
            if(sc.hasNext()) {
                s = sc.nextLine();
                System.out.printf("%d %s\n", i, s);
            } else {
                break;
            }
            i++;
        }
    }
}
