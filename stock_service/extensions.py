# encoding: utf-8

from flask_marshmallow import Marshmallow
from marshmallow import pre_dump as pre_dump_
from datetime import datetime as datetime_

marsh = Marshmallow()
datetime = datetime_
pre_dump = pre_dump_
