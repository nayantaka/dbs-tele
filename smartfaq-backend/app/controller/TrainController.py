import sys
from app import app
from app import responses as res
from flask_jwt_extended import *
from app.service.Daemon.TrainModel import TrainModel

@jwt_required
def index():
    training = TrainModel()
    result = training.result

    return res.ok(result, 'success')
