import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt();
        int M = sc.nextInt();
        BitSet b1, b2;
        b1 = new BitSet(N);
        b2 = new BitSet(N);
        
        for(int i=0; i<M; i++) {
            String instr = sc.next();
            int setNumber = sc.nextInt();
            int op = sc.nextInt();
            //sc.nextLine();
            
            if(instr.equals("AND")) {
                if(setNumber == 1) {
                    b1.and(b2);
                } else if(setNumber == 2) {
                    b2.and(b1);
                }
            } else if(instr.equals("OR")) {
                if(setNumber == 1) {
                    b1.or(b2);
                } else if(setNumber == 2) {
                    b2.or(b1);
                }
            } else if(instr.equals("XOR")) {
                if(setNumber == 1) {
                    b1.xor(b2);
                } else if(setNumber == 2) {
                    b2.xor(b1);
                }
            } else if(instr.equals("FLIP")) {
                if(setNumber == 1) {
                    b1.flip(op);
                } else if(setNumber == 2) {
                    b2.flip(op);
                }
            } else if(instr.equals("SET")) {
                if(setNumber == 1) {
                    b1.set(op);
                } else if(setNumber == 2) {
                    b2.set(op);
                }
            }
            System.out.println(b1.cardinality() + " " + b2.cardinality());
        }
        
        sc.close();
    }
}
