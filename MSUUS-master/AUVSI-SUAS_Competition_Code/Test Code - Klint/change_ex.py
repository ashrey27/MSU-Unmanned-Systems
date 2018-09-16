def update_val(conn, c):
    c.execute("UPDATE test SET visited='True', value=1 WHERE visited='False' AND value=0")
    conn.commit()