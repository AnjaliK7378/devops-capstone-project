"""
Account Routes
"""
from flask import Blueprint, request, jsonify  # <-- FIXES LINTER
from .models import Account                   # <-- FIXES CIRCULAR IMPORT
from . import db                             # <-- FIXES CIRCULAR IMPORT

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/', methods=['POST'])
def create_account():
    data = request.get_json()
    if 'name' not in data:  # Assuming you have a 'name' field
        return jsonify({'error': 'Name is required'}), 400
    
    account = Account()
    account.deserialize(data)
    db.session.add(account)
    db.session.commit()
    
    return jsonify(account.serialize()), 201

@bp.route('/', methods=['GET'])
def list_accounts():
    accounts = Account.query.all()
    return jsonify([a.serialize() for a in accounts])

@bp.route('/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get_or_404(account_id)
    return jsonify(account.serialize())

@bp.route('/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    account = Account.query.get_or_404(account_id)
    data = request.get_json()
    account.deserialize(data)
    db.session.commit()
    return jsonify(account.serialize())