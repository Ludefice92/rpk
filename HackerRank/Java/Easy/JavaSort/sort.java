import java.util.*;

class Student{
	private int id;
	private String fname;
	private double cgpa;
	public Student(int id, String fname, double cgpa) {
		super();
		this.id = id;
		this.fname = fname;
		this.cgpa = cgpa;
	}
	public int getId() {
		return id;
	}
	public String getFname() {
		return fname;
	}
	public double getCgpa() {
		return cgpa;
	}
}

//Complete the code
public class Solution
{
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		int testCases = Integer.parseInt(in.nextLine());
		
		List<Student> studentList = new ArrayList<Student>();
		while(testCases>0){
			int id = in.nextInt();
			String fname = in.next();
			double cgpa = in.nextDouble();
			
			Student st = new Student(id, fname, cgpa);
			studentList.add(st);
			
			testCases--;
		}
        
        //need a custom sort comparator
        Collections.sort(studentList, new Comparator<Student>() {
            @Override
            public int compare(Student st1, Student st2) {
                if(Double.compare(st2.getCgpa(), st1.getCgpa())!=0) {
                    return Double.compare(st2.getCgpa(), st1.getCgpa());
                } else if(!st1.getFname().equals(st2.getFname())) {
                    return st1.getFname().compareTo(st2.getFname());
                } else {
                    return Integer.compare(st1.getId(),st2.getId());
                }
            }
        });
      
      	for(Student st: studentList){
			System.out.println(st.getFname());
		}
	}
}



