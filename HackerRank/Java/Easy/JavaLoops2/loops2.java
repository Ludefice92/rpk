import java.util.*;
import java.io.*;

class Solution{
    public static void main(String []argh){
        Scanner in = new Scanner(System.in);
        int t=in.nextInt();
        for(int i=0;i<t;i++){
            int a = in.nextInt();
            int b = in.nextInt();
            int n = in.nextInt();
            int seriesValue = a;
            for(int j=0; j<n; j++) {
                seriesValue += Math.pow(2,j) * b;
                System.out.printf("%d ", seriesValue);            
            }
            System.out.printf("\n");
        }
        in.close();
    }
}
