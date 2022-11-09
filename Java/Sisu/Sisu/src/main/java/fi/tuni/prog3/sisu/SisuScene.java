package fi.tuni.prog3.sisu;

import java.util.ArrayList;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.VPos;

import javafx.scene.Scene;
import javafx.scene.control.Button;

import javafx.scene.control.Label;
import javafx.scene.control.ListView;

import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;

import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.control.TreeView;

import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;

import javafx.scene.web.WebView;

/**
 * Creates and handles scene and its elements for user interface after user has
 * logged in
 *
 *
 */
public class SisuScene {

    private Student currentStudent;
    private Button completeCourseBtn;
    private CourseUnit selectedCourse;
    private ListView<CourseUnit> coursesListView;
    private Label listViewTitle = new Label();
    private final String style = getClass().getResource("/SisuStyle.css").toExternalForm();
    private Label labelProgress = new Label();
    private TreeViewLoader loader;

    /**
     * Empty constructor
     */
    SisuScene() {
    }

    /**
     * return TreeViewLoader object
     *
     * @return TreeViewLoader
     */
    public TreeViewLoader geTreeViewLoader() {
        return this.loader;
    }

    /**
     * Loads a listview that shows students completed courses
     *
     * @param infoBox for loading completed courses
     */
    private void completedBtnClicked(VBox infoBox) {
        coursesListView = new ListView<>();
        coursesListView.setId("courses-listview");
        coursesListView.setMinWidth(450);
        for (CourseUnit c : currentStudent.getCompletedCourses()) {
            coursesListView.getItems().add(c);
        }

        infoBox.getChildren().clear();
        listViewTitle.setText("Completed courses");
        infoBox.getChildren().add(listViewTitle);
        infoBox.getChildren().addAll(coursesListView);

        coursesListView.getSelectionModel().select(0);
    }

    /**
     * Loads a listview that shows students enrolled courses
     *
     * @param infoBox for loading enrolled courses
     */
    private void enrolledCoursesBtnClicked(VBox infoBox) {
        coursesListView = new ListView<>();
        coursesListView.setId("courses-listview");
        coursesListView.setMinWidth(450);
        for (CourseUnit c : currentStudent.getEnrolledCourses()) {
            coursesListView.getItems().add(c);
        }
        infoBox.getChildren().clear();
        listViewTitle.setText("Enrolled courses");
        infoBox.getChildren().add(listViewTitle);
        infoBox.getChildren().addAll(coursesListView);
        infoBox.getChildren().add(completeCourseBtn);

        coursesListView.getSelectionModel().select(0);
    }

    /**
     * Handle complete course button click Moves course from enrolled courses to
     * completed courses
     *
     * @param currentUser Current student
     * @param infoBox infobox for refreshing the view
     */
    private void completeCourseBtnClicked(Student currentUser, VBox infoBox) {
        // get current course
        selectedCourse = coursesListView.getSelectionModel().getSelectedItem();

        if (selectedCourse != null) {
            currentStudent.completeCourse(selectedCourse);
        }

        // refresh list view
        enrolledCoursesBtnClicked(infoBox);
        this.labelProgress.setText(currentUser.getCredits() + "/" + currentUser.getProgramme().getMinCredits());

    }

    /**
     * Method to create tab and set its contents to display Student profile
     *
     * @param currentUser - Student object, Student who is logged in
     * @return - Tab that can later be added to TabPane
     */
    public Tab profileTab(Student currentUser) {

        Tab tabProfile = new Tab("Profile");
        tabProfile.setId("profile-tab");
        HBox profileLayout = new HBox();

        GridPane gridProfile = new GridPane();
        gridProfile.setHgap(10);
        gridProfile.setVgap(15);

        VBox btnVbox = new VBox();
        btnVbox.setSpacing(3);
        btnVbox.setPrefWidth(100);
        Button completedBtn = new Button("Completed");
        completedBtn.setId("completed-button");
        Button enrolledBtn = new Button("Enrolled");
        enrolledBtn.setId("enrolled-button");
        enrolledBtn.setMinWidth(btnVbox.getPrefWidth());
        completedBtn.setMinWidth(btnVbox.getPrefWidth());
        btnVbox.getChildren().addAll(enrolledBtn, completedBtn);

        completeCourseBtn = new Button("Mark as complete");
        completeCourseBtn.setId("mark-complete-button");
        VBox courseInfoBox = new VBox();
        courseInfoBox.setId("courseInfoBox");
        courseInfoBox.setMinWidth(350);
        GridPane.setHalignment(courseInfoBox, HPos.RIGHT);
        GridPane.setValignment(courseInfoBox, VPos.CENTER);

        Label labelName = new Label(currentUser.getName());
        labelName.setWrapText(true);
        Text textName = new Text("Name:");
        textName.setUnderline(true);
        gridProfile.add(textName, 1, 1);
        gridProfile.add(labelName, 1, 2);

        Label labelStudentNumber = new Label(currentUser.getStdNumber());
        labelStudentNumber.setWrapText(true);
        Text textStudentNumber = new Text("Student number:");
        textStudentNumber.setUnderline(true);

        gridProfile.add(textStudentNumber, 1, 3);
        gridProfile.add(labelStudentNumber, 1, 4);

        Label labelProgramme = new Label(currentUser.getProgramme().toString());
        labelProgramme.setMaxWidth(500);
        labelProgramme.setWrapText(true);
        Text textProgramme = new Text("Degree programme:");
        textProgramme.setUnderline(true);

        gridProfile.add(textProgramme, 1, 5);
        gridProfile.add(labelProgramme, 1, 6, 2, 1);

        this.labelProgress.setText(currentUser.getCredits() + "/" + currentUser.getProgramme().getMinCredits() + " credits");
        Text textProgress = new Text("Progress:");
        textProgress.setUnderline(true);

        gridProfile.add(textProgress, 1, 7);
        gridProfile.add(this.labelProgress, 1, 8);

        Text textCourses = new Text("Courses:");
        textCourses.setUnderline(true);

        gridProfile.add(textCourses, 1, 9);
        gridProfile.add(btnVbox, 1, 10);

        completedBtn.setOnAction((event) -> completedBtnClicked(courseInfoBox));
        enrolledBtn.setOnAction((event) -> enrolledCoursesBtnClicked(courseInfoBox));
        profileLayout.getChildren().addAll(gridProfile, courseInfoBox);

        completeCourseBtn.setOnAction((event) -> completeCourseBtnClicked(currentUser, courseInfoBox));
        coursesListView = new ListView<>();
        coursesListView.setId("courses-listview");
        tabProfile.setContent(profileLayout);
        tabProfile.setClosable(false);

        return tabProfile;
    }

    /**
     * Enroll to course button handler
     *
     * @param treeView TreeViewLoader object for getting current course
     * @param student Current Student
     */
    private void enrollBtnClicked(TreeViewLoader treeView, Student student) {
        CourseUnit current = treeView.getCurrentCourse();
        if (current != null) {
            student.enrollToCourse(current);
        }

    }

    /**
     * Toggle button handler for viewing outcomes
     *
     * @param tree TreeViewLoader object for getting current object
     * @param box webView for loading text
     */
    private void outcomeToggled(TreeViewLoader tree, WebView box) {
        if (tree.getCurrentObjectClass() != null) {
            if (tree.getCurrentObjectClass().equals(CourseUnit.class)) {
                if (tree.getCurrentCourse() != null) {
                    CourseUnit course = tree.getCurrentCourse();
                    box.getEngine().loadContent(course.getName() + "\n" + course.getCode() + "\n" + course.getOutcomes());

                }
            } else if (tree.getCurrentObjectClass().equals(StudyModule.class)) {
                if (tree.getCurrentStudyModule() != null) {
                    StudyModule module = tree.getCurrentStudyModule();
                    box.getEngine().loadContent(module.getName() + "\n" + module.getOutcomes());
                }
            }
        }

    }

    /**
     * Toggle button handler for viewing description
     *
     * @param tree TreeViewLoader object for getting current object
     * @param box webView for loading text
     */
    private void descriptionToggled(TreeViewLoader tree, WebView box) {
        if (tree.getCurrentObjectClass() != null) {
            if (tree.getCurrentObjectClass().equals(CourseUnit.class)) {
                if (tree.getCurrentCourse() != null) {
                    CourseUnit course = tree.getCurrentCourse();
                    box.getEngine().loadContent(course.getName() + "\n" + course.getCode() + "\n" + course.getDescription());
                }
            } else if (tree.getCurrentObjectClass().equals(StudyModule.class)) {
                if (tree.getCurrentStudyModule() != null) {
                    StudyModule module = tree.getCurrentStudyModule();
                    box.getEngine().loadContent(module.getName() + "\n" + module.getDescription());
                }
            }
        }

    }

    /**
     * Method to create tab and set its contents to display the structure of
     * degree program and course descriptions
     *
     * @param degrees - ArrayList of all degree programmes
     * @param currentStudent - Student object, Student who is logged in
     * @return - Tab that can be added to TabPane
     * @throws Exception
     */
    public Tab programmeTab(ArrayList<DegreeProgramme> degrees, Student currentStudent) throws Exception {
        Tab tabProgram = new Tab("Program");
        tabProgram.setId("program-tab");
        HBox programLayout = new HBox();
        VBox sideBox = new VBox(10);
        sideBox.getStyleClass().add("VBox");
        sideBox.setPadding(new Insets(0, 10, 10, 10));

        SisuApi api = new SisuApi();
        HBox toggleButtonBox = new HBox(10);
        toggleButtonBox.setPadding(new Insets(0, 0, 0, 10));

        ToggleGroup group = new ToggleGroup();
        ToggleButton descToggle = new ToggleButton("Description");
        ToggleButton outcomesToggle = new ToggleButton("Outcomes");
        descToggle.getStyleClass().add("toggleButton");
        outcomesToggle.getStyleClass().add("toggleButton");

        descToggle.setToggleGroup(group);
        outcomesToggle.setToggleGroup(group);
        descToggle.setSelected(true);

        toggleButtonBox.getChildren().add(descToggle);
        toggleButtonBox.getChildren().add(outcomesToggle);
        sideBox.getChildren().add(toggleButtonBox);

        Button enrollBtn = new Button("Enroll");
        enrollBtn.setId("enroll-button");
        enrollBtn.setDisable(true);

        // infobox for course info
        // webView allows for html text loading
        WebView infoBox = new WebView();
        infoBox.setScaleX(0.95);

        DegreeProgramme degree = currentStudent.getProgramme();

        // fetch api for degree submodules
        api.fetchModules(degree.getId(), degree);

        // load tree view element
        TreeViewLoader treeView = new TreeViewLoader(degree, infoBox, enrollBtn, descToggle);
        this.loader = treeView;
        treeView.loadTreeView();

        TreeView<TreeViewObject> treeObject = treeView.getTreeViewObject();
        treeObject.setMinWidth(500);
        treeObject.getStyleClass().add("treeView");
        programLayout.getChildren().add(treeObject);
        sideBox.getChildren().add(infoBox);
        sideBox.getChildren().add(enrollBtn);
        programLayout.getChildren().add(sideBox);
        tabProgram.setContent(programLayout);
        enrollBtn.setOnAction((event) -> {
            enrollBtnClicked(treeView, currentStudent);
        });

        outcomesToggle.setOnAction((event) -> outcomeToggled(treeView, infoBox));
        descToggle.setOnAction((event) -> descriptionToggled(treeView, infoBox));
        tabProgram.setClosable(false);

        return tabProgram;
    }

    /**
     * Method to create scene for main UI. Displays two tabs containing student
     * profile and degree program structure.
     *
     * @param currentUser - Student object, student who is logged in
     * @param degrees - ArrayList containing all degree programmes
     * @return - Scene for stage2 showing after logging in
     * @throws Exception
     */
    public Scene userScene(Student currentUser, ArrayList<DegreeProgramme> degrees) throws Exception {
        TabPane tabPane = new TabPane();
        Tab tabProfile = this.profileTab(currentUser);
        Tab tabProgram = this.programmeTab(degrees, currentUser);
        this.currentStudent = currentUser;
        tabPane.getTabs().add(tabProfile);
        tabPane.getTabs().add(tabProgram);

        Scene scene = new Scene(tabPane, 900, 480);
        scene.getStylesheets().add(this.style);

        return scene;
    }

}
