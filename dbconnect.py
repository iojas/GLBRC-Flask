import MySQLdb

def connection():
    conn = MySQLdb.connect(host='glbrc-cluster.cluster-crwqdxb9dkgh.us-west-2.rds.amazonaws.com',
                           user='glbrc',
                           passwd='rootroot',
                           db='glbrc')
    c= conn.cursor();
    return c, conn