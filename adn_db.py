#!/usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import sha1
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class ADNDb:
    db = None
    db_endpoint_url = "http://localhost:8080"
    nombre_tabla_adn = "ADN"
    nombre_tabla_stat = "stat"
    tabla_adn = None
    tabla_stat = None
    stat_id = 42
    stat_actual = None 

    def __init__(self, endpoint_url = None):
        self.db = boto3.resource('dynamodb', region_name='us-east-1')

        #Si las tablas no existen, las creo
        tabla_names = boto3.client('dynamodb', region_name='us-east-1').list_tables()['TableNames']

        #self.db = boto3.resource('dynamodb', endpoint_url= self.db_endpoint_url if endpoint_url == None else endpoint_url)

        ##Si las tablas no existen, las creo
        #tabla_names = boto3.client('dynamodb', endpoint_url="http://localhost:8080").list_tables()['TableNames']

        if self.nombre_tabla_adn in tabla_names:
            self.tabla_adn = self.db.Table(self.nombre_tabla_adn)
        else:
            self.tabla_adn = self.db.create_table(
                    TableName = self.nombre_tabla_adn,
                    AttributeDefinitions = [
                        {
                            'AttributeName': 'adn_hash',
                            'AttributeType': 'N'
                        },
                        #{
                        #    'AttributeName': 'adn_json',
                        #    'AttributeType': 'S'
                        #},
                        #{
                        #    'AttributeName': 'esMutante',
                        #    'AttributeType': 'N'
                        #},
                    ],
                    KeySchema = [
                        {
                            'AttributeName': 'adn_hash',
                            'KeyType': 'HASH'
                        },
                    ],
                    ProvisionedThroughput = {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                )

        if self.nombre_tabla_stat in tabla_names:
            self.tabla_stat = self.db.Table(self.nombre_tabla_stat)
        else:
            self.tabla_stat = self.db.create_table(
                    TableName = self.nombre_tabla_stat,
                    AttributeDefinitions = [
                        {
                            'AttributeName': 'id',
                            'AttributeType': 'N'
                        },
                        #{
                        #    'AttributeName': 'stat_json',
                        #    'AttributeType': 'S'
                        #},
                    ],
                    KeySchema = [
                        {
                            'AttributeName': 'id',
                            'KeyType': 'HASH'
                        },
                    ],
                    ProvisionedThroughput = {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }

                )

        #Inicializo las estadísticas
        stat_en_db = self.get_stat_en_db()

        if stat_en_db == None:
            self.stat_actual = {
                'count_mutant_dna': 0,
                'count_human_dna': 0,
                'ratio': 0,
            }
        else:
            self.stat_actual = stat_en_db


    def get_stat_en_db(self):
        try:
            response = self.tabla_stat.get_item(Key={'id':self.stat_id})
            if response.has_key('Item'):
                return json.loads(response['Item']['stat_json'])
            else:
                return None

        except ClientError as e:
            print(e.response['Error']['Message'])
            raise

    def get_stat(self):
        return self.stat_actual

    def actualizar_stat(self, esMutante):
        if self.stat_actual == None:
            self.stat_actual = {
                'count_mutant_dna': 1 if esMutante else 0,
                'count_human_dna': 1,
                'ratio': 1 if esMutante else 0,
            }
        else:
            self.stat_actual['count_mutant_dna'] += (1 if esMutante else 0)
            self.stat_actual['count_human_dna'] += 1
            self.stat_actual['ratio'] = float(self.stat_actual['count_mutant_dna']) / self.stat_actual['count_human_dna']

    def adn_hash(self, adn):
        return int(sha1("".join(adn)).hexdigest()[:10], 16)

    def guardar_test(self, adn, esMutante):
        adn_hash = self.adn_hash(adn)

        self.actualizar_stat(esMutante)

        item_adn = {
            'adn_hash': adn_hash,
            'adn_json': json.dumps(adn),
            # No se si se convierte automáticamente de bool a int
            'esMutante': 1 if esMutante else 0
        }

        response = self.tabla_adn.put_item(Item = item_adn)

        response = self.tabla_stat.put_item(
                Item = {
                        'id': self.stat_id,
                        'stat_json': json.dumps(self.stat_actual)
                    }
                )

    def get_test(self, adn):
        try:
            item = self.tabla_adn.get_item(
                    Key={
                        'adn_hash': self.adn_hash(adn)
                        }
                    )['Item']

            return item
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise

    def existe_adn(self, adn):
        try:
            adn_hash = self.adn_hash(adn)
            items = self.tabla_adn.query(KeyConditionExpression = Key('adn_hash').eq(adn_hash))
            return items['Count'] > 0
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise

