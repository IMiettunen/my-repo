package fi.tuni.prog3.sisu;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import org.json.*;

/**
 * Class for fetching degree, module and course information from Sisu
 */
public class SisuApi {

    SisuApi() {

    }

    /**
     * Method for Api query with selected string
     *
     * @param urlString Query url
     * @return String response
     * @throws Exception
     */
    private String fetchString(String urlString) throws Exception {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        BufferedReader in = null;
        String inputLine;
        StringBuffer response = null;
        try {
            // build string from response
            in = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()));

            response = new StringBuffer();
        } catch (IOException e) {
            System.out.println("APi response failed with code: " + connection.getResponseCode());
            return "";
        }

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        // fix for ääkköset
        return response.toString().replace("Ã¤", "ä").replace("Ã¶", "ö");
    }

    /**
     * Method of fetching all degreeprogrammes from Api
     *
     * @return ArrayList<DegreeProgramme> List of all degreeprogrammes
     * @throws Exception
     */
    public ArrayList<DegreeProgramme> fetchDegrees() throws Exception {
        String response = fetchString(
                "https://sis-tuni.funidata.fi/kori/api/module-search?curriculumPeriodId=uta-lvv-2021&universityId=tuni-university-root-id&moduleType=DegreeProgramme&limit=1000");

        if (response.isBlank()) {
            return new ArrayList<>();
        }
        ArrayList<DegreeProgramme> programs = new ArrayList<>();

        JSONObject obj = new JSONObject(response);
        JSONArray jarray = obj.getJSONArray("searchResults");

        for (int i = 0; i < jarray.length(); ++i) {
            JSONObject o = jarray.getJSONObject(i);
            DegreeProgramme program = new DegreeProgramme(o.getString("name"),
                    o.getString("groupId"), o.getString("id"), o.getJSONObject("credits").getInt("min"), o.getString("code"));

            programs.add(program);
        }

        return programs;
    }

    /**
     * Method for getting submodules of selected module
     *
     * @param id module Id
     * @param module module for saving submodules
     * @throws Exception
     */
    public void fetchModules(String id, Module module) throws Exception {
        String response = fetchString("https://sis-tuni.funidata.fi/kori/api/modules/" + id);
        JSONObject obj = new JSONObject(response);

        JSONObject rule = obj.getJSONObject("rule");

        // calls the recursive function
        getSubModulesRecr(rule, module);

    }

    /**
     * Method for getting all submodules and courseunits recursively
     *
     * @param obj JsonObject of current module
     * @param prevModule Module for saving submodules
     * @throws Exception
     */
    public void getSubModulesRecr(JSONObject obj, Module prevModule) throws Exception {

        try {
            String type = obj.getString("type");
            if (type.equals("CreditsRule")) {
                getSubModulesRecr(obj.getJSONObject("rule"), prevModule);

            } else if (type.equals("StudyModule")) {
                StudyModule studyModule = new StudyModule();

                // fetch name
                if (obj.getJSONObject("name").has("fi")) {
                    studyModule.setName(obj.getJSONObject("name").getString("fi"));
                } else {
                    studyModule.setName(obj.getJSONObject("name").getString("en"));
                }

                // fetch description
                if (!obj.isNull("contentDescription")) {
                    if (obj.getJSONObject("contentDescription").has("fi")) {
                        studyModule.setDescription(obj.getJSONObject("contentDescription").getString("fi"));
                    } else {
                        studyModule.setDescription(obj.getJSONObject("contentDescription").getString("en"));

                    }
                }

                //fetch outcomes
                if (!obj.isNull("outcomes")) {
                    if (obj.getJSONObject("outcomes").has("fi")) {
                        studyModule.setOutcomes(obj.getJSONObject("outcomes").getString("fi"));
                    } else {
                        studyModule.setOutcomes(obj.getJSONObject("outcomes").getString("en"));

                    }
                }

                // fetch credits
                studyModule.setMinCredits(obj.getJSONObject("targetCredits").getInt("min"));
                if (!obj.getJSONObject("targetCredits").isNull("max")) {
                    studyModule.setMaxCredits(obj.getJSONObject("targetCredits").getInt("max"));
                }

                // set Id
                studyModule.setGroupId(obj.getString("groupId"));

                getSubModulesRecr(obj.getJSONObject("rule"), studyModule);
                prevModule.addModule(studyModule);
            } else if (type.equals("ModuleRule")) {

                //new query from current module
                String groupId = obj.getString("moduleGroupId");
                String response = fetchString("https://sis-tuni.funidata.fi/kori/api/modules/by-group-id?groupId=" + groupId
                        + "&universityId=tuni-university-root-id");
                JSONArray arr = new JSONArray(response);

                JSONObject newObj = arr.getJSONObject(0);

                getSubModulesRecr(newObj, prevModule);

            } else if (type.equals("CompositeRule")) {

                JSONArray rules = obj.getJSONArray("rules");

                // iterate all rules in composite rule
                for (int i = 0; i < rules.length(); ++i) {
                    JSONObject rule = rules.getJSONObject(i);
                    getSubModulesRecr(rule, prevModule);

                }

            } else if (type.equals("CourseUnitRule")) {

                // new query for course information
                String id = obj.getString("courseUnitGroupId");
                String response = fetchString("https://sis-tuni.funidata.fi/kori/api/course-units/by-group-id?groupId=" + id
                        + "&universityId=tuni-university-root-id");
                JSONArray arr = new JSONArray(response);
                JSONObject newObj = arr.getJSONObject(0);

                CourseUnit course = new CourseUnit();

                // fetch course name
                if (newObj.getJSONObject("name").has("fi")) {
                    course.setName(newObj.getJSONObject("name").getString("fi"));
                } else {
                    course.setName(newObj.getJSONObject("name").getString("en"));
                }

                // fetch course description
                if (!newObj.isNull("content")) {
                    if (newObj.getJSONObject("content").has("fi")) {
                        course.setDescription(newObj.getJSONObject("content").getString("fi"));
                    } else {
                        course.setDescription(newObj.getJSONObject("content").getString("en"));
                    }
                }

                // set outcome
                if (!newObj.isNull("outcomes")) {
                    if (newObj.getJSONObject("outcomes").has("fi")) {
                        course.setOutcome(newObj.getJSONObject("outcomes").getString("fi"));
                    } else {
                        course.setOutcome(newObj.getJSONObject("outcomes").getString("en"));

                    }
                }
                // set max and min credits
                course.setMinCredits(newObj.getJSONObject("credits").getInt("min"));
                if (!newObj.getJSONObject("credits").isNull("max")) {
                    course.setMaxCredits(newObj.getJSONObject("credits").getInt("max"));
                }

                // set groupId
                course.setGroupId(newObj.getString("groupId"));

                // set code
                course.setCode(newObj.getString("code"));

                prevModule.addCourse(newObj.getString("groupId"), course);

            } else if (type.equals("GroupingModule")) {
                GroupingModule groupingModule = new GroupingModule();

                // set name
                if (obj.getJSONObject("name").has("fi")) {
                    groupingModule.setName(obj.getJSONObject("name").getString("fi"));
                } else {
                    groupingModule.setName(obj.getJSONObject("name").getString("en"));
                }

                // set id
                groupingModule.setGroupId(obj.getString("groupId"));
                groupingModule.setId(obj.getString("id"));

                prevModule.addModule(groupingModule);
                getSubModulesRecr(obj.getJSONObject("rule"), groupingModule);

            } else if (type.equals("AnyModuleRule")) {
                Module anyModule = new GroupingModule("anyModule", "", "id");
                prevModule.addModule(anyModule);

            } else if (type.equals("AnyCourseUnitRule")) {
                Module anyModule = new GroupingModule("anyCourse", "", "id");
                prevModule.addModule(anyModule);
            } else {
                System.out.println("unknown type " + type);
            }
        } catch (JSONException e) {
            System.out.println(e);
            System.out.println(obj);
        }

    }
}
