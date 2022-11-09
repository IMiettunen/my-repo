package fi.tuni.prog3.sisu;

import javafx.scene.Node;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TreeView;
import javafx.scene.input.KeyCode;
import javafx.stage.Stage;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.testfx.api.FxAssert;
import org.testfx.api.FxRobot;
import org.testfx.framework.junit5.ApplicationExtension;
import org.testfx.framework.junit5.ApplicationTest;
import org.testfx.matcher.control.ComboBoxMatchers;
import org.testfx.matcher.control.LabeledMatchers;
import static org.testfx.matcher.control.LabeledMatchers.hasText;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.testfx.assertions.api.Assertions.assertThat;

/**
 * Class for testing Sisu application
 */
@ExtendWith(ApplicationExtension.class)
public class SisuTest extends ApplicationTest{

    private Sisu sisu;
    public SisuTest() {
    }
    

    @Override
    public void start(Stage stage) throws Exception {

       sisu = new Sisu();
       sisu.start(stage);
       stage.show();
    }

    /**
     * Test for login screen buttons
     * @param robot
     */
    @Test
    public void checkButtons(){

        FxAssert.verifyThat("#login-button", LabeledMatchers.hasText("Log in"));
        FxAssert.verifyThat("#register-button", LabeledMatchers.hasText("New user"));
    }

    /**
     * Test new user creation fields and return button
     * @param robot
     */
    @Test
    public void testNewUserTextFields(FxRobot robot){
         robot.clickOn("#register-button");
         robot.lookup("#name-field").query().isVisible();
         robot.lookup("#studentnumber-field").query().isVisible();
         robot.lookup("#password-field").query().isVisible();
         robot.lookup("#password-field-2").query().isVisible();
         FxAssert.verifyThat("#create-button", LabeledMatchers.hasText("Create user"));
         FxAssert.verifyThat("#return-button", LabeledMatchers.hasText("Return"));
         robot.clickOn("#return-button");
         FxAssert.verifyThat("#login-button", LabeledMatchers.hasText("Log in"));
    }
    
    /**
     * Test the new user creation programmes combobox
     * @param robot
     */
    @Test
    public void testProgrammesCombobox(FxRobot robot){
        robot.clickOn("#register-button");
        FxAssert.verifyThat("#programmes-combobox", ComboBoxMatchers.hasItems(sisu.getAllDegreeProgrammes().size()));
        
        ComboBox<Object> com = robot.lookup("#programmes-combobox").queryComboBox();

        // select first item in combobox (no item selected on default)
        
        robot.clickOn(com);
        robot.type(KeyCode.DOWN);
        assertThat(com, ComboBoxMatchers.hasSelectedItem(sisu.getAllDegreeProgrammes().get(0)));

        robot.clickOn(com);
        robot.type(KeyCode.DOWN,3);
        assertThat(com, ComboBoxMatchers.hasSelectedItem(sisu.getAllDegreeProgrammes().get(3)));
    } 

    /**
     * Tests new user creation and file saving
     * @param robot
     */
    @Test
    public void testNewUserCreation(FxRobot robot){

        String name = "T. Kari";
        String studentnumber = "H123123";
        String password = "password";
        
        // fill fields
        robot.clickOn("#register-button");
        robot.lookup("#name-field").queryTextInputControl().setText(name);
        robot.lookup("#studentnumber-field").queryTextInputControl().setText(studentnumber);
        robot.lookup("#password-field").queryTextInputControl().setText(password);
        robot.lookup("#password-field-2").queryTextInputControl().setText(password);

        // select degree
        ComboBox<Object> com = robot.lookup("#programmes-combobox").queryComboBox();
        robot.clickOn(com);
        robot.type(KeyCode.DOWN, 7);
        robot.type(KeyCode.ENTER);
        robot.clickOn("#create-button");
        
        FxAssert.verifyThat(robot.lookup("#info-label"), hasText("User created succesfully! Press Return."));
        
        // return to log in screen
        robot.clickOn("#return-button");

        // assert that a user was added to users
        assertEquals(1, sisu.getUsers().size());
        // get student object
        Student student = sisu.getUsers().values().iterator().next();

        //check correct info
        assertEquals(name.toUpperCase(), student.getName());
        assertEquals(studentnumber, student.getStdNumber());
        assertEquals(password, student.getPassword());
        assertEquals(sisu.getAllDegreeProgrammes().get(6), student.getProgramme());

    }

    /**
     * Test user creation error message label
     * @param robot
     */
    @Test
    public void checkNewUserErrorMessages(FxRobot robot){
        robot.clickOn("#register-button");

        Label infoLabel = robot.lookup("#info-label").query();

        // no fields filled
        robot.clickOn("#create-button");
        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("All fields must be filled!"));
        
        // all fields filled, incorrect password
        robot.lookup("#password-field").queryTextInputControl().setText("password");
        robot.lookup("#password-field-2").queryTextInputControl().setText("notTheSamePassword");
        robot.lookup("#studentnumber-field").queryTextInputControl().setText("H123");
        robot.lookup("#name-field").queryTextInputControl().setText("test User");
        robot.clickOn("#create-button");
        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("Passwords do not match!"));

        // fixed password, no degree
        robot.lookup("#password-field-2").queryTextInputControl().setText("password");
        robot.clickOn("#create-button");
        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("Select a degreeprogramme!"));

        // degree selected, succesful creation
        ComboBox<Object> com = robot.lookup("#programmes-combobox").queryComboBox();
        robot.clickOn(com);
        robot.type(KeyCode.DOWN);
        robot.type(KeyCode.ENTER);
        robot.clickOn("#create-button");

        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("User created succesfully! Press Return."));

    }

    /**
     * Test login and login error messages
     * @param robot
     */
    @Test
    public void testLogin(FxRobot robot){
        // create new user
        testNewUserCreation(robot);
    
        Label infoLabel = robot.lookup("#login-message-label").query();
        
        // set incorrect username
        robot.lookup("#login-name-field").queryTextInputControl().setText("incorrect");
        robot.clickOn("#login-button");
        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("Unknown username!"));

        // set correct name but incorrect password
        robot.lookup("#login-name-field").queryTextInputControl().setText("T. Kari");
        robot.lookup("#login-password-field").queryTextInputControl().setText("notCorrect");
        robot.clickOn("#login-button");
        FxAssert.verifyThat(infoLabel, LabeledMatchers.hasText("Wrong password!"));

        // fix password and log in
        robot.lookup("#login-password-field").queryTextInputControl().setText("password");
        robot.clickOn("#login-button");
    }

    /**
     * Test the treeview item selection
     * @param robot
     */
    @Test
    public void testTreeView(FxRobot robot){
        // create new user
        testNewUserCreation(robot);

        //log in
        robot.lookup("#login-name-field").queryTextInputControl().setText("T. Kari");
        robot.lookup("#login-password-field").queryTextInputControl().setText("password");
        robot.clickOn("#login-button");

        //
        Node tab = robot.lookup("#program-tab").query();

        robot.clickOn(tab);
        TreeView<TreeViewObject> tree = robot.lookup("#treeview").query();

        DegreeProgramme degree = sisu.getCurrentUser().getProgramme();

        // calculate amount of expanded modules (+1 for degreeprograms)
        assertEquals(tree.getExpandedItemCount(), degree.getModules().size() + degree.getCourses().size() +1);

        // select first course of first modules
        robot.type(KeyCode.TAB);
        robot.type(KeyCode.DOWN);
        robot.type(KeyCode.RIGHT, 4);
        Module selectedModule = degree.getModules().get(0).getModules().get(0);
        assertEquals(selectedModule.getCourses().get(0), tree.getSelectionModel().getSelectedItem().getValue());
    }

    /**
     * Test course selection and enrolling
     * @param robot
     */
    @Test
    public void testCourseEnrolling(FxRobot robot){
        testTreeView(robot);

        // enroll to course and switch tabs and check enrolled courses
        robot.clickOn("#enroll-button");
        robot.clickOn("#profile-tab");
        robot.clickOn("#enrolled-button");

        
        DegreeProgramme degree = sisu.getCurrentUser().getProgramme();
        Module selectedModule = degree.getModules().get(0).getModules().get(0);

        ListView<CourseUnit> list = robot.lookup("#courses-listview").queryListView();
        assertThat(list).hasListCell(selectedModule.getCourses().get(0));
    }

    /**
     * test course enrolling + marking as completed
     * @param robot
     */
    @Test
    public void testCourseCompletion(FxRobot robot){
        testCourseEnrolling(robot);

        DegreeProgramme degree = sisu.getCurrentUser().getProgramme();
        Module selectedModule = degree.getModules().get(0).getModules().get(0);
        
        // mark course as complete
        robot.clickOn("#mark-complete-button");
        assertThat(robot.lookup("#courses-listview").queryListView()).isEmpty();

        // check completed courses
        robot.clickOn("#completed-button");
        assertThat(robot.lookup("#courses-listview").queryListView()).hasListCell(selectedModule.getCourses().get(0));

    }
}
