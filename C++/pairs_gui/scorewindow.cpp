/* Class ScoreWindow
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
 *
*/

#include "scorewindow.hh"
#include "player.hh"
#include "ui_scorewindow.h"

ScoreWindow::ScoreWindow(vector<string> winners, int winning_pts_, int time_spent, QWidget *parent, bool tie) :
    QDialog(parent),
    ui(new Ui::ScoreWindow), tie_(tie), winners_(winners), win_pts_(winning_pts_), time_spent(time_spent)
{
    ui->setupUi(this);

    announce_winners();

}

ScoreWindow::~ScoreWindow()
{
    delete ui;
}

void ScoreWindow::announce_winners()
{
    if (winners_.size() != 1){
        tie_ = true;
    }
    if(!tie_){
        QString winner = QString::fromStdString(winners_.at(0));
        ui->winnerIsLabel->setText("Winner is:");
        ui->winnernames->setText(winner);
        ui->winningpoints->display(win_pts_);
    }else{
        ui->winnerIsLabel->setText("It's a tie between");
        for(string i : winners_){
            QString winner = QString::fromStdString(i);
            ui->winnernames->append(winner);
            ui->winningpoints->display(win_pts_);
        }

    }ui->lcdNumber->display(time_spent);
}
