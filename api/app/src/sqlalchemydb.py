import logging
from config import DATABASE_URL

from sqlalchemy import Table, MetaData, create_engine, exc, and_, or_, not_
from sqlalchemy import asc, desc, select, exists, func


logger = logging.getLogger()


class AlchemyDB:
    engine = None
    _table = dict()

    def __init__(self):
        self.conn = AlchemyDB.get_connection()

    def __del__(self):
        self.conn.close()

    @staticmethod
    def init():
        try:
            AlchemyDB.engine = create_engine(DATABASE_URL,
                                             paramstyle='format', pool_recycle=3600, )

            meta = MetaData()

            AlchemyDB._table["Campaign"] = Table('Campaign', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["CampaignSegmentMap"] = Table('CampaignSegmentMap', meta, autoload=True,
                                                           autoload_with=AlchemyDB.engine)
            AlchemyDB._table["CampaignSummary"] = Table('CampaignSummary', meta, autoload=True,
                                                        autoload_with=AlchemyDB.engine)
            AlchemyDB._table["Category"] = Table('Category', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["ContactSegmentMap"] = Table('ContactSegmentMap', meta, autoload=True,
                                                          autoload_with=AlchemyDB.engine)
            AlchemyDB._table["LinkTrack"] = Table('LinkTrack', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["MailTrack"] = Table('MailTrack', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["SampleCampaignSummary"] = Table('SampleCampaignSummary', meta, autoload=True,
                                                              autoload_with=AlchemyDB.engine)
            AlchemyDB._table["Segment"] = Table('Segment', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["Template"] = Table('Template', meta, autoload=True, autoload_with=AlchemyDB.engine)
            AlchemyDB._table["TestParameters"] = Table('TestParameters', meta, autoload=True,
                                                       autoload_with=AlchemyDB.engine)
            AlchemyDB._table["Variant"] = Table('Variant', meta, autoload=True, autoload_with=AlchemyDB.engine)
            meta.create_all(AlchemyDB.engine)
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
        except Exception as err:
            logger.error(err, exc_info=True)

    @staticmethod
    def get_connection():
        return AlchemyDB.engine.connect()

    @staticmethod
    def get_raw_connection():
        return AlchemyDB.engine.raw_connection()

    @staticmethod
    def get_table(name):
        return AlchemyDB._table[name]

    def begin(self):
        self.trans = self.conn.begin()

    def commit(self):
        self.trans.commit()

    def rollback(self):
        self.trans.rollback()

    @staticmethod
    def args_to_where(table, args):
        clause = []
        for k, v in args.items():
            if isinstance(v, (list, tuple)):
                clause.append(table.c[k].in_(v))
            elif isinstance(v, dict):
                if v['op'] == 'gte':
                    clause.append(table.c[k] >= v['value'])
                elif v['op'] == 'lte':
                    clause.append(table.c[k] <= v['value'])
            else:
                clause.append(table.c[k] == v)
        return and_(*clause)

    @staticmethod
    def args_to_where_or(table, args):
        clause = []
        for k, v in args.items():
            if isinstance(v, (list, tuple)):
                clause.append(table.c[k].in_(v))
            else:
                clause.append(table.c[k] == v)
        return or_(*clause)

    @staticmethod
    def args_to_like(table, args):
        clause = []
        for k in args:
            if isinstance(k, (list, tuple)):
                if k[0][0] == '!':
                    clause.append(not_(table.c[k[0][1:]].like(k[1])))
                else:
                    clause.append(table.c[k[0]].like(k[1]))
        return and_(*clause)

    @staticmethod
    def args_to_like_or(table, args):
        clause = []
        for k in args:
            if isinstance(k, (list, tuple)):
                if k[0][0] == '!':
                    clause.append(not_(table.c[k[0][1:]].like(k[1])))
                else:
                    clause.append(table.c[k[0]].like(k[1]))
        return or_(*clause)

    def insert_row(self, table_name, **values):
        table = AlchemyDB.get_table(table_name)
        insert = table.insert().values(values)
        logger.debug(insert)
        row_proxy = self.conn.execute(insert)
        logger.debug(row_proxy.inserted_primary_key)
        if row_proxy.inserted_primary_key:
            return row_proxy.inserted_primary_key[0]

    def insert_row_batch(self, table_name, values):
        table = AlchemyDB.get_table(table_name)
        self.conn.execute(table.insert(), values)

    def update_row(self, table_name, *keys, **row):
        table = AlchemyDB.get_table(table_name)
        try:
            if not isinstance(keys, (list, tuple)):
                keys = [keys]
            if not keys or len(keys) == len(row):
                return False
            clause = dict()
            for k in keys:
                clause[k] = row[k]
            clean_row = row.copy()
            for key in keys:
                if key in clean_row.keys():
                    del clean_row[key]
            clauses = AlchemyDB.args_to_where(table, clause)
            update = table.update(clauses, clean_row)
            self.conn.execute(update)
            return True
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def update_row_new(self, table_name, where=None, val=None):
        if not where:
            where = {}
        if not val:
            val = {}
        try:
            table = AlchemyDB.get_table(table_name)
            clauses = AlchemyDB.args_to_where(table, where)
            update = table.update(clauses, val)
            self.conn.execute(update)
            return True
        except Exception as err:
            logger.error(err, exc_info=True)
            return False

    def delete_row(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            delete = table.delete().where(AlchemyDB.args_to_where(table, where))
            self.conn.execute(delete)
            return True
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def find_one(self, table_name, **where):
        logger.debug("Conditions: " + str(where))
        table = AlchemyDB.get_table(table_name)
        sel = select([table]).where(AlchemyDB.args_to_where(table, where))
        logger.debug(sel)
        row = self.conn.execute(sel)
        tup = row.fetchone()
        if tup:
            return dict(tup)
        return False

    def exists_row(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            sel = select([table]).where(AlchemyDB.args_to_where(table, where))
            sel = select([exists(sel)])
            row = self.conn.execute(sel).scalar()
            if row:
                return True
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
        return False

    def count_rows(self, table_name, like=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            if like and type(like) == list:
                sel = select([func.count()]).select_from(table).where(
                    and_(AlchemyDB.args_to_where(table, where), AlchemyDB.args_to_like(table, like)))
            else:
                sel = select([func.count()]).select_from(table).where(AlchemyDB.args_to_where(table, where))
            logger.debug(sel)
            row = self.conn.execute(sel)
            tup = row.fetchall()
            logger.debug(tup)
            return tup[0][0]
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def count_rows_or(self, table_name, like=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            if like and type(like) == list:
                sel = select([func.count()]).select_from(table).where(
                    or_(AlchemyDB.args_to_where(table, where), AlchemyDB.args_to_like_or(table, like)))
            else:
                sel = select([func.count()]).select_from(table).where(AlchemyDB.args_to_where(table, where))
            logger.debug(sel)
            row = self.conn.execute(sel)
            tup = row.fetchall()
            logger.debug(tup)
            return tup[0][0]
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def count_rows_join(self, table_names, foreign_key, where, like=None, joinflag='inner'):
        logger.debug(table_names)
        logger.debug(foreign_key)
        logger.debug(where)
        table = [AlchemyDB.get_table(t) for t in table_names]
        try:
            fclause = AlchemyDB.args_to_join(table[0], table[1], foreign_key[0])
            logger.debug(fclause)
            clause = AlchemyDB.args_to_where_join(where)
            logger.debug(clause)
            # clause = and_(fclause,clause)
            logger.debug(clause)
            if joinflag == 'outer':
                j = table[0].outerjoin(table[1], fclause)
            else:
                j = table[0].join(table[1], fclause)
            for i in range(1, len(foreign_key)):
                fclause = AlchemyDB.args_to_join(table[i], table[i + 1], foreign_key[i])
                j = j.join(table[i + 1], fclause)

            if like and type(like) == list and len(like) == 2:
                sel = select([func.count()]).select_from(j).where(
                    and_(clause, AlchemyDB.get_table(like[0].split('.')[0]).c[like[0].split('.')[1]].like(like[1])))
            else:
                sel = select([func.count()]).select_from(j).where(clause)

            logger.debug(sel)
            row = self.conn.execute(sel)
            tup = row.fetchall()
            logger.debug(tup)
            return tup[0][0]
        except Exception as e:
            logger.exception(e)
            return False

    def max(self, table_name, column_name, like=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            if like and type(like) == list:
                sel = select([func.max(table.c[column_name])]).select_from(table).where(
                    and_(AlchemyDB.args_to_where(table, where), AlchemyDB.args_to_like(table, like)))
            else:
                sel = select([func.max(table.c[column_name])]).select_from(table).where(
                    AlchemyDB.args_to_where(table, where))
            logger.debug(sel)
            row = self.conn.execute(sel)
            tup = row.fetchall()
            logger.debug(tup)
            return tup[0][0]
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def find(self, table_name, order_by=None, _limit=None, _offset=None, like=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            func = asc
            if order_by and order_by.startswith('_'):
                order_by = order_by[1:]
                func = desc
            if like and type(like) == list:
                sel = select([table]).where(
                    and_(AlchemyDB.args_to_where(table, where), AlchemyDB.args_to_like(table, like))).order_by(
                    func(order_by))
            else:
                sel = select([table]).where(AlchemyDB.args_to_where(table, where)).order_by(func(order_by))

            if _limit:
                sel = sel.limit(_limit)

            if _offset:
                sel = sel.offset(_offset)
            logger.debug(sel)

            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def find_or(self, table_name, order_by, _limit=None, _offset=None, like=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            func = asc
            if order_by and order_by.startswith('_'):
                order_by = order_by[1:]
                func = desc
            if like and type(like) == list:
                sel = select([table]).where(
                    or_(AlchemyDB.args_to_where_or(table, where), AlchemyDB.args_to_like_or(table, like))).order_by(
                    func(order_by))
            else:
                sel = select([table]).where(AlchemyDB.args_to_where_or(table, where)).order_by(func(order_by))

            if _limit:
                sel = sel.limit(_limit)

            if _offset:
                sel = sel.offset(_offset)
            logger.debug(sel)

            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    @staticmethod
    def args_to_join(table1, table2, args):
        logger.debug(type(table1))
        logger.debug(type(table2))
        logger.debug(args)
        clause = []
        for k, v in args.items():
            clause.append(table1.c[k] == table2.c[v])
        return and_(*clause)

    def select_join(self, table_names, foreign_key, where, order_by, _limit=None, _offset=None, like=None,
                    joinflag='inner'):
        logger.debug(table_names)
        logger.debug(foreign_key)
        logger.debug(where)
        table = [AlchemyDB.get_table(t) for t in table_names]
        try:
            func = asc
            if order_by and order_by.startswith('_'):
                order_by = order_by[1:]
                func = desc
            fclause = AlchemyDB.args_to_join(table[0], table[1], foreign_key[0])
            logger.debug(fclause)
            clause = AlchemyDB.args_to_where_join(where)
            logger.debug(clause)
            # clause = and_(fclause,clause)
            logger.debug(clause)
            if joinflag == 'outer':
                j = table[0].outerjoin(table[1], fclause)
            else:
                j = table[0].join(table[1], fclause)
            for i in range(1, len(foreign_key)):
                fclause = AlchemyDB.args_to_join(table[i], table[i + 1], foreign_key[i])
                j = j.join(table[i + 1], fclause)

            if like and type(like) == list and len(like) == 2:
                sel = select(table, use_labels=True).select_from(j).where(and_(clause, AlchemyDB.get_table(
                    like[0].split('.')[0]).c[like[0].split('.')[1]].like(like[1]))).order_by(func(order_by))
            else:
                sel = select(table, use_labels=True).select_from(j).where(clause).order_by(func(order_by))

            if _limit:
                sel = sel.limit(_limit)

            logger.debug(sel)

            if _offset:
                sel = sel.offset(_offset)

            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except Exception as e:
            logger.exception(e)
            return False

    @staticmethod
    def args_to_where_join(where):
        # where = [({"SocialContact.Email": email}), ({"AppUserId": appid})]
        logger.debug(where)
        or_list = []
        for tup in where:
            and_list = []
            for r in tup:
                if r:
                    logger.debug(r)
                    tab, col = r.keys()[0].split('.')
                    table = AlchemyDB.get_table(tab)
                    v = r.values()[0]
                    if isinstance(v, (list, tuple)):
                        and_list.append(table.c[col].in_(v))
                    else:
                        and_list.append(table.c[col] == v)
            or_list.append(and_(*and_list))
        logger.debug('AND List: ' + str(and_(*and_list)))
        logger.debug('OR List: ' + str(or_(*or_list)))
        return or_(*or_list)

