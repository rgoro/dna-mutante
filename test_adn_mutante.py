#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from adn_mutante import esMutante, ADNException

class TestADNMutante(unittest.TestCase):

    def test_ejemplo1_noMutante(self):
        adn = ["atgcga", "cagtgc", "ttattt", "agacgg", "gcgtca", "tcactg"]

        self.assertFalse(esMutante(adn))

    def test_ejemplo2_mutante(self):
        adn = ["atgcga", "cagtgc", "ttatgt", "agaagg", "ccccta", "tcactg"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosHorizontales(self):
        adn = ["aaaaga", "cagtgc", "ttctat", "agaagg", "ccccta", "tcactg"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosHorizontales_bis(self):
        adn = ["aaaaga", "cagtgc", "ttctat", "agaagg", "tacccc", "tcactg"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosVerticales(self):
        adn = ["actgag", "ggagtt", "attacc", "agcaca", "aatgcc", "actact"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosVerticales_bis(self):
        adn = ["actgcg", "ggagct", "attacc", "agcaca", "aatgac", "actatt"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosDiagonalesIzqDer(self):
        adn = ["actcga", "gatagc", "gtatct", "actaag", "tactcg", "cagatt"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosDiagonalesDerIzq(self):
        adn = ["actggt", "ggcact", "catata", "ttatcg", "catcaa", "aggatc"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dosDiagonalesDerIzq_bis(self):
        adn = ["acgtta", "tactcg", "acttct", "ttacgg", "accgga", "gctata"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_dobleHorizontal(self):
        adn = ["aaaaaa", "cagtgc", "ttctat", "agaagg", "ctccta", "tcactg"]

        self.assertFalse(esMutante(adn))

    def test_seisPorSeis_mayusculasValen(self):
        adn = ["actgag", "gGagtt", "attacc", "agcAca", "AATGCC", "actact"]

        self.assertTrue(esMutante(adn))

    def test_seisPorSeis_letraInvalida(self):
        adn = ["actggt", "ggcact", "catrta", "ttatcg", "catcaa", "aggatc"]

        with self.assertRaises(ADNException) as cm:
            esMutante(adn)

        the_exception = cm.exception
        self.assertEqual(str(the_exception), "Letra inválida: «r»")

    def test_cincoPorCinco_no_mutante(self):
        adn = ["atcag", "tcaat", "caatg", "gatct", "cgcct"]

        self.assertFalse(esMutante(adn))

    def test_cuatroPorCuatro_no_mutante(self):
        adn = ["atca", "tcaa", "caat", "gatc"]

        self.assertFalse(esMutante(adn))

    def test_cuatroPorCuatro_mutante(self):
        adn = ["atca", "tcaa", "caat", "gatc"]

        self.assertFalse(esMutante(adn))

    def test_adn_chico(self):
        adn = ["atc", "gat", "cga"]

        with self.assertRaises(ADNException) as cm:
            esMutante(adn)

        the_exception = cm.exception
        self.assertEqual(str(the_exception), "Secuencia de ADN demasiado chica (N = 3)")

    def test_adn_inconsistente(self):
        adn = ["atct", "gattt", "acga", "aatc"]

        with self.assertRaises(ADNException) as cm:
            esMutante(adn)

        the_exception = cm.exception
        self.assertEqual(str(the_exception), "Secuencia de dimensiones inválidas (esperaba 4 y la 1-ésima fila mide 5)")

if __name__ == '__main__':
    unittest.main()
