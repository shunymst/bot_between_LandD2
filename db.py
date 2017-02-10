#!/usr/bin/env python
# coding=utf-8
import boto3
from boto3.dynamodb.conditions import Key, Attr


# precondition
# pip install awscli==1.11.46
# aws configure
# AWS Access Key ID [None]: AKIXXXXXXXXXXXXXXXXX
# AWS Secret Access Key [None]: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Default region name [None]: XXXXXX
# Default output format [None]: json
# pip install boto3==1.4.4

dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('LINE_USERS')
table = dynamodb.Table('FriendsV2')


response = table.get_item(Key={"MID":"U69b93081ef731fdaf077813f65296ebc"})# yamashita
print(response)
