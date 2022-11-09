package fi.tuni.prog3.sisu;

/**
 * Contains information of one studymodule
 *
 */
public class StudyModule extends Module {

    private String description;
    private String outcome;

    /**
     * Empty constructor
     */
    public StudyModule() {
        this.description = "";
        this.outcome = "";
    }

    ;

    /**
     * Constructor
     * @param name - name of the course
     * @param groupId - course groupID
     * @param description - StudyModule description
     * @param credits - StudyModule credits
     */
    public StudyModule(String name, String groupId, String description, int credits) {
        super(name, groupId, credits);
        this.description = description;
    }

    /**
     * Set outcome for StudyModule
     *
     * @param outcomes - StudyModule outcome
     */
    public void setOutcomes(String outcomes) {
        this.outcome = outcomes;
    }

    /**
     * Get StudyModule outcome
     *
     * @return String StudyModule outcome
     */
    public String getOutcomes() {
        return this.outcome;
    }

    /**
     * Set description for StudyModule
     *
     * @param desc - StudyModule description
     */
    public void setDescription(String desc) {
        this.description = desc;
    }

    /**
     * Get StudyModule description
     *
     * @return String StudyModule description
     */
    public String getDescription() {
        return this.description;
    }

}
