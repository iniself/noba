#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/3/19  
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function, unicode_literals)
from noba.Core import core
from noba.dber import DAL, Table, Field, Set, Expression, Rows, Row
from functools import reduce
from noba.snippet import is_str, is_list, is_number
from .abs import DBManagerAbs

config = core.make('config')
migrate_folder = core.make('project.migrate.absolute.path')

class Operator(object):
    def set_operators(self):
        self.logical_operators = ['==', '!=', '<', '>', '<=', '>=', 'like', 'ilike', 'regexp', 'startswith', 'endswith', 'contains', 'belongs']
        self.time_operators = ['.year', '.month', '.day', '.hour', '.minutes', '.seconds']

    def has_op(self, op):
        return op in self.logical_operators

    def _trans_query_str(self, query_str):
        first, operator, second = self._spit_to_key_op_value(query_str)
        if not operator:
            return first

        if operator == '==':
            query = first == second
        elif operator == '!=':
            query = first != second
        elif operator == '<':
            query = first < second
        elif operator == '>':
            query = first > second
        elif operator == '<=':
            query = first <= second
        elif operator == '>=':
            query = first >= second
        elif operator == 'like':
            query = first.like(second)
        elif operator == 'ilike':
            query = first.ilike(second)
        elif operator == 'regexp':
            query = first.regexp(second)
        elif operator == 'startswith':
            query = first.startswith(second)
        elif operator == 'endswith':
            query = first.endswith(second)
        elif operator == 'contains':
            query = first.contains(second)
        elif operator == 'belongs':
            query = first.belongs(eval(second))
        else:
            query = first

        return query

    def _spit_to_key_op_value(self, query_string):
        if isinstance(self, DberTable):
            table = self
        elif isinstance(self, Collections):
            table = self.table
        else:
            raise SyntaxError

        logical_operator = [item for item in self.logical_operators if item in query_string]

        if len(logical_operator) > 1:
            if '<=' in logical_operator:
                logical_operator = ['<=']
            elif '>=' in logical_operator:
                logical_operator = ['>=']
            else:
                raise SyntaxError("Incorrect time operation")
        elif len(logical_operator) == 0:
            # none operator
            return self._split_time_operators(query_string, table), None, None

        tmp = [self._split_time_operators(one.strip(), table) for one in query_string.split(*logical_operator)]
        if not isinstance(tmp[0], Field) and  not isinstance(tmp[0], Expression) and not isinstance(tmp[1], Field):
            raise SyntaxError("Incorrect operation")
        return tmp[0], logical_operator[0], tmp[1]

    def _split_time_operators(self, query_string, table):
        filed, time_op = query_string, None

        found_items = [item for item in self.time_operators if item in filed]
        if len(found_items) > 1:
            raise SyntaxError("Incorrect time operation")
        elif len(found_items) == 1:
            filed = filed.replace(found_items[0], "").strip()
            time_op = found_items[0][1:].strip()

        if filed in table.fields:
            filed = getattr(table, filed)

        try:
            if time_op:
                filed = getattr(filed, time_op)()
            return filed
        except:
            raise SyntaxError("only date and datetime fields can use year|month|day operation, and only datetime time can use hour|minutes|seconds operation")

    def _trans_join_query_str(self, query_str):
        first_table, first_field, operator, second_table, second_field = self._spit_join_to_key_op_value(query_str)
        if not operator:
            return first_field

        if operator == '==':
            query = first_field == second_field
        elif operator == '!=':
            query = first_field != second_field
        elif operator == '<':
            query = first_field < second_field
        elif operator == '>':
            query = first_field > second_field
        elif operator == '<=':
            query = first_field <= second_field
        elif operator == '>=':
            query = first_field >= second_field
        elif operator == 'like':
            query = first_field.like(second_field)
        elif operator == 'ilike':
            query = first_field.ilike(second_field)
        elif operator == 'regexp':
            query = first_field.regexp(second_field)
        elif operator == 'startswith':
            query = first_field.startswith(second_field)
        elif operator == 'endswith':
            query = first_field.endswith(second_field)
        elif operator == 'contains':
            query = first_field.contains(second_field)
        elif operator == 'belongs':
            query = first_field.belongs(eval(second_field))
        else:
            query = first_field
        return first_table, second_table, query

    def _spit_join_to_key_op_value(self, query_string):
        if isinstance(self, DberTable):
            table = self
        elif isinstance(self, Collections):
            table = self.table
        else:
            raise SyntaxError

        logical_operator = [item for item in self.logical_operators if item in query_string]

        if len(logical_operator) > 1:
            if '<=' in logical_operator:
                logical_operator = ['<=']
            elif '>=' in logical_operator:
                logical_operator = ['>=']
            else:
                raise SyntaxError("Incorrect time operation")
        elif len(logical_operator) == 0:
            raise SyntaxError("Incorrect operation")

        first_list = query_string.split(*logical_operator)[0].split('.')
        second_list = query_string.split(*logical_operator)[1].split('.')

        if len(first_list) > 1:
            first_table = self._db.table(first_list[0].strip())
            first_field = first_table._get_field(first_list[1].strip())
        else:
            first_table = table
            first_field = first_table._get_field(first_list[0].strip())

        if len(second_list) > 1:
            second_table = self._db.table(second_list[0].strip())
            second_field = second_table._get_field(second_list[1].strip())
        else:
            second_table = table
            second_field = second_table._get_field(second_list[0].strip())
        return first_table, first_field, logical_operator[0], second_table, second_field



def sumbit_change(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        if isinstance(args[0], DberTable) or isinstance(args[0], Collections):
            db = args[0]._db
        elif isinstance(args[0], DBManager):
            db = args[0]
        else:
            raise SyntaxError

        db.commit()
        return  ret
    return wrapper

def connect_close(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        if isinstance(args[0], DberTable) or isinstance(args[0], Collections):
            db = args[0]._db
        elif isinstance(args[0], DBManager):
            db = args[0]
        else:
            raise SyntaxError

        db.close()
        return  ret
    return wrapper

def format_result(func):
    def wrapper(*args, **kwargs):
        format = kwargs.get('format', True)
        if not format:
            del kwargs['format']

        ret = func(*args, **kwargs)
        _format = config.get('db.format', None)
        if not _format:
            return ret

        if format:
            if _format == 'list':
                if isinstance(ret, Rows):
                    return ret.as_list()
                elif isinstance(ret, Row):
                    # return ret.as_dict()
                    return ret.as_ordered_dict()
                else:
                    raise SyntaxError
            elif _format == 'dataframe':
                import pandas as pd
                if isinstance(ret, Rows):
                    pd_data = ret.as_list()
                elif isinstance(ret, Row):
                    pd_data = [ret.as_ordered_dict()]
                else:
                    raise SyntaxError
                try:
                    return pd.DataFrame(pd_data).set_index('id')
                except KeyError:
                    return pd.DataFrame(pd_data)
        else:
            return ret
    return wrapper

class ABMeta(type(DAL), type(DBManagerAbs)):
    pass


class DBManager(DAL, DBManagerAbs, metaclass=ABMeta):
    def __init__(self, args={}):
        args['folder'] = migrate_folder
        _connector = config.get('db.connector', None)
        super(DBManager, self).__init__(self._connect_str_factory(connector=_connector), **args)

    def _connect_str_factory(self, connector):
        host = config.get('db.host')
        port = config.get('db.port')
        database = config.get('db.database')
        username = config.get('db.username')
        password = config.get('db.password')
        # dsn = config.get('db.dsn')
        host = f'{host}:{port}' if port.strip() else f'{host}'
        return {
            "sqlite": f"sqlite://{migrate_folder.joinpath(database)}",
            "mysql": f"mysql://{username}:{password}@{host}/{database}?set_encoding=utf8mb4",
            "postgresql": f"postgres://{username}:{password}@{host}/{database}",
            "mssql": f"mssql://{username}:{password}@{host}/{database}",
            "mssql3": f"mssql3://{username}:{password}@{host}/{database}",
            "mssql4": f"mssql4://{username}:{password}@{host}/{database}",
            "firebird": f"firebird://{username}:{password}@{host}/{database}",
            "oracle": f"oracle://{username}:{password}@{host}/{database}",
            "db2": f"db2://{username}:{password}@{host}/{database}",
            "ingres": f"ingres://{username}:{password}@{host}/{database}",
            "sybase": f"sybase://{username}:{password}@{host}/{database}",
            "informix": f"informix://{username}:{password}@{database}",
            "teradata": f"teradata://DSN={host};UID={username};PWD={password};DATABASE={database}",
            "cubrid": f"cubrid://{username}:{password}@{host}/{database}",
            "sapdb": f"sapdb://{username}:{password}@{host}/{database}",
            "imap": f"imap://{username}:{password}@{host}",
            "mongodb": f"mongodb://{username}:{password}@{host}/{database}",
            "google:sql": f"",
            "google:datastore": f"",
            "google:datastore+ndb": f"",
        }.get(connector.lower(), None)


    @property
    def db(self):
        return self

    @connect_close
    @sumbit_change
    def add_table(self, tabel_name, fields=[]):
        self.define_table(tabel_name, *(self.__generate_dber_field(fields)), migrate=True, redefine=True, table_class=DberTable)
        return getattr(self, tabel_name)

    def table(self, tabel_name):
        self.import_table_definition(self._adapter.folder, table=tabel_name, table_class=DberTable)
        table_obj = getattr(self, tabel_name, None)
        if not table_obj or (len(table_obj.fields) == 1 and 'id' in table_obj.fields):
            fields = self.__get_table_filed_name(tabel_name)
            self.define_table(tabel_name, *(self.__generate_dber_field(fields)), migrate=False, redefine=True, table_class=DberTable)
        return getattr(self, tabel_name)

    def get_table(self, table_name):
        return getattr(self, table_name)

    def __get_table_filed_name(self, tabel_name):
        try:
            # self.executesql(f"select {self._adapter.dialect.quote('*')} from {self._adapter.dialect.quote(tabel_name)} limit 0")
            self.executesql(f"select * from {self._adapter.dialect.quote(tabel_name)} limit 0")
        except Exception:
            self.executesql(f"select * from {tabel_name} limit 0")

        desc = self._adapter.cursor.description
        return [f[0] for f in desc]

    def __generate_dber_field(self, fields):
        return [Field(field) if is_str(field) else (Field(field[0], **field[1])) for field in fields]



class DberTable(Table, Operator):
    def __init__(self, dbManager, tabel_name, *fields, **args):
        super(DberTable, self).__init__(dbManager, tabel_name, *fields, **args)
        self.set_operators()

    def __getattr__(self, item):
        if item in ['like', 'ilike', 'regexp', 'startswith', 'endswith', 'contains', 'belongs']:
            return self.__magic_joker(item)
        super(DberTable, self).__getattr__(item)

    def __magic_joker(self, item):
        def one_func(field, value=()):
            query = getattr(getattr(self, field), item)(value)
            return Collections(self._db, self, query, ignore_common_filters=None)
        return one_func

    def _get_field(self,field=None, tabel=None):
        if not tabel:
            tabel = self

        if isinstance(field, Field):
            return field
        else:
            return getattr(tabel, field)

    def isnull(self, field, ignore_common_filters=None):
        query = getattr(self, field) == None
        return Collections(self._db, self, query, ignore_common_filters=ignore_common_filters)

    def where(self, query_string="", ignore_common_filters=None):
        query = self._trans_query_str(query_string)

        if not query or self._tablename == query:
            query = self
        if isinstance(query, Table):
            query = self.id != None
        elif isinstance(query, Field):
            query = query != None
        elif isinstance(query, dict):
            icf = query.get("ignore_common_filters")
            if icf:
                ignore_common_filters = icf
        return Collections(self._db, self, query, ignore_common_filters=ignore_common_filters)

    def get(self, *selects, **attributes):
        # get all rows from some field
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        return set.get(*selects, **attributes)

    def fetch(self, *selects, **attributes):
        # fetch all rows from some field
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        return set.fetch(*selects, **attributes)

    def get_except(self, *selects, **attributes):
        fields = [i for i in self.fields if i not in selects]
        return self.get(*fields, **attributes)

    def fetch_except(self, *selects, **attributes):
        fields = [i for i in self.fields if i not in selects]
        return self.fetch(*fields, **attributes)

    def order_by(self, orderby):
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        set.orderby = getattr(self, orderby)
        return set

    def group_by(self, groupby):
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        set.groupby = getattr(self, groupby)
        return set

    def limit(self, min, max):
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        set.limitby = (min, max)
        return set

    def inner_join(self, query_string=''):
        first_table, second_table, query = self._trans_join_query_str(query_string)
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        set.innerjoin.append({'first_table':first_table, 'second_table':second_table, 'query':query})
        return set

    def left_join(self, query_string=''):
        first_table, second_table, query = self._trans_join_query_str(query_string)
        set = Collections(self._db, self, self.id != None, ignore_common_filters=None)
        set.leftjoin.append({'first_table':first_table, 'second_table':second_table, 'query':query})
        return set

    @connect_close
    @format_result
    def get_by_id(self, id):
        return self[id]

    def where_id(self, id):
        return self.where(f'id=={id}')

    @connect_close
    def fetch_by_id(self, id):
        return self[id]

    @connect_close
    @sumbit_change
    def insert(self, **fields):
        return super().insert(**fields)

    @connect_close
    @sumbit_change
    def update_or_insert(self, _key=lambda: None, **values):
        if _key:
            query = self._trans_query_str(_key)
        return super().update_or_insert(query, **values)

    def validate_and_insert(self):
        pass

    def validate_and_update(self):
        pass


class Collections(Set, Operator):
    def __init__(self, dbManager, table, query, ignore_common_filters=None):
        self.orderby = None
        self.limitby = None
        self.groupby = None
        self.innerjoin = []
        self.leftjoin = []

        self.table = table
        super(Collections, self).__init__(dbManager, query, ignore_common_filters)
        self.set_operators()

    @connect_close
    @format_result
    def get(self, *selects, **attributes):
        # fetch data from database
        if self.orderby:
            attributes['orderby'] = self.orderby
        if self.limitby:
            attributes['limitby'] = self.limitby
        if self.groupby:
            attributes['groupby'] = self.groupby
        if self.innerjoin:
            if len(self.innerjoin) > 1:
                attributes['join'] = reduce(lambda first, second: (getattr(first['second_table'], 'on')(first['query'] & second['query'])), self.innerjoin)
            elif len(self.innerjoin) == 1:
                attributes['join'] = getattr(self.innerjoin[0]['second_table'], 'on')(self.innerjoin[0]['query'])
        if self.leftjoin:
            if len(self.leftjoin) > 1:
                attributes['left'] = reduce(lambda first, second: (getattr(first['second_table'], 'on')(first['query'] & second['query'])), self.leftjoin)
            elif len(self.leftjoin) == 1:
                attributes['left'] = getattr(self.leftjoin[0]['second_table'], 'on')(self.leftjoin[0]['query'])

        if any(self.innerjoin) or any(self.leftjoin):
            fields = list()
            if not all(['.' in select for select in selects]):
                raise SyntaxError
            for select in selects:
                if isinstance(select, Expression):
                    fields.append(select)
                else:
                    table, field = select.split('.')
                    fields.append(getattr(getattr(self._db, table, None), field))
        else:
            fields = [field if isinstance(field, Expression) else getattr(self.table, field) for field in selects]
        return self.select(*fields, **attributes)

    def fetch(self, *selects, **attributes):
        attributes['format'] = False
        return self.get(*selects, **attributes)

    def get_except(self, *selects, **attributes):
        fields = [i for i in self.table.fields if i not in selects]
        return self.get(*fields, **attributes)

    def fetch_except(self, *selects, **attributes):
        fields = [i for i in self.table.fields if i not in selects]
        return self.fetch(*fields, **attributes)

    def order_by(self, orderby):
        self.orderby = getattr(self.table, orderby)
        return self

    def group_by(self, groupby):
        self.groupby = getattr(self.table, groupby)
        return self

    def limit(self, min, max):
        self.limitby = (min, max)
        return self

    def inner_join(self, query_string=''):
        first_table, second_table, query = self._trans_join_query_str(query_string)
        self.innerjoin.append({'first_table':first_table, 'second_table':second_table, 'query':query})
        return self

    def left_join(self, query_string=''):
        first_table, second_table, query = self._trans_join_query_str(query_string)
        self.leftjoin.append({'first_table':first_table, 'second_table':second_table, 'query':query})
        return self

    def where(self, query_string, ignore_common_filters=False):
        query = self._trans_query_str(query_string)
        if query is None:
            return self
        elif isinstance(query, Table):
            query = self.db._adapter.id_query(query)
        elif isinstance(query, str):
            query = Expression(self.db, query)
        elif isinstance(query, Field):
            query = query != None
        if self.query:
            return Collections(
                self.db, self.table, self.query & query, ignore_common_filters=ignore_common_filters
            )
        else:
            return Collections(self.db, self.table, query, ignore_common_filters=ignore_common_filters)

    def or_where(self, query_string, ignore_common_filters=False):
        query = self._trans_query_str(query_string)
        if query is None:
            return self
        elif isinstance(query, Table):
            query = self.db._adapter.id_query(query)
        elif isinstance(query, str):
            query = Expression(self.db, query)
        elif isinstance(query, Field):
            query = query != None
        if self.query:
            return Collections(
                self.db, self.table, self.query | query, ignore_common_filters=ignore_common_filters
            )
        else:
            return Collections(self.db, self.table, query, ignore_common_filters=ignore_common_filters)

    @connect_close
    @sumbit_change
    def update(self, **update_fields):
        return super().update(**update_fields)



class FileManager(DBManagerAbs):
    def __init__(self):
        self.pd = core.make('pd')
        self._table = None
        self.operators = ['==', '!=', '<', '>', '<=', '>=']
        self.file_path = migrate_folder.joinpath(config.get('db.database') if not self._table else self._table)
        self._where = []
        self._index = None
        self._limit = ()

    def table(self, table_name=None):
        self._table =  table_name
        return self

    def where(self, query_string):
        field, operator, val = self._split_query(query_string)
        self._where.append({'field':field, 'operator':operator, 'where':'&', 'val':val})
        return self

    def or_where(self, query_string):
        field, operator, value = self._split_query(query_string)
        self._where.append({'field':field, 'operator':operator, 'where':'|', 'val':value})
        return self

    def limit(self, min, max=None):
        self._limit = {'min':min, 'max':max}
        return self

    def set_index(self, index):
        self._index = index
        return self

    def _split_query(self, query_string):
        operator = [item for item in self.operators if item in query_string]
        if len(operator) > 1:
            if '<=' in operator:
                operator = ['<=']
            elif '>=' in operator:
                operator = ['>=']
            else:
                raise SyntaxError("Incorrect time operation")
        elif len(operator) == 0:
            raise SyntaxError("Incorrect operation")

        field = query_string.split(*operator)[0].strip()
        val = query_string.split(*operator)[1].strip()
        return field, operator[0].strip(), val

    def get(self, *field, **kwargs):
        data = self._read_file_to_pd(*field, **kwargs)
        if any(self._where):
            if len(self._where) > 1:
                where_express = reduce(self._generate_where_express(data), self._where)
            else:
                where_express = self._generate_op_express(self._where[0], data)
            data = data[where_express]
        if self._limit:
            if not self._limit['max']:
                data = data[self._limit['min']:]
            else:
                data = data[self._limit['min']:self._limit['max']]

        return data

    def _read_file_to_pd(self, *field, **kwargs):
        pass

    def _generate_where_express(self, data):
        def some_fun(first, second):
            first_where = self._generate_op_express(first, data)
            second_where = self._generate_op_express(second, data)
            if second['where'] == '&':
                return first_where & second_where
            if second['where'] == '|':
                return first_where | second_where
        return some_fun

    def _generate_op_express(self, where, data):
        field = getattr(data, where['field'])
        operator = where['operator']
        # val = float(where['val']) if is_number(where['val']) else where['val']
        try:
            val = eval(where['val'])
        except SyntaxError:
            val = where['val']

        if operator == '==':
            where = field == val
        elif operator == '!=':
            where = field != val
        elif operator == '<':
            where = field < val
        elif operator == '>':
            where = field > val
        elif operator == '<=':
            where = field <= val
        elif operator == '>=':
            where = field >= val
        return where

    def get_except(self, *field, **kwargs):
        res = self.get(**kwargs)
        return res.drop(list(field), axis=1)


class CSV(FileManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_file_to_pd(self, *field, **kwargs):
        kwargs['encoding'] = "utf-8"
        data = self.pd.read_csv(self._table or self.file_path, index_col=self._index, usecols=field if field else None, **kwargs)
        return data

class XLS(FileManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_file_to_pd(self, *field, **kwargs):
        sheet_name = kwargs.get('sheet_name', 0)
        data = self.pd.read_excel(self.file_path, sheet_name=sheet_name, index_col=self._index, usecols=field if field else None, **kwargs)
        return data

