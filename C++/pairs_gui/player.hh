/* Class Player
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
 *
 * Luokka yksittäiselle pelaajalle. Sisätää attribuutteina nimen ja kerätyt pisteet.
 *
*/

#ifndef PLAYER_HH
#define PLAYER_HH

#include <string>
#include <vector>

using namespace std;

class Player
{
public:
    // Rakentaja: luo annetun nimisen pelaajan.

    Player(const string& name);

    // Palauttaa pelaajan nimen.

    string get_name() const;

    // Palauttaa pelaajan tähän asti keräämien parien määrän

    unsigned int number_of_pairs() const;

   //lisää pelaajalle pisteitä
    void add_points();


private:
    // Pelaajan nimi ja kerätyt pisteet
    string name_;
    int pts_;
};

#endif // PLAYER_HH
