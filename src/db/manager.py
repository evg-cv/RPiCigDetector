import mysql.connector

from settings import HOST_NAME, USER_NAME, PASSWORD, DATABASE_NAME


class DatabaseManager:

    def __init__(self):
        self.connect = mysql.connector.connect(host=HOST_NAME, user=USER_NAME, password=PASSWORD,
                                               database=DATABASE_NAME)
        self.cursor = self.connect.cursor()
        self.__create_init_table()

    def __create_init_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS butt_numbers (ID INT AUTO_INCREMENT PRIMARY KEY, "
                            "T_Stamp VARCHAR(255), Butt_Number VARCHAR (255))")

        self.connect.commit()

    def insert_data(self, butt_num, t_stamp):

        insert_sql = "INSERT INTO butt_numbers (T_Stamp, Butt_Number) VALUES (%s, %s)"
        self.cursor.execute(insert_sql, (t_stamp, butt_num))
        self.connect.commit()

        print("[INFO] Successfully Inserted")

        return

    def read_data(self):
        self.cursor.execute("SELECT * FROM (SELECT * FROM butt_numbers ORDER BY id DESC LIMIT 30) sub ORDER BY id ")
        query_result = self.cursor.fetchall()

        return query_result

    def update_data(self, field, value, id_index):
        self.cursor.execute("SELECT id FROM butt_numbers")
        query_result = self.cursor.fetchall()
        if len(query_result) < 30:
            id_value = query_result[id_index]
        else:
            id_value = query_result[id_index - 30]

        update_sql = "UPDATE butt_numbers SET " + field + " = " + f"'{value}'" + " WHERE id = " + str(id_value[0])
        self.cursor.execute(update_sql)
        self.connect.commit()

        print(f"[INFO] {field}: {value} successfully updated")

    def delete_data(self, data_id):
        delete_sql = "DELETE FROM butt_numbers WHERE id = " + str(data_id)
        self.cursor.execute(delete_sql)
        self.connect.commit()

        print(f"User_Id:{data_id} successfully deleted")


if __name__ == '__main__':

    DatabaseManager().insert_data(butt_num="", t_stamp="")
