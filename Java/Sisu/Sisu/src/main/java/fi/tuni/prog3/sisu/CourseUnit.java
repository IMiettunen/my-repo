package fi.tuni.prog3.sisu;

/**
 * Contains information about one specific course
 *
 *
 */
public class CourseUnit extends TreeViewObject {

    private String name;
    private String groupId;
    private int minCredits;
    private int maxCredits;
    private String description;
    private String code;
    private String outcome;

    /**
     * Empty constructor
     */
    public CourseUnit() {
    }

    ;

    /**
     * CourseUnit constructor
     * @param name - name of the course
     * @param groupId - unique groupId of the course
     * @param description - description of the course
     * @param minCredits - minimum credits from completed course
     */
    public CourseUnit(String name, String groupId, String description, int minCredits) {
        this.name = name;
        this.groupId = groupId;
        this.description = description;
        this.minCredits = minCredits;
        this.maxCredits = minCredits;
    }

    /**
     * Get name of the course
     *
     * @return String Name of the course
     */
    public String getName() {
        return this.name;
    }

    /**
     *
     * @return
     */
    @Override
    public String toString() {
        String s;
        if (this.maxCredits != this.minCredits) {
            s = String.format("%s %s %d-%dop", this.code, this.name, this.minCredits, this.maxCredits);
        } else {
            s = String.format("%s %s %dop", this.code, this.name, this.minCredits);
        }

        return s;
    }

    /**
     * Set outcome value to course
     *
     * @param outcome - outcome of the course
     */
    public void setOutcome(String outcome) {
        this.outcome = outcome;
    }

    /**
     * Get course outcome
     *
     * @return String Outcome of the course
     */
    public String getOutcomes() {
        return this.outcome;
    }

    /**
     * Set code for the course
     *
     * @param code - course code
     */
    public void setCode(String code) {
        this.code = code;
    }

    /**
     * Get code of the course
     *
     * @return String Course code
     */
    public String getCode() {
        return this.code;
    }

    /**
     * Set name of the course
     *
     * @param name - Name of the course
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Set groupID for course
     *
     * @param groupId - groupID
     */
    public void setGroupId(String groupId) {
        this.groupId = groupId;
    }

    /**
     * Set course description
     *
     * @param desc - description
     */
    public void setDescription(String desc) {
        this.description = desc;
    }

    /**
     * Set value for minimum credit
     *
     * @param credits - value of minimum credit
     */
    public void setMinCredits(int credits) {
        this.minCredits = credits;
    }

    /**
     * Set value for maximum credit
     *
     * @param credits - value of max credit
     */
    public void setMaxCredits(int credits) {
        this.maxCredits = credits;
    }

    /**
     * Get minimum credit from course
     *
     * @return Int min credit of the course
     */
    public int getMinCredits() {
        return this.minCredits;
    }

    /**
     * Get max possible credit from course
     *
     * @return Int max credit of the course
     */
    public int getMaxCredits() {
        return this.maxCredits;
    }

    /**
     * Get course description
     *
     * @return String course description
     */
    public String getDescription() {
        return this.description;
    }

    /**
     * Get course's groupID
     *
     * @return String course groupID
     */
    public String getGroupId() {
        return this.groupId;
    }

}
