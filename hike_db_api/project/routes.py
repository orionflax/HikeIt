from flask import Blueprint, jsonify, request,make_response
from project.models import Routes
from project.util import *
from flask import jsonify

bp = Blueprint('routes', __name__)

@bp.route('/home', methods=['GET'])
def send_csrf_token():
    return (jsonify(success=True))