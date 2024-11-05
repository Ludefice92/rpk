import java.util.Scanner;

public class Solution {

    static boolean isAnagram(String a, String b) {
        // Complete the function
        //I would use a map for this, but I'm not allowed to so I will use these 2 arrays instead
        char[] alphabet = new char[26];
        for(int i=0; i<26; i++) {
            alphabet[i] = (char) ('a'+i);
        }
        int[] sumCharsA = new int[26]; //holds sum of each letter of the alphabet
        int[] sumCharsB = new int[26]; //holds sum of each letter of the alphabet
        boolean aUpdated = false;
        boolean bUpdated = false;
        if(a.length() == b.length()) { //anagram strings must be the same size
            for(int j=0; j<a.length(); j++) {
                for(int k=0; k<26; k++) {
                    if(a.substring(j,j+1).compareToIgnoreCase(String.valueOf(alphabet[k]))==0) {
                        sumCharsA[k]++;
                        aUpdated = true;
                    }
                    if(b.substring(j,j+1).compareToIgnoreCase(String.valueOf(alphabet[k]))==0) {
                        sumCharsB[k]++;
                        bUpdated = true;
                    }
                    if(aUpdated && bUpdated) {
                        aUpdated = false;
                        bUpdated = false;
                        break;
                    }
                }
            }
            for(int l=0; l<26; l++) {
                if(sumCharsA[l] != sumCharsB[l]) return false;
            }
            return true;
        }
        
        return false;
    }

    public static void main(String[] args) {
    
        Scanner scan = new Scanner(System.in);
        String a = scan.next();
        String b = scan.next();
        scan.close();
        boolean ret = isAnagram(a, b);
        System.out.println( (ret) ? "Anagrams" : "Not Anagrams" );
    }
}