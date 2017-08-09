#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from adn_mutante import esMutante, ADNException
from adn_db import ADNDb

import boto3
import json

class TestADNDb(unittest.TestCase):
    ADNDb = None
    adn1 = ["atgcga", "cagtgc", "ttattt", "agacgg", "gcgtca", "tcactg"]
    hash_adn1 = 274368094279 #364697752066052461306429170069426344459438571043L 
    adn2 = ["atgcga", "cagtgc", "ttatgt", "agaagg", "ccccta", "tcactg"]

    def setUp(self):
        # Esto crea todas las tablas
        self.ADNDb = ADNDb("http://localhost:8080")

    def tearDown(self):
        # No debería acceder estos campos directamente, pero para limpiar en el test
        # me permito la imprudencia
        self.ADNDb.tabla_adn.delete()
        self.ADNDb.tabla_stat.delete()
    
    def test_empiezoDeCero(self):
        stat_inicial = self.ADNDb.get_stat()
        self.assertIsNone(stat_inicial)
        self.assertFalse(self.ADNDb.existe_adn(self.adn1))
        self.assertFalse(self.ADNDb.existe_adn(self.adn2))

    def test_adnHash(self):
        self.assertEqual(self.ADNDb.adn_hash(self.adn1), self.hash_adn1)

    def test_agregoAdn1(self):
        self.ADNDb.guardar_test(self.adn1, False)

        self.assertTrue(self.ADNDb.existe_adn(self.adn1))
        
        stat = self.ADNDb.get_stat()
        self.assertEqual(stat['count_mutant_dna'], 0)
        self.assertEqual(stat['count_human_dna'], 1)
        self.assertEqual(stat['ratio'], 0)

        test_en_db = self.ADNDb.get_test(self.adn1)
        self.assertEqual(test_en_db['adn_hash'], self.hash_adn1)
        self.assertEqual(test_en_db['adn_json'], json.dumps(self.adn1))
        self.assertFalse(test_en_db['esMutante'])

    def test_agregoAdn1y2(self):
        self.ADNDb.guardar_test(self.adn1, False)
        self.ADNDb.guardar_test(self.adn2, True)

        self.assertTrue(self.ADNDb.existe_adn(self.adn1))
        self.assertTrue(self.ADNDb.existe_adn(self.adn2))
        
        stat = self.ADNDb.get_stat()
        self.assertEqual(stat['count_mutant_dna'], 1)
        self.assertEqual(stat['count_human_dna'], 2)
        self.assertEqual(stat['ratio'], 0.5)

        test_en_db = self.ADNDb.get_test(self.adn2)
        self.assertEqual(test_en_db['adn_json'], json.dumps(self.adn2))
        self.assertTrue(test_en_db['esMutante'])

