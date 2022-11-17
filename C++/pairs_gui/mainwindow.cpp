/* Class MainWindow
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
 *
*/

#include "mainwindow.hh"
#include "ui_mainwindow.h"
#include <QGridLayout>
#include <QGraphicsView>
#include <algorithm>
#include <random>
#include <chrono>
#include <QTimer>
#include <thread>
#include <QLCDNumber>
#include <QApplication>
#include <QMessageBox>




using namespace std;
using namespace std::chrono;
using namespace std::this_thread;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::set_display()
{
    int sec = ui->gametimer->intValue();
    ui->gametimer->display(sec+1);
}

void MainWindow::init_cards()
{
    //Luodaan GridLayout johon kortit voidaan sijoittaa
    QGridLayout *Glayout = new QGridLayout(ui->gameboard);
    Glayout->setSpacing(10);




    //Luodaan pelikortit loopissa ja sijoitetaan ne gridiin jonka sivujen pituus tulee korttien
    //määrän lähimmistä tekijöistä. Symbolit saadaan vektorista johon ne on luotu aiemmin
    //Nappulat yhdistetään handlecardclick slotiin.
    int yc = 0;
    int x = 0;
    for(int i = 0; i < rows_ ; ++i ){
        int xc = 0;
        for(int j = 0; j <columns_ ; ++j){
            char symbol_in_turn = symbols_.at(x);
            QString letter = "";
            letter = symbol_in_turn;
            QPushButton* pushButton = new QPushButton(this);
            pushButton->setMaximumWidth(75);
            pushButton->setMinimumHeight(40);
            cards_[pushButton] = letter;
            Glayout->addWidget(pushButton, xc, yc, 1, 1);
            connect(pushButton, &QPushButton::clicked,
                    this, &MainWindow::handleCardClick);
            ++xc;
            ++x;
        }++yc;
    }

}

void MainWindow::create_symbols()
{
   int card_amount =  card_nbr_;

   for(int i = 0, c = 'A'; i < card_amount; ++c)
   {
       // Lisätään kaksi samaa korttia (parit) pelilaudalle
       for(int j = 0; j < 2 ; ++j)
       {
           symbols_.push_back(c);
       } i+= 2;

       //Sekoitetaan symbolivektori kellosta otetun seedin mukaan, jotta
       //ne voi myöhemmin poimia järjestyksessä vekorista
   }unsigned seed = chrono::system_clock::now().time_since_epoch().count();
   auto rng = default_random_engine {seed};
   shuffle(begin(symbols_), end(symbols_), rng);
}

bool MainWindow::two_cards_open()
{
    int count_open = 0;
    unordered_map<QPushButton*, QString>::iterator i;
    for ( i = cards_.begin(); i != cards_.end(); ++i ){
        if( i->first->text() != ""){
            count_open += 1;
        }
    //Jos pelilaudalla on kortteja avoinna enemmän kuin jo löydetyt + 1
    //Niin silloin paluuarvo on true ja kortit sulkeutuvat jos ne eivät olleet pari
    }if ( count_open > cards_found_ + 1){
        return true;
    }return false;
}

void MainWindow::calculate_factors()
{
    //Lasketaan lähimmät yhteiset tekijät jotta pelikortit saataisiin
    //fiksuun muotoon pelilaudalle
    unsigned int card_amount = card_nbr_;
    for(unsigned int i = 1; i * i <= card_amount; ++i)
    {
        if(card_nbr_ % i == 0)
        {
            rows_ = i;
        }
    }
    columns_ = card_nbr_ / rows_;
}

void MainWindow::on_playButton_clicked()
{
    if (players_.size() < 2){
        return;
    }
    //Luodaan ja yhdistetään ajastimet slotteihinsa
    timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &MainWindow::close_cards);

    gametime = new QTimer(this);
    connect(gametime, &QTimer::timeout, this, &MainWindow::set_display);

    //Alustetaan alkuarvoja pelille, laitetaan pelilauta kuntoon ja
    //Käynnistetään pelikello
    player_nbr_ = players_.size();
    card_nbr_ = ui->cardamountspinBox->value();
    ui->cardamountspinBox->setDisabled(true);
    ui->P1lineEdit->setDisabled(true);
    calculate_factors();
    create_symbols();
    init_cards();
    create_scoreboard();
    in_turn();
    ui->playButton->setDisabled(true);
    ui->announceLabel->setText("IN TURN");
    gametime->start(1000);
}

void MainWindow::close_cards()
{
    //Sulkee avatut kortit jotka eivät ollut pari ja pysäyttää kellon
    timer->stop();
    for (QPushButton* i : open_cards_){
        i->setText("");
    }open_cards_.clear();
    in_turn();
}

bool MainWindow::is_pair()
{
    //Taristaa onko kahdessa avatussa kortissa sama symboli
    //palauttaa true jos on
    QPushButton* card1 = open_cards_.at(0);
    QPushButton* card2 = open_cards_.at(1);

    if (cards_.at(card1) != cards_.at(card2)){
        return false;
    }else{
        return true;
    }
}

void MainWindow::pair_found()
{
    //Jos kortit oli pari, niin tämä suorittaa niille toimenpiteitä
    //Disablee ne ja vaihtaa väriä ja lisää pisteitä pelaajalle
    QPushButton* card1 = open_cards_.at(0);
    QPushButton* card2 = open_cards_.at(1);
    for(auto card : {card1,card2}){
        card->setStyleSheet("background-color: green");
        card->setDisabled(true);
    }open_cards_.clear();
    players_.at(turn_)->add_points();
    refresh_scoreboard(players_.at(turn_));
    cards_found_ += 2;
}

void MainWindow::new_game()
{
    //Alustaa kaikki tarvittavat asiat pelilaudalla uutta peliä varten
    //vapauttaa myös muistin niiltä osin kuin mahdollista
    //Nollaa myös MAinWIndow luokan attribuutit
    ui->playButton->setEnabled(true);
    ui->cardamountspinBox->setEnabled(true);
    ui->P1lineEdit->setEnabled(true);
    ui->playernumberlcd->display(0);
    ui->gametimer->display(0);
    ui->inTurn->clear();
    card_nbr_ = 0;
    player_nbr_ = 0;
    columns_ = 0;
    rows_ = 0;
    cards_found_ = 0;
    turn_ = -1;
    winning_points_ = 0;
    for(auto player : players_){
        delete player;
    }for (auto button : cards_){
        delete button.first;
    }
    ui->gameboard->layout()->deleteLater();

    for(auto child : ui->scoreboardwidget->children()){
        delete child;
    }
    ui->scoreboardwidget->layout()->deleteLater();

    cards_.clear();
    symbols_.clear();
    players_.clear();
    open_cards_.clear();


}

void MainWindow::in_turn()
{
    //Selvittää vuorossa olevan pelaajan
    turn_ += 1;
    if (turn_ == player_nbr_ ){
        turn_ = 0;
    }
    string player_name = players_.at(turn_)->get_name();
    QString name = QString::fromStdString(player_name);
    ui->inTurn->setText(name);

}

void MainWindow::create_scoreboard( int row)
{
    //Luo pistetaulun melko samalla tavalla kun pelilaudan
    QGridLayout *scoreboard = new QGridLayout(ui->scoreboardwidget);
    for(auto player : players_){
        string player_name = player->get_name();
        QString name = QString::fromStdString(player_name);
        int player_points = player->number_of_pairs();
        QLabel *nameLabel = new QLabel();
        QLCDNumber *points = new QLCDNumber();
        points->setObjectName(name);
        nameLabel->setText(name);
        points->display(player_points);
        scoreboard->addWidget(nameLabel, row, 0);
        scoreboard->addWidget(points, row, 1);
        ++row;
    }
}

void MainWindow::refresh_scoreboard(Player* player)
{
    //Päivittää pistetaulun, ottaa lähtöarvona pelaaja osoittimen
    //jotta saa selville päivitettävät pisteet
    int player_points = player->number_of_pairs();
    string player_name = player->get_name();
    QString name = QString::fromStdString(player_name);
    QLCDNumber *points = ui->scoreboardwidget->findChild<QLCDNumber*>(name);
    points->display(player_points);
}

vector<string> MainWindow::winner_is()
{
    //Selvittää kaikkien suurimmat pisteet saaneiden nimet ja palauttaa
    //ne vektorissa. Selvittää myös suurimman pistesaaliin ja tallentaa attribuuttiin

    vector<string> winners;
    vector<int> points;
    for(auto player : players_){
        unsigned int pts = player->number_of_pairs();
        points.push_back(pts);
    }winning_points_ = *max_element(points.begin(),points.end());
    unsigned int max_pts = unsigned(winning_points_);

    for(auto player : players_){
        if(player->number_of_pairs() == max_pts){
            winners.push_back(player->get_name());
        }
    }
    return winners;
}

void MainWindow::handleCardClick()
{
    //Toteuttaa toiminnot korttia painaessa
    if(timer->isActive()){  //estää kolmannen kortin avaamisen
        return;
    }
    //Selvittää miltä nappulalta käsky tuli
    QPushButton *btn = qobject_cast<QPushButton *>(sender());
    QString c = btn->text();
    if ( c == ""){
        btn->setText(cards_.at(btn));
        open_cards_.push_back(btn);
    }
    if (two_cards_open()){  //Jos kaksi korttia on auki ja ne eivät ole pari
        if(!is_pair()){     //Ajastin käynnistyy ja sulkee sitten kortit
            timer->start(900);
        }else{
            pair_found();   //Jos pari löytyy tarkitetaan onko se viimeinen pari
            if( cards_found_ == card_nbr_){
               gametime->stop();//Jos on, kello pysähtyy ja pop up tulostaulu ilmestyy
               popup1 = new ScoreWindow(winner_is(), winning_points_, ui->gametimer->intValue());
               if(popup1->exec()){  //Jos pelaaja haluaa toisen pelin, pelilauta alustetaan
                  new_game();
               }else{       //Jos ei niin peli päättyy
                  for (auto player : players_){
                      delete player;
                  }close();
               }
            }
        }
    }
}

void MainWindow::on_addButton_clicked()
{
    //Luo Player olioita pelin pelaajille ja tallentaa nämä
    //vektoriin. Näyttää lcd numerolla pelaajien määrän
    QString player_name = ui->P1lineEdit->text();
    string name = player_name.toStdString();
    Player* player1 = new Player(name);
    players_.push_back(player1);
    player_nbr_ += 1;
    ui->playernumberlcd->display(player_nbr_);
}
