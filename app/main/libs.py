# encoding: utf-8
from flask import abort
from flask.ext.sqlalchemy import Pagination


def do_paginate(query, page=1, per_page=20, error_out=True):
    if error_out and page < 1:
        abort(404)
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        abort(404)
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()
    return Pagination(query=None, page=page, per_page=per_page, total=total, items=items)
