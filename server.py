from __future__ import annotations
from hashlib import md5
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Adv
from schema import PatchAdver, VALIDATION_CLASS, CreateAdver
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def get_adv(session: Session, adv_id: int):
    user = session.get(Adv, adv_id)
    if user is None:
        raise HttpError(404, message="user doesn't exist")
    return user


def hash_password(password: str):
    password = password.encode()
    password_hash = md5(password)
    password_hash_str = password_hash.hexdigest()
    return password_hash_str


class AdvView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = get_adv(session, adv_id)
            return jsonify(
                {
                    "id": adv.id,
                    "user": adv.user,
                    "title": adv.title,
                    "description": adv.description,
                    "creation_time": adv.creation_time.isoformat(),
                }
            )

    def post(self):
        json_data = validate_json(request.json, CreateAdver)
        # json_data["password"] = hash_password(json_data["password"])
        with Session() as session:
            user = Adv(**json_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["title"]} уже существует')
            return jsonify({"id": user.id})

    def patch(self, user_id: int):
        json_data = validate_json(request.json, PatchAdver)
        # if "password" in json_data:
        #     json_data["password"] = hash_password(json_data["password"])
        with Session() as session:
            user = get_adv(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["user"]} уже существует')
            return jsonify(
                {
                    "id": user.id,
                    "user": user.user,
                    "title": user.title,
                    "description": user.description,
                    "creation_time": user.creation_time.isoformat(),
                }
            )

    def delete(self, adv_id: int):
        with Session() as session:
            user = get_adv(session, adv_id)
            session.delete(user)
            session.commit()
            return jsonify({"status": "success"})


app.add_url_rule(
    "/ad/<int:ad_id>",
    view_func=AdvView.as_view("with_user_id"),
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule("/ad/",
                 view_func=AdvView.as_view("create_user"),
                 methods=["POST"])
if __name__ == "__main__":
    app.run()
