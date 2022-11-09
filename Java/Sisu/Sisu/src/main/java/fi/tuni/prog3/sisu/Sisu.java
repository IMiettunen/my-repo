package fi.tuni.prog3.sisu;

import javafx.scene.image.Image;
import java.util.ArrayList;
import java.util.TreeMap;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class Sisu extends Application {

    private ArrayList<DegreeProgramme> degreePrograms;
    private TreeMap<String, String> accounts = new TreeMap<>();
    private Student currentUser;
    private TreeMap<String, Student> users = new TreeMap<>();
    private final String style = getClass().getResource("/SisuStyle.css").toExternalForm();
    private final SisuScene appScene = new SisuScene();

    /**
     * get SisuScene object
     *
     * @return SisuScene
     */
    public SisuScene getSisuScene() {
        return this.appScene;
    }

    /**
     * get all accounts
     *
     * @return TreeMap<String, String> accounts
     */
    public TreeMap<String, String> getAccounts() {
        return this.accounts;
    }

    /**
     * get all users
     *
     * @return TreeMap<String, Student> users
     */
    public TreeMap<String, Student> getUsers() {
        return this.users;
    }

    /**
     * get current student
     *
     * @return Student current student
     */
    public Student getCurrentUser() {
        return this.currentUser;
    }

    /**
     * get all degrees
     *
     * @return ArrayList<DegreeProgramme> all degrees
     */
    public ArrayList<DegreeProgramme> getAllDegreeProgrammes() {
        return this.degreePrograms;
    }

    /**
     *
     * @param stage
     * @throws Exception
     */
    @Override
    public void start(Stage stage) throws Exception {

        final Stage stage2 = new Stage();
        stage.setTitle("SISU");
        stage2.setTitle("SISU");

        Image icon = new Image("/tuni.png");
        stage.getIcons().add(icon);
        stage2.getIcons().add(icon);

        // populate data
        SisuApi api = new SisuApi();
        degreePrograms = api.fetchDegrees();

        //Retrieves userdata ,creates students and initializing accounts 
        FileHandler fileHandler = new FileHandler();
        this.users = fileHandler.readRegister(degreePrograms, "register.json");
        this.accounts = fileHandler.initAccounts(users, accounts);

        //Setup for LogIn scene
        GridPane gridLogIn = new GridPane();
        gridLogIn.setHgap(3);
        gridLogIn.setVgap(3);
        gridLogIn.setAlignment(Pos.CENTER);

        Label logInMessage = new Label("");
        logInMessage.setId("login-message-label");
        gridLogIn.add(logInMessage, 1, 0);
        GridPane.setColumnSpan(logInMessage, 2);

        TextField fieldName = new TextField();
        fieldName.setId("login-name-field");
        Label labelName = new Label("Name:");
        gridLogIn.add(labelName, 1, 2);
        gridLogIn.add(fieldName, 2, 2);

        PasswordField fieldPassword = new PasswordField();
        fieldPassword.setId("login-password-field");
        Label labelPassword = new Label("Password:");
        gridLogIn.add(labelPassword, 1, 3);
        gridLogIn.add(fieldPassword, 2, 3);

        Button btnLogIn = new Button("Log in");
        btnLogIn.setId("login-button");

        Button btnNewUser = new Button("New user");
        btnNewUser.setId("register-button");
        gridLogIn.add(btnLogIn, 1, 4);
        gridLogIn.add(btnNewUser, 2, 4);

        Scene sceneLogIn = new Scene(gridLogIn, 300, 150);
        sceneLogIn.getStylesheets().add(this.style);

        //Setup for NewUser scene.  
        GridPane gridNewUser = new GridPane();
        gridNewUser.setHgap(10);
        gridNewUser.setVgap(3);

        Label newUserMessage = new Label("");
        newUserMessage.setId("info-label");
        gridNewUser.add(newUserMessage, 1, 0);
        GridPane.setColumnSpan(newUserMessage, 3);

        TextField fieldNameNU = new TextField();
        fieldNameNU.setId("name-field");
        fieldNameNU.setPrefWidth(400);
        Label labelNameNU = new Label("Name:");
        labelNameNU.setPrefWidth(200);

        gridNewUser.add(labelNameNU, 1, 2);
        gridNewUser.add(fieldNameNU, 2, 2);

        TextField fieldStudentNumber = new TextField();
        fieldStudentNumber.setId("studentnumber-field");
        fieldStudentNumber.setPrefWidth(400);
        Label labelStudentNumber = new Label("Student number:");
        labelStudentNumber.setPrefWidth(200);

        gridNewUser.add(labelStudentNumber, 1, 3);
        gridNewUser.add(fieldStudentNumber, 2, 3);

        PasswordField fieldPasswordNU = new PasswordField();
        fieldPasswordNU.setId("password-field");
        fieldPasswordNU.setPrefWidth(400);
        Label labelPasswordNU = new Label("Password:");
        labelPasswordNU.setPrefWidth(200);

        gridNewUser.add(labelPasswordNU, 1, 4);
        gridNewUser.add(fieldPasswordNU, 2, 4);

        PasswordField fieldPasswordNU2 = new PasswordField();
        fieldPasswordNU2.setId("password-field-2");
        fieldPasswordNU2.setPrefWidth(400);
        Label labelPasswordNU2 = new Label("Repeat Password:");
        labelPasswordNU2.setPrefWidth(200);

        gridNewUser.add(labelPasswordNU2, 1, 5);
        gridNewUser.add(fieldPasswordNU2, 2, 5);

        Label labelProgram = new Label("Choose Degreeprogram:");
        labelProgram.setPrefWidth(200);

        ObservableList<DegreeProgramme> options = FXCollections.observableArrayList(degreePrograms);
        ComboBox<DegreeProgramme> programs = new ComboBox<DegreeProgramme>(options);

        programs.setId("programmes-combobox");
        programs.setPrefWidth(400);

        gridNewUser.add(labelProgram, 1, 6);
        gridNewUser.add(programs, 2, 6);

        Button btnCreateUser = new Button("Create user");
        btnCreateUser.setId("create-button");
        btnCreateUser.setPrefWidth(200);

        Button btnReturn = new Button("Return");
        btnReturn.setId("return-button");
        btnReturn.setPrefWidth(200);

        HBox hboxBtn = new HBox(10);
        hboxBtn.getChildren().addAll(btnCreateUser, btnReturn);

        gridNewUser.add(hboxBtn, 2, 7);

        Scene sceneNewUser = new Scene(gridNewUser, 600, 200);
        sceneNewUser.getStylesheets().add(this.style);

        //Creating new user if conditions are met. User added to this.users and account info to this.accounts
        btnCreateUser.setOnAction((event) -> {
            if (fieldNameNU.getText().equals("") || fieldStudentNumber.getText().equals("") || fieldPasswordNU.getText().equals("") || fieldPasswordNU2.getText().equals("")) {
                newUserMessage.setText("All fields must be filled!");
            } else if (accounts.containsKey(fieldNameNU.getText().toUpperCase())) {
                newUserMessage.setText("Username exists already! Change name or press Return to log in.");
            } else if (!fieldPasswordNU.getText().equals(fieldPasswordNU2.getText())) {
                newUserMessage.setText("Passwords do not match!");
            } else if (programs.getValue() == null) {
                newUserMessage.setText("Select a degreeprogramme!");
            } else {
                String newName = fieldNameNU.getText().toUpperCase();
                String password = fieldPasswordNU.getText();
                String studentNumber = fieldStudentNumber.getText();

                DegreeProgramme prog = programs.getValue();
                newUserMessage.setText("User created succesfully! Press Return.");
                Student newStudent = new Student(newName, studentNumber, password, prog);
                users.put(newName, newStudent);
                accounts.put(newName, password);

            }
        });

        //Return to log in window and clear fields
        btnReturn.setOnAction((event) -> {
            fieldNameNU.clear();
            fieldPasswordNU.clear();
            fieldPasswordNU2.clear();
            fieldStudentNumber.clear();
            programs.setValue(null);
            newUserMessage.setText("");
            stage.setScene(sceneLogIn);
        });

        //Move to new user window
        btnNewUser.setOnAction((event) -> {
            fieldName.clear();
            fieldPassword.clear();
            logInMessage.setText("");
            stage.setScene(sceneNewUser);
        });

        //Log in, if existing username and right password
        btnLogIn.setOnAction((event) -> {

            // check correct login info
            String username = fieldName.getText().toUpperCase();
            String userPassword = fieldPassword.getText();
            if (accounts.containsKey(username)) {
                if (!accounts.get(username).equals(userPassword)) {
                    logInMessage.setText("Wrong password!");
                } else {
                    currentUser = users.get(username);

                    Scene scene;
                    try {
                        scene = appScene.userScene(this.currentUser, this.degreePrograms);
                        stage2.setScene(scene);
                        stage.close();
                        stage2.show();
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
            } else {
                logInMessage.setText("Unknown username!");
            }
        });

        stage.setScene(sceneLogIn);

        stage.show();

        stage2.setOnCloseRequest((WindowEvent event) -> {
            fileHandler.writeRegister(users);
            Platform.exit();
            System.exit(0);
        });

        stage.setOnCloseRequest((WindowEvent event) -> {
            fileHandler.writeRegister(users);
            Platform.exit();
            System.exit(0);
        });
    }

    public static void main(String[] args) {
        launch();
    }

}
