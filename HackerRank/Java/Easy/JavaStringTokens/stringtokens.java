import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.nextLine().trim();
        if(s.isEmpty()) {
            System.out.println(0);
            scan.close();
            return;
        }
        // Write your code here.
        String[] splitS = s.split("[^A-Za-z]+");
        System.out.println(splitS.length);
        for(String tok : splitS) {
            System.out.println(tok);
        }
        scan.close();
    }
}

