package fi.tuni.prog3.sisu;

/**
 * Module for grouping courses wich do not belong to certain set of studies
 *
 */
public class GroupingModule extends Module {

    private String id;

    public GroupingModule() {

    }

    public GroupingModule(String name, String groupId, String id) {
        super(name, groupId, 0);
        this.id = id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getId() {
        return this.id;
    }

}
