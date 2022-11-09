package fi.tuni.prog3.wordle;

import java.io.IOException;
import java.util.ArrayList;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.Border;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.BorderStroke;
import javafx.scene.layout.BorderStrokeStyle;
import javafx.scene.layout.BorderWidths;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;


/**
 * JavaFX Wordle
 */
public class Wordle extends Application {

    @Override
    public void start(Stage stage) throws IOException{
        GamePlay wordle = new GamePlay("words.txt");
        
        
        
        ArrayList<Label> squares = new ArrayList<>();
        
        stage.setTitle("Wordle");
        
        BorderPane border = new BorderPane();
        
        HBox topHbox = new HBox(10);
        border.setTop(topHbox);
        
        Label msgLbl = new Label("");
        msgLbl.setId("infoBox");
        Button newGame = new Button("Start New Game");
        newGame.setId("newGameBtn");
        newGame.setFocusTraversable(false);
        msgLbl.setPrefHeight(25);
        topHbox.getChildren().addAll(newGame,msgLbl);
        
        GridPane grid = new GridPane();
        grid.setHgap(3);
        grid.setVgap(3);
        grid.setAlignment(Pos.CENTER);
        
        int j = wordle.getCol();
        
        for(int x = 0; x<6 ; x++){
           for(int y = 0; y<j ; y++){
               Label letter = new Label("");
               letter.setId(x+"_"+y);
               letter.setPrefHeight(50);
               letter.setPrefWidth(50);
               letter.setBackground(new Background(new BackgroundFill(Color.WHITE, CornerRadii.EMPTY, Insets.EMPTY)));
               letter.setBorder(new Border(new BorderStroke(Color.BLACK, BorderStrokeStyle.SOLID, CornerRadii.EMPTY,
                        BorderWidths.DEFAULT)));
               squares.add(letter);
               
               letter.setAlignment(Pos.CENTER);
               grid.add(letter, y, x);
           }
        }
        
        border.setCenter(grid);
         
        Scene scene = new Scene(border, 500, 500);
        
        stage.setScene(scene);
        stage.show();
         
        scene.setOnKeyPressed((KeyEvent event) -> {

            switch (event.getCode()) {
                case ENTER:
                    if(wordle.getGameStatus() == 0){
                        int index = wordle.getEmptySpace(0)-1;
                        int indexStart = index-wordle.getCol()+1;
                        wordle.raiseGuessCount();
                        wordle.disableErase();

                        while(indexStart < index+1){
                            Label temp = squares.get(indexStart);
                            int color = wordle.checkChar(temp.getId(),temp.getText());
                            switch (color){
                                case 1:
                                    temp.setBackground(new Background(new BackgroundFill(Color.ORANGE, CornerRadii.EMPTY, Insets.EMPTY)));
                                    break;
                                case 2:
                                    temp.setBackground(new Background(new BackgroundFill(Color.GREEN, CornerRadii.EMPTY, Insets.EMPTY)));
                                    break;
                                default:
                                    temp.setBackground(new Background(new BackgroundFill(Color.GREY, CornerRadii.EMPTY, Insets.EMPTY)));
                                    break;
                            }
                            indexStart +=1;
                        }
                        if (wordle.checkWin(squares.get(index).getId())){
                            msgLbl.setText("Congratulations, you won!");
                        }else if(wordle.checkLose()){
                            msgLbl.setText("Game over, you lost!");
                        }else if(msgLbl.getText().equals("")){
                            wordle.setStatus(1);
                        }
                    }else{
                        msgLbl.setText("Give a complete word before pressing Enter!");
                    }   break;
                case BACK_SPACE:
                    if(wordle.getEraseable()){
                        int index = wordle.getEmptySpace(2);
                        Label temp = squares.get(index);
                        wordle.setStatus(1);
                        temp.setText("");
                        msgLbl.setText("");
                        if(wordle.linesFirst(temp.getId())){
                            wordle.disableErase();
                        }
                    }   break;
                default:
                    if( wordle.getGameStatus() != 0){
                        msgLbl.setText("");
                        wordle.enableErase();
                        String a = event.getText();
                        int index = wordle.getEmptySpace(1);
                        Label temp = squares.get(index);
                        if(wordle.linesLast(temp.getId())){
                            wordle.setStatus(0);
                        }
                        temp.setText(a.toUpperCase());
                    }   break;
            }
        });       
        
        
        newGame.setOnAction((ActionEvent e) -> {
            wordle.restart();
            squares.clear();
            grid.getChildren().removeAll();
            border.getChildren().remove(grid);
            GridPane grid1 = new GridPane();
            grid1.setHgap(3);
            grid1.setVgap(3);
            grid1.setAlignment(Pos.CENTER);
            msgLbl.setText("");
            int j1 = wordle.getCol();
            for (int x = 0; x<6; x++) {
                for (int y = 0; y < j1; y++) {
                    Label letter = new Label("");
                    letter.setId(x+"_"+y);
                    letter.setPrefHeight(50);
                    letter.setPrefWidth(50);
                    letter.setBackground(new Background(new BackgroundFill(Color.WHITE, CornerRadii.EMPTY, Insets.EMPTY)));
                    letter.setBorder(new Border(new BorderStroke(Color.BLACK, BorderStrokeStyle.SOLID, CornerRadii.EMPTY,
                            BorderWidths.DEFAULT)));
                    squares.add(letter);
                    letter.setAlignment(Pos.CENTER);
                    grid1.add(letter, y, x);
                }
            }
            border.setCenter(grid1);
        });
    };

    public static void main(String[] args) {
        launch();
    }

}