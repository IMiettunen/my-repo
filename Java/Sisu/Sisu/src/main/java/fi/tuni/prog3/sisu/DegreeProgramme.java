package fi.tuni.prog3.sisu;

/**
 * Describes degree program with it's contents
 *
 */
public class DegreeProgramme extends Module {

    private String id;
    private String code;

    public DegreeProgramme(String name, String groupId, String id, int credits, String code) {

        super(name, groupId, credits);
        this.id = id;
        this.code = code;
    }

    public String getId() {
        return this.id;
    }

    public String getCode() {
        return this.code;
    }

}
