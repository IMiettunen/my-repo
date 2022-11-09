package fi.tuni.prog3.sisu;

import java.util.ArrayList;
import java.util.Set;
import java.util.TreeMap;

/**
 * Abstract class for modules. Contains information about other modules and
 * courses it consists of
 *
 *
 */
public abstract class Module extends TreeViewObject {

    private String name;
    private String groupId;
    private TreeMap<String, CourseUnit> courses;
    private ArrayList<Module> modules;
    private int minCredits;
    private int maxCredits;

    /**
     * Empty constructor
     */
    Module() {
        this.courses = new TreeMap<>();
        this.modules = new ArrayList<>();
    }

    /**
     * Constructor
     *
     * @param name - Name of the module
     * @param groupId - Module groupID
     * @param credits - Module credits
     */
    Module(String name, String groupId, int credits) {
        this.name = name;
        this.groupId = groupId;
        this.courses = new TreeMap<>();
        this.modules = new ArrayList<>();
        this.minCredits = credits;
    }

    /**
     * Set Module name
     *
     * @param name - module name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Get Module name
     *
     * @return String Module name
     */
    public String getName() {
        return this.name;
    }

    /**
     * Get Module groupID
     *
     * @return String Module groupID
     */
    public String getGroupId() {
        return this.groupId;
    }

    /**
     * Set Module groupID
     *
     * @param groupId - module groupId
     */
    public void setGroupId(String groupId) {
        this.groupId = groupId;
    }

    /**
     * Set minimum credit for module
     *
     * @param credits - value for minimum credit
     */
    public void setMinCredits(int credits) {
        this.minCredits = credits;
    }

    /**
     * Set max credit for Module
     *
     * @param credits - value for maximum credit
     */
    public void setMaxCredits(int credits) {
        this.maxCredits = credits;
    }

    /**
     * Add course to Module
     *
     * @param groupId - course groupID
     * @param course - CourseUnit object
     */
    public void addCourse(String groupId, CourseUnit course) {
        this.courses.put(groupId, course);
    }

    /**
     * Add Module to Module
     *
     * @param module - Module object to be added
     */
    public void addModule(Module module) {
        this.modules.add(module);
    }

    /**
     * Get number of Modules inside this Module
     *
     * @return Int Number of modules
     */
    public int sizeOfModules() {
        return this.modules.size();
    }

    /**
     * Get number of CourseUnits inside this Module
     *
     * @return Int Number of CourseUnits
     */
    public int sizeOfCourses() {
        return this.courses.size();
    }

    /**
     * Get min credits from Module
     *
     * @return Int Minimum credits
     */
    public int getMinCredits() {
        return this.minCredits;
    }

    /**
     * Get max possible credit from Module
     *
     * @return Int Maximum credits
     */
    public int getMaxCredits() {
        return this.maxCredits;
    }

    /**
     * Get all modules belonging to this Module
     *
     * @return ArrayList<Module> List of Modules
     */
    public ArrayList<Module> getModules() {
        return this.modules;
    }

    /**
     * Get IDs of courses belonging to Module
     *
     * @return Set<String> Set of Course IDs
     */
    public Set<String> getCourseIDs() {
        return this.courses.keySet();
    }

    /**
     * Get courses Belonging to Module
     *
     * @return ArrayList<CourseUnit> List of courses
     */
    public ArrayList<CourseUnit> getCourses() {
        ArrayList<CourseUnit> courses = new ArrayList<>();
        for (var course : this.courses.entrySet()) {
            courses.add(course.getValue());
        }

        return courses;
    }

    @Override
    public String toString() {
        String s;
        if (this.maxCredits != this.minCredits && this.maxCredits != 0) {
            s = String.format("%s - %d-%dop", this.getName(), this.getMinCredits(), this.getMaxCredits());
        } else {
            s = String.format("%s - %dop", this.getName(), this.getMinCredits());
        }

        return s;
    }
}
