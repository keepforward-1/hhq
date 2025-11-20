"""
数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

from models.user import User
from models.galaxy_classification import GalaxyClassification
from models.constellation_recognition import ConstellationRecognition
from models.celestial_positioning import CelestialPositioning
from models.space_engine_data import SpaceEngineData
from models.tianxun_ai_chat import TianxunAIChat
from models.homepage_content import HomepageContent

__all__ = ['db', 'User', 'GalaxyClassification', 'ConstellationRecognition', 
           'CelestialPositioning', 'SpaceEngineData', 'TianxunAIChat', 'HomepageContent']

