import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        String S = in.next();
        int start = in.nextInt();
        int end = in.nextInt();
        String substring = "";
        int subStringIndex = 0;
        for(int i=start; i<end; i++) {
            substring += S.charAt(i);
            subStringIndex++;
        }
        System.out.print(substring);
    }
}
