from conexion import conectar

def actualizar_nivel(userName):
    conn = conectar()
    cur = conn.cursor()

    cur.callproc('update_nivel',[userName,])

    cur.close()
    conn.commit()
    conn.close()

def isBanned(user_name):
    conn = conectar()
    cur = conn.cursor()

    cur.callproc('jugadorToxico',[user_name])
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result[0]

def porc_toxicos():
    conn=conectar()
    cur = conn.cursor()

    cur.callproc('porcentajeToxico',[])
    result = cur.fetchone()

    cur.close()
    conn.close()
    return result[0]

def top3():
    conn=conectar()
    cur = conn.cursor()
    top = []

    cur.callproc('topNiveles',[])
    result = cur.fetchall()
    for jug in result:
        top.append([jug[0],jug[1]])
    
    cur.close()
    conn.close()

    return top

    