from flask import Blueprint, request, jsonify  # <-- THIS FIXES THE LINTER
from service.models import Account             # <-- THIS IS PART 1 OF THE CIRCULAR FIX
from . import db                               # <-- THIS IS PART 2 OF THE CIRCULAR FIX
# (add any other imports your file needs below this)

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('', methods=['POST'])
def create_account():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    account = Account(name=data['name'], balance=data.get('balance', 0.0))
    db.session.add(account)
    db.session.commit()
    return jsonify(account.serialize()), 201

@bp.route('', methods=['GET'])
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
    if 'name' in data:
        account.name = data['name']
    if 'balance' in data:
        account.balance = data['balance']
    db.session.commit()
    return jsonify(account.serialize())

@bp.route('/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return '', 204