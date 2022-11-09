package fi.tuni.prog3.sisu;

import java.util.ArrayList;

/**
 * Contains personal information and also information about Students studies
 *
 */
public class Student {

    private final String name;
    private final String stdNumber;
    private final DegreeProgramme programme;
    private final String password;
    private int credits;
    private ArrayList<CourseUnit> enrolledCourses;
    private ArrayList<CourseUnit> completedCourses;

    Student(String name, String stdNumber, String password, DegreeProgramme programme) {
        this.name = name;
        this.stdNumber = stdNumber;
        this.password = password;
        this.programme = programme;
        this.enrolledCourses = new ArrayList<>();
        this.completedCourses = new ArrayList<>();
        this.credits = 0;
    }

    /**
     * enroll to course
     *
     * @param c course to enroll
     */
    public void enrollToCourse(CourseUnit c) {
        if (!enrolledCourses.contains(c) && !completedCourses.contains(c)) {
            enrolledCourses.add(c);
        }

    }

    /**
     * Add course to completed courses. Deletes course from enrolled courses
     *
     * @param c course to complete
     */
    public void completeCourse(CourseUnit c) {
        if (!this.completedCourses.contains(c)) {
            if (this.enrolledCourses.contains(c)) {
                enrolledCourses.remove(c);
            }

            this.completedCourses.add(c);
            this.credits += c.getMaxCredits();
        }
    }

    public ArrayList<CourseUnit> getEnrolledCourses() {
        return this.enrolledCourses;
    }

    public ArrayList<CourseUnit> getCompletedCourses() {
        return this.completedCourses;
    }

    public int getCredits() {
        return this.credits;
    }

    public String getName() {
        return this.name;
    }

    public String getPassword() {
        return this.password;
    }

    public String getStdNumber() {
        return this.stdNumber;
    }

    public DegreeProgramme getProgramme() {
        return this.programme;
    }

}
