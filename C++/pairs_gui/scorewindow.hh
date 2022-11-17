/* Class ScoreWindow
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
 *
 * Popup ikkuna tulosten esittämistä varten. Kertoo pelin voittajan/voittajat,
 * pistemäärän jolla voitettiin ja peliin kuluneen ajan sekunteina. Tässä ikkunassa
 * pelaaja voi valita haluaako jatkaa peliä, mikä johtaa pelin alustamiseen vai
 * haluaako pelaaja lopettaa, mikä lopettaa ohjelman suorituksen
*/

#ifndef SCOREWINDOW_HH
#define SCOREWINDOW_HH

#include <vector>
#include <QDialog>
using namespace std;

namespace Ui {
class ScoreWindow;
}

class ScoreWindow : public QDialog
{
    Q_OBJECT

public:
    explicit ScoreWindow(vector<string> winners, int win_pts_, int time_spent, QWidget *parent = nullptr, bool tie = false);
    ~ScoreWindow();


private slots:

private:
    Ui::ScoreWindow *ui;

    bool tie_;              //kertoo onko voittajia useampi
    vector<string> winners_; //voittajan/voittajien nimet
    int win_pts_;           //pisteet joilla peli voitettiin
    int time_spent;         //Peliin kulunut aika

    // Funktio tuottaa pop up ikkunan sisältöineen sen mukaan, oliko voittajia yksi vai useampi
    void announce_winners();

};


#endif // SCOREWINDOW_HH
