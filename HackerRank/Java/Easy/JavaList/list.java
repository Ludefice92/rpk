import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), i;
        List<Integer> L = new ArrayList<Integer>();
        for(i=0; i<n; i++) {
            L.add(sc.nextInt());
        }
        int q = sc.nextInt(), index=0, value=0;
        sc.nextLine();
        String query;
        for(i=0; i<q; i++) {
            query = sc.next();
            index = sc.nextInt();
            if(query.equalsIgnoreCase("Insert")) {
                value = sc.nextInt();
                L.add(index, value);
            } else if(query.equalsIgnoreCase("Delete")) {
                L.remove(index);
            }
        }
        
        for(i=0; i<L.size(); i++) {
            System.out.printf("%d ",L.get(i));
        }
        
        sc.close();;
    }
}
