package fi.tuni.prog3.sisu;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Map;
import java.util.TreeMap;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Class for reading stored data, saving data and initializing some main class
 * attributes
 *
 * @author ilari
 */
public class FileHandler {

    FileHandler() {

    }

    /**
     * Method for saving student data in json file. Already saved data will be
     * read and re-saved with new and modified data.
     *
     * @param users - TreeMap for storing Students under their name.
     */
    public void writeRegister(TreeMap<String, Student> users) {

        JSONArray jsonarray = new JSONArray();

        String fileName = "register.json";

        for (Map.Entry<String, Student> entry : users.entrySet()) {
            JSONObject jsonObj = new JSONObject();
            jsonObj.put("name", entry.getValue().getName());
            jsonObj.put("student number", entry.getValue().getStdNumber());
            jsonObj.put("degree programme", entry.getValue().getProgramme().getName());
            jsonObj.put("password", entry.getValue().getPassword());
            jsonObj.put("credits", entry.getValue().getCredits());

            JSONArray enrolled = new JSONArray(entry.getValue().getEnrolledCourses());

            JSONArray completed = new JSONArray(entry.getValue().getCompletedCourses());

            jsonObj.put("enrolledCourses", enrolled);
            jsonObj.put("completedCourses", completed);
            jsonarray.put(jsonObj);
        }
        try (PrintWriter out = new PrintWriter(new FileWriter(fileName))) {
            out.write(jsonarray.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    /**
     * Method for reading previously saved student data from register.
     *
     * @param programmes
     * @param filename
     * @return
     */
    public TreeMap<String, Student> readRegister(ArrayList<DegreeProgramme> programmes, String filename) throws FileNotFoundException, IOException {
        StringBuilder contentBuilder = new StringBuilder();
        TreeMap<String, Student> users = new TreeMap<>();

        File directory = new File(filename);

        if (!directory.exists()) {
            String filedata = "";
            try (FileOutputStream fos = new FileOutputStream(filename)) {
                fos.write(filedata.getBytes());
                fos.flush();
            }
            return users;
        }

        String fileContent;

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {

            String content;
            while ((content = br.readLine()) != null) {
                contentBuilder.append(content);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        fileContent = contentBuilder.toString();

        JSONArray jsonArray;
        if (!fileContent.isEmpty()) {
            jsonArray = new JSONArray(fileContent);
        } else {
            return users;
        }

        if (jsonArray.length() != 0) {
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject obj = jsonArray.getJSONObject(i);
                JSONArray enrolled = obj.getJSONArray("enrolledCourses");
                JSONArray completed = obj.getJSONArray("completedCourses");
                String name = obj.getString("name");
                String studentnumber = obj.getString("student number");
                String password = obj.getString("password");
                String progName = obj.getString("degree programme");
                //DegreeProgramme programme;
                Student newStudent;
                for (var prog : programmes) {
                    if (prog.getName().equals(progName)) {
                        newStudent = new Student(name, studentnumber, password, prog);
                        users.put(name, newStudent);

                        if (!enrolled.isEmpty()) {
                            for (int x = 0; x < enrolled.length(); x++) {
                                JSONObject eC = enrolled.getJSONObject(x);

                                CourseUnit course = new CourseUnit();

                                // fetch course name
                                course.setName(eC.getString("name"));

                                // fetch course description
                                if (!eC.isNull("description")) {
                                    course.setDescription(eC.getString("description"));
                                }

                                // set outcome
                                if (!eC.isNull("outcomes")) {
                                    course.setOutcome(eC.getString("outcomes"));
                                }
                                // set max and min credits
                                course.setMinCredits(eC.getInt("minCredits"));
                                course.setMaxCredits(eC.getInt("maxCredits"));

                                // set groupId
                                course.setGroupId(eC.getString("groupId"));

                                // set code
                                course.setCode(eC.getString("code"));

                                newStudent.enrollToCourse(course);
                            }
                        }

                        if (!completed.isEmpty()) {
                            for (int y = 0; y < completed.length(); y++) {

                                JSONObject cC = completed.getJSONObject(y);

                                CourseUnit course = new CourseUnit();

                                // fetch course name
                                course.setName(cC.getString("name"));

                                // fetch course description
                                if (!cC.isNull("description")) {
                                    course.setDescription(cC.getString("description"));
                                }

                                // set outcome
                                if (!cC.isNull("outcomes")) {
                                    course.setOutcome(cC.getString("outcomes"));
                                }
                                // set max and min credits
                                course.setMinCredits(cC.getInt("minCredits"));
                                course.setMaxCredits(cC.getInt("maxCredits"));

                                // set groupId
                                course.setGroupId(cC.getString("groupId"));

                                // set code
                                course.setCode(cC.getString("code"));

                                newStudent.completeCourse(course);

                            }
                        }
                        break;
                    }
                }

            }
        }
        return users;
    }

    /**
     * Method for initializing "accounts" TreeMap containing username-password
     * key-value pairs
     *
     * @param users
     * @param accounts
     * @return
     */
    public TreeMap<String, String> initAccounts(TreeMap<String, Student> users, TreeMap<String, String> accounts) {
        users.entrySet().forEach(entry -> {
            accounts.put(entry.getKey(), entry.getValue().getPassword());
        });
        return accounts;
    }
}
