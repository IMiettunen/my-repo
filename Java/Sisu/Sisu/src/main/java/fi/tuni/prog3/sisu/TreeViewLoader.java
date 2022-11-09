package fi.tuni.prog3.sisu;

import javafx.scene.control.Button;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.TreeItem;
import javafx.scene.control.TreeView;
import javafx.scene.web.WebView;

/**
 * Class for loading the treeView element for selected degree
 */
public class TreeViewLoader {

    private TreeView<TreeViewObject> treeView;
    private CourseUnit currentCourse;
    private Object currentObject;
    private StudyModule currentStudyModule;
    private Button enrollBtn;
    private DegreeProgramme degree;
    private WebView infoBox;
    private ToggleButton defaultToggle;

    TreeViewLoader(DegreeProgramme prog, WebView infoBox, Button enrollBtn, ToggleButton defaultToggle) {
        treeView = new TreeView<>();
        treeView.setId("treeview");
        this.degree = prog;
        this.infoBox = infoBox;
        this.enrollBtn = enrollBtn;
        this.defaultToggle = defaultToggle;
    }

    /**
     * Method for getting treeView
     *
     * @return TreeView<TreeViewObject>
     */
    public TreeView<TreeViewObject> getTreeViewObject() {
        return this.treeView;
    }

    /**
     * Methdod for getting current CourseUnit that user has selected from
     * treeeView
     *
     * @return CourseUnit
     */
    public CourseUnit getCurrentCourse() {
        return currentCourse;
    }

    /**
     * Method for getting current selected object's class
     *
     * @return Object
     */
    public Object getCurrentObjectClass() {
        return this.currentObject;
    }

    /**
     * Method for handling user action on treeView's objects
     *
     * @param obj clicked object
     */
    private void handleMouseClickOnCourse(TreeViewObject obj) {

        this.currentObject = obj.getClass();
        this.defaultToggle.setSelected(true);
        // enroll button is only active when viewing a course
        if (!currentObject.equals(CourseUnit.class)) {
            enrollBtn.setDisable(true);
        } else {
            enrollBtn.setDisable(false);
        }
        // clicked object is a CourseUnit
        if (currentObject.equals(CourseUnit.class)) {
            // Cast to courseUnit
            CourseUnit course = (CourseUnit) obj;
            this.currentCourse = course;
            // set description

            infoBox.getEngine()
                    .loadContent(course.getName() + "\n" + course.getCode() + "\n" + course.getDescription());

        } else if (currentObject.equals(StudyModule.class)) {
            StudyModule studyModule = (StudyModule) obj;
            this.currentStudyModule = studyModule;
            this.currentCourse = null;
            infoBox.getEngine().loadContent(studyModule.getName() + "\n" + studyModule.getDescription());
        } else {
            currentCourse = null;
            infoBox.getEngine().loadContent("");
        }
    }

    /**
     * Method for getting current StudyModule user has selected
     *
     * @return StudyModule
     */
    public StudyModule getCurrentStudyModule() {
        return this.currentStudyModule;
    }

    /**
     * Method for initializing treeView
     */
    public void loadTreeView() {
        TreeItem<TreeViewObject> rootItem = new TreeItem<>();
        rootItem.setExpanded(true);
        rootItem.setValue(degree);

        loadTreeRecr(degree, rootItem);

        treeView.setMinWidth(400);
        treeView.getSelectionModel().selectedItemProperty().addListener(
                (observable, oldValue, newValue) -> {
                    if (newValue != null) {
                        handleMouseClickOnCourse(newValue.getValue());
                    }
                });

        treeView.setRoot(rootItem);

    }

    /**
     * Recursive method for loading all treeView modules
     *
     * @param mod current module
     * @param parent treeItem to load modules to
     */
    private void loadTreeRecr(Module mod, TreeItem<TreeViewObject> parent) {

        // load all submodules
        for (var subModule : mod.getModules()) {
            TreeItem<TreeViewObject> subModuleItem = new TreeItem<TreeViewObject>(subModule);

            // recursively load all submodules of current module
            loadTreeRecr(subModule, subModuleItem);
            parent.getChildren().add(subModuleItem);
        }

        // load all courses (if any)
        for (var subCourse : mod.getCourses()) {
            TreeItem<TreeViewObject> subCourseItem = new TreeItem<TreeViewObject>(subCourse);

            parent.getChildren().add(subCourseItem);
        }

    }

}
