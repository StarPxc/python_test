"""
 @Author 浦希成
 @Date 2018/8/29 8:29
 @Description 
 
"""
import pymysql

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '935377012'


"""
批量插入
"""
def insert_to_mysql(db_name, table_name, data_list):
    sql = 'insert into {table_name} ('.format(table_name=table_name)
    conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=db_name)
    cur = conn.cursor()
    for key in data_list[0].keys():
        sql += key + ','
    sql = sql[:-1] + ') values'
    for data in data_list:
        sql += '('
        for value in data.values():
            if isinstance(value, str) or value is None:
                sql += "'{}'".format(value) + ','
            else:
                sql += str(value) + ','
        sql = sql[:-1] + '),'
    sql = sql[:-1]
    print(sql)
    lines = cur.execute(sql)  # 返回受影响的行数
    print('成功插入{}条数据'.format(lines))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    data_list = [{'product_code': 'EB5720', 'bank_name': '中国光大银行',
                  'register_code': 'http://www.cebbank.com/site/gryw/yglc/lccpsj/yxl94/48910208/2018082815101228331.pdf',
                  'invest_code': '', 'product_name': '财富定向-6月', 'product_type': '', 'product_summary': '',
                  'product_profit_type': '预期年化收益率', 'product_profit': '4.9-4.9%', 'risk_level': '中风险',
                  'product_limit_time': '180天', 'start_time': '20170905', 'end_time': '20170911',
                  'start_amount': '100万', 'limit_amount': '',
                  'url': 'http://www.cebbank.com/site/gryw/yglc/lccpsj/yxl94/48910208/index.html', 'update_time': '',
                  'is_deleted': 0}
        , {'product_code': 'EB5717', 'bank_name': '中国光大银行',
           'register_code': 'http://www.cebbank.com/site/gryw/yglc/lccpsj/yxl94/48910196/2018082815082185432.pdf',
           'invest_code': '', 'product_name': '财富定向-3月', 'product_type': '', 'product_summary': '',
           'product_profit_type': '预期年化收益率', 'product_profit': '4.8-4.8%', 'risk_level': '中风险',
           'product_limit_time': '90天', 'start_time': '20170905', 'end_time': '20170911', 'start_amount': '100万',
           'limit_amount': '', 'url': 'http://www.cebbank.com/site/gryw/yglc/lccpsj/yxl94/48910196/index.html',
           'update_time': '', 'is_deleted': 0}
                 ]
    insert_to_mysql('bank_spider', 'invest_product', data_list)
