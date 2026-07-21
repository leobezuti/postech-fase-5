import os
import sys
import logging
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import upgrade
from sqlalchemy.exc import IntegrityError

from extensions import db, migrate
import models  # noqa: F401

print("deployv2")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)


def build_database_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    else:
        log.critical("Erro: defina DATABASE_URL.")
        sys.exit(1)

app.config["SQLALCHEMY_DATABASE_URI"] = build_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)


def run_migrations():
    with app.app_context():
        upgrade()
        log.info("Migrations aplicadas com sucesso.")


try:
    run_migrations()
    log.info("Conexão com PostgreSQL (ngo-service) inicializada.")
except Exception as e:
    log.critical(f"Erro ao conectar ou migrar o banco: {e}")
    sys.exit(1)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ngo-service"})


@app.route("/ngos", methods=["POST"])
def create_ngo():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "cause", "city")):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    ngo = models.Ngo(
        name=data["name"],
        email=data["email"],
        cause=data["cause"],
        city=data["city"],
    )

    try:
        db.session.add(ngo)
        db.session.commit()
        return jsonify(ngo.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "E-mail já cadastrado"}), 409
    except Exception as e:
        db.session.rollback()
        log.error(f"Erro ao criar ONG: {e}")
        return jsonify({"error": "Erro interno"}), 500


@app.route("/ngos", methods=["GET"])
def get_ngos():
    try:
        ngos = models.Ngo.query.order_by(models.Ngo.id.desc()).all()
        return jsonify([ngo.to_dict() for ngo in ngos]), 200
    except Exception as e:
        log.error(f"Erro ao buscar ONGs: {e}")
        return jsonify({"error": "Erro interno"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    app.run(host="0.0.0.0", port=port)
