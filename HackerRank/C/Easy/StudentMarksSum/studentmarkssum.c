#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

//Complete the following function.
//odd marks in marks are for girls, even marks are for boys
int marks_summation(int* marks, int number_of_students, char gender) {
  //Write your code here.
  int sumMarks = 0;
  for(int i=0; i<number_of_students; i++) {
      if(gender == 'b' && i % 2 == 0) sumMarks += marks[i];
      if(gender == 'g' && i % 2 != 0) sumMarks += marks[i];
  }
  return sumMarks;
}

int main() {
    int number_of_students;
    char gender;
    int sum;
  
    scanf("%d", &number_of_students);
    int *marks = (int *) malloc(number_of_students * sizeof (int));
 
    for (int student = 0; student < number_of_students; student++) {
        scanf("%d", (marks + student));
    }
    
    scanf(" %c", &gender);
    sum = marks_summation(marks, number_of_students, gender);
    printf("%d", sum);
    free(marks);
 
    return 0;
}