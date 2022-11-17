/* Class MainWindow
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
 *
 * Ohjelma on muistipeli, johon voi osallistua 2-n pelaajaa. Pelin alussa valitaan korttien määrä.
 * Pelaajat kääntävät kortteja vuorotellen ja saavat pisteitä löydetyistä pareista. Peli
 * laskee pisteitä, mittaa peliin kulunutta aikaa ja kertoo lopussa kuka voitti pelin millä pisteillä.
*/

#ifndef MAINWINDOW_HH
#define MAINWINDOW_HH

#include "player.hh"
#include "scorewindow.hh"
#include <QMainWindow>
#include <QGraphicsScene>
#include <unordered_map>
#include <vector>
#include <QPushButton>


using namespace std;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void calculate_factors();   //Laskee pelilaudan muodostamiseen tarvittavat lähimmät tekijät

    void init_cards();          //Alustaa pelilaudan korteilla ja kortit symboleilla

    void create_symbols();      //"Luo" symbolit ja tallentaa ne

    bool two_cards_open();      //Tarkistaa onko kaksi korttia käännettynä samaan aikaan

    void close_cards();         //Sulkee ei-parilliset kortit ajastimen kuluttua loppuun

    bool is_pair();             //Kertoo onko kaksi käännettyä korttia pari

    void in_turn();             //Kertoo kuka pelaajista on vuorossa

    void create_scoreboard(const int row = 0); //Tuottaa tulostaulun pelilaudan viereen

    void refresh_scoreboard(Player*); //Päivittää tulostaulun pelaajien keräämien pisteiden mukaan

    vector<string> winner_is(); //Palauttaa vectorissa voittajan/voittajien nimet

    void pair_found();          //Toteuttaa löydetyn parin korteille toimenpiteitä

    void new_game();            //Alustaa pelilaudan, attribuutit ja kaiken muun tarvittavan uutta erää varten



private slots:

   void on_playButton_clicked(); //Toteuttaa pelin aloittamisen vaatimia toimenpiteitä play nappulan painalluksesta

   void handleCardClick();      //Käsitelee korttien painallukset

   void on_addButton_clicked(); //Luo pelaajat

   void set_display();          //Päivittää pelikelloa


private:
    Ui::MainWindow *ui;
    QTimer *timer;          //Ajastin käännettyjen korttien sulkemista varten
    QTimer *gametime;       //Ajastin peiin kulunutta aikaa varten
    ScoreWindow *popup1;    //Pop up tulostaulu


    int card_nbr_ = 0;      //Pelilaudan korttien määrä
    int cards_found_ = 0;   //Löydettyjen korttien määrä
    int player_nbr_ = 0;    //Pelaajien määrä
    int columns_ = 0;       //Sarakkeiden määrä
    int rows_ = 0;          //Rivien määrä
    int turn_ = -1;         //Vuorossa oleva pelaaja
    unsigned int winning_points_ = 0; //Pelin voittanut pistemäärä

    unordered_map<QPushButton*, QString> cards_; //Mappi pelikorteille ja symboleille
    vector<char> symbols_;  //vectori symboleille
    vector<Player*> players_; //Vektori pelaajille
    vector<QPushButton*> open_cards_; //Avatut kortit ovat väliaikaisesti tässä vektorissa

};
#endif // MAINWINDOW_HH
