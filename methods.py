import sqlite3

def crear_db(DB_NAME):
    """Crea la base de datos y la tabla de sorteos si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sorteos (
        sorteo_id INTEGER PRIMARY KEY,
        day INTEGER,
        month INTEGER,
        year INTEGER,
        week_day TEXT,
        n1_loto INTEGER,
        n2_loto INTEGER,
        n3_loto INTEGER,
        n4_loto INTEGER,
        n5_loto INTEGER,
        n6_loto INTEGER,
        comodin INTEGER,
        money_per_winner_loto INTEGER,
        amount_of_winners_loto INTEGER,
	    money_per_winner_super_quina INTEGER,
	    amount_of_winners_super_quina INTEGER,
	    money_per_winner_quina INTEGER,
	    amount_of_winners_quina INTEGER,
	    money_per_winner_super_cuaterna INTEGER,
	    amount_of_winners_super_cuaterna INTEGER,
	    money_per_winner_cuaterna INTEGER,
	    amount_of_winners_cuaterna INTEGER,
	    money_per_winner_super_terna INTEGER,
	    amount_of_winners_super_terna INTEGER,
	    money_per_winner_terna INTEGER,
	    amount_of_winners_terna INTEGER,
	    money_per_winner_super_dupla INTEGER,
	    amount_of_winners_super_dupla INTEGER,
	    n1_recargado INTEGER,
        n2_recargado INTEGER,
        n3_recargado INTEGER,
        n4_recargado INTEGER,
        n5_recargado INTEGER,
        n6_recargado INTEGER,
    	money_per_winner_recargado INTEGER,
	    amount_of_winners_recargado INTEGER,
        n1_revancha INTEGER,
        n2_revancha INTEGER,
        n3_revancha INTEGER,
        n4_revancha INTEGER,
        n5_revancha INTEGER,
        n6_revancha INTEGER,
    	money_per_winner_revancha INTEGER,
	    amount_of_winners_revancha INTEGER,
        n1_desquite INTEGER,
        n2_desquite INTEGER,
        n3_desquite INTEGER,
        n4_desquite INTEGER,
        n5_desquite INTEGER,
        n6_desquite INTEGER,
    	money_per_winner_desquite INTEGER,
	    amount_of_winners_desquite INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()