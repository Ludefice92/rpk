Snow Howler is the librarian at the central library of the city of HuskyLand. He must handle requests which come in the following forms:

1 x y : Insert a book with  pages at the end of the  shelf.

2 x y : Print the number of pages in the  book on the  shelf.

3 x : Print the number of books on the  shelf.

Snow Howler has got an assistant, Oshie, provided by the Department of Education. Although inexperienced, Oshie can handle all of the queries of types 2 and 3.

Help Snow Howler deal with all the queries of type 1.

Oshie has used two arrays:

int* total_number_of_books;
/*
 * This stores the total number of books on each shelf.
 */

int** total_number_of_pages;
/*
 * This stores the total number of pages in each book of each shelf.
 * The rows represent the shelves and the columns represent the books.
 */
Input Format

The first line contains an integer , the number of shelves in the library.
The second line contains an integer , the number of requests.
Each of the following  lines contains a request in one of the three specified formats.

Constraints

For each query of the second type, it is guaranteed that a book is present on the  shelf at  index.
Both the shelves and the books are numbered starting from 0.
Maximum number of books per shelf .
Output Format

Write the logic for the requests of type 1. The logic for requests of types 2 and 3 are provided.

Sample Input 0

5
5
1 0 15
1 0 20
1 2 78
2 2 0
3 0
Sample Output 0

78
2
Explanation 0

There are  shelves and  requests, or queries.
- 1 Place a  page book at the end of shelf .
- 2 Place a  page book at the end of shelf .
- 3 Place a  page book at the end of shelf .
- 4 The number of pages in the  book on the  shelf is 78.
- 5 The number of books on the  shelf is 2.