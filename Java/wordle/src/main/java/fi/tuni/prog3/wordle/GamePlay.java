/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package fi.tuni.prog3.wordle;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.TreeSet;

/**
 *
 * @author ilari
 */
public class GamePlay {
    private String answer;
    private int gCount = 0;
    private int columns;
    private final ArrayList<String> wordList = new ArrayList<>();
    private int firstEmpty;
    private final TreeSet guessedRight = new TreeSet();
    private int gameStatus = 0;
    private boolean eraseable = false;
    
    public GamePlay(String fileName)throws IOException{

        File file = new File(fileName);
        BufferedReader br = new BufferedReader(new FileReader(file));

        String line;
        while ((line = br.readLine()) != null) {
            this.wordList.add(line.toUpperCase());
        }
        br.close();
        
        this.answer = this.wordList.get(0);
        this.wordList.remove(0);
        this.columns = this.answer.length();
        this.firstEmpty = 0;
        this.gameStatus = 1;
        
    }
    public int getCol(){
        return this.columns;
    }
    public int getEmptySpace(int i){
        switch (i) {
            case 1:
                this.firstEmpty += 1;
                return this.firstEmpty-1;
            case 0:
                return this.firstEmpty;
            default:
                this.firstEmpty -=1;
                return this.firstEmpty;
        }
    }
    public int getIdCol(String id){
        String[] tmp = id.split("_");
        return Integer.parseInt(tmp[1]);
    }
    public int getIdRow(String id){
        String[] tmp = id.split("_");
        return Integer.parseInt(tmp[0]);
    }
    
    public int getGameStatus(){
        return this.gameStatus;
    }
    public void setStatus(int status){
            this.gameStatus = status;
    }

    public void raiseGuessCount(){
        this.gCount += 1;
    }
    
    public void disableErase(){
        this.eraseable = false;
    }
    public void enableErase(){
        this.eraseable = true;
    }
    public boolean getEraseable(){
        return this.eraseable;
    }
    
    public Boolean linesFirst(String id){
        int idC=this.getIdCol(id);
        return idC == 0;
    }
    public Boolean linesLast(String id){
        int idC=this.getIdCol(id);
        return idC-(this.columns-1) == 0;
    }
    
    public int checkChar(String id, String a){
        int col = this.getIdCol(id);
        int row = this.getIdRow(id);
        String A = a.toUpperCase();
        char b = A.charAt(0);
        
        if(b == this.answer.charAt(col)){
            guessedRight.add(row*this.columns+col);
            return 2;
        }else if(this.answer.contains(A)){
            return 1;
        }else{
            return 0;
        }   
    }
    
    public boolean checkWin(String id){
        int idR=this.getIdRow(id);
        int idC=this.getIdCol(id);
        int indexEnd = idR*this.columns+idC;
        int indexStart = indexEnd-(this.columns-1);
        Boolean victory = true;
        while(indexStart < indexEnd+1){
            if(!this.guessedRight.contains(indexStart)){
                victory = false;
            }
            indexStart += 1;
        }
        return victory;
    }
    public boolean checkLose(){
        return this.gCount == 6;
    }   
    
    public void restart(){

        this.answer = this.wordList.get(0);
        this.wordList.remove(0);
        this.columns = this.answer.length();
        this.firstEmpty = 0;
        this.gameStatus = 1;
        this.gCount = 0;
        this.guessedRight.clear();
        this.eraseable = false;
    }
}
