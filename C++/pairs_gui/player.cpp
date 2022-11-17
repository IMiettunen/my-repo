/* Class Player
 * ----------
 * Ohjelman kirjoittaja
 * Nimi: Ilari Miettunen
 * Opiskelijanumero: 050371213
 * Käyttäjätunnus: nqilmi
 * E-Mail: ilari.miettunen@tuni.fi
*/

#include "player.hh"
#include <vector>
#include<string>
#include<iostream>
using namespace std;

Player::Player(const string &name):
    name_(name), pts_(0)
{

}

string Player::get_name() const
{   return name_;

}

unsigned int Player::number_of_pairs() const
{   return pts_;

}

void Player::add_points()
{
    pts_ += 1;
}


