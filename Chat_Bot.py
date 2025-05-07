import tkinter as tk
import sqlite3


class Chat_Bot:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot Quản Lý Học Sinh")

        # Tạo cơ sở dữ liệu nếu chưa tồn tại
        self.connect_db()

        # Giao diện ChatBot
        self.chat_log = tk.Text(self.root, bg="white", font=("Arial", 12), state=tk.DISABLED, width=50, height=20)
        self.chat_log.pack(padx=10, pady=10)

        self.chat_log.tag_configure("user", justify="right")
        self.chat_log.tag_configure("bot", justify="left")

        intro_message = (
            "Xin chào! Tôi là ChatBot Quản Lý Học Sinh.\n"
            "Tôi có thể giúp bạn thực hiện các công việc nhanh chóng:\n\n"
            "👉 Ví dụ: 'id 101', 'lớp 10A1'.\n"
        )
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"Bot: {intro_message}\n", "bot")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)

        self.entry = tk.Entry(self.root, font=("Arial", 12), width=40)
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        send_button = tk.Button(self.root, text="Gửi", font=("Arial", 12), bg="blue", fg="white", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

    def connect_db(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS StudentDB (
                MSSV VARCHAR(20) PRIMARY KEY,
                Ho_Ten VARCHAR(50),
                Gender TEXT,
                Birth_Date DATE
            )
        ''')

        conn.commit()
        conn.close()

    def send_message(self):
        user_message = self.entry.get().strip()
        if user_message:
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(tk.END, f"Bạn: {user_message}\n", "user")
            self.entry.delete(0, tk.END)

            bot_response = self.handle_query(user_message)
            self.chat_log.insert(tk.END, f"Bot: {bot_response}\n", "bot")

        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)

    def handle_query(self, query):
        if "id" in query.lower() and "lớp" in query.lower():
            # Trường hợp nhập cả ID và lớp
            student_id = self.extract_id(query)
            class_name = self.extract_class(query)
            if student_id and class_name:
                return self.get_student_by_id_and_class(student_id, class_name)
            else:
                return "Vui lòng cung cấp cả ID và lớp hợp lệ. Ví dụ: 'id 101 lớp 10A1'."
        elif "lớp" in query.lower() and "vắng bao nhiêu" in query.lower():
            class_name = self.extract_class(query)
            if class_name:
                return self.get_absence_statistics_by_class(class_name)
            else:
                return "Vui lòng cung cấp lớp hợp lệ. Ví dụ: 'lớp 10A1 vắng'."
        elif "id" in query.lower():
            student_id = self.extract_id(query)
            if student_id:
                return self.get_student_by_id(student_id)
            else:
                return "Vui lòng cung cấp ID hợp lệ. Ví dụ: 'id 101'."
        elif "lớp" in query.lower():
            class_name = self.extract_class(query)
            if class_name:
                return self.get_students_by_class(class_name)
            else:
                return "Vui lòng cung cấp lớp hợp lệ. Ví dụ: 'lớp 10A1'."
        elif "Hi" or "hi" or "Xin chào" in query.lower():
            return "Xin chào! Tôi có thể hỗ trợ bạn điều gì hôm nay?"
        else:
            return "Xin lỗi, tôi không hiểu. Bạn có thể hỏi về ID hoặc lớp học sinh."

    def get_student_by_id(self, student_id):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT StudentDB.MSSV, StudentDB.Ho_Ten, StudentDB.Gender, StudentDB.Birth_Date, Lop.Ten_Lop
            FROM StudentDB
            JOIN LopSinhVien ON StudentDB.MSSV = LopSinhVien.MSSV
            JOIN Lop ON LopSinhVien.Ma_Lop = Lop.Ma_Lop
            WHERE StudentDB.MSSV = ?
        ''', (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            return (
                f"Thông tin học sinh:ID: {student[0]},Tên: {student[1]},Giới tính: {student[2]},Ngày sinh: {student[3]},Lớp: {student[4]}\n"
            )
        else:
            return "Không tìm thấy học sinh với ID đã nhập."

    def get_students_by_class(self, class_name):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT StudentDB.MSSV, StudentDB.Ho_Ten
            FROM StudentDB
            JOIN LopSinhVien ON StudentDB.MSSV = LopSinhVien.MSSV
            JOIN Lop ON LopSinhVien.Ma_Lop = Lop.Ma_Lop
            WHERE Lop.Ten_Lop = ?
        ''', (class_name,))
        students = cursor.fetchall()
        conn.close()

        if students:
            response = f"Danh sách học sinh lớp {class_name}:\n"
            for student in students:
                response += f"- ID: {student[0]}, Tên: {student[1]}\n"
            return response
        else:
            return f"Không tìm thấy học sinh nào trong lớp {class_name}."

    def get_student_by_id_and_class(self, student_id, class_name):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT StudentDB.MSSV, StudentDB.Ho_Ten, StudentDB.Gender, StudentDB.Birth_Date, Lop.Ten_Lop
            FROM StudentDB
            JOIN LopSinhVien ON StudentDB.MSSV = LopSinhVien.MSSV
            JOIN Lop ON LopSinhVien.Ma_Lop = Lop.Ma_Lop
            WHERE StudentDB.MSSV = ? AND Lop.Ten_Lop = ?
        ''', (student_id, class_name))
        student = cursor.fetchone()
        conn.close()

        if student:
            return (
                f"Thông tin học sinh:\n"
                f"- ID: {student[0]}\n"
                f"- Tên: {student[1]}\n"
                f"- Giới tính: {student[2]}\n"
                f"- Ngày sinh: {student[3]}\n"
                f"- Lớp: {student[4]}\n"
            )
        else:
            return f"Không tìm thấy học sinh với ID '{student_id}' trong lớp '{class_name}'."

    def get_absence_statistics_by_class(self, class_name):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()

        # Lấy tổng số học sinh trong lớp
        cursor.execute('''
            SELECT COUNT(*)
            FROM StudentDB
            JOIN LopSinhVien ON StudentDB.MSSV = LopSinhVien.MSSV
            JOIN Lop ON LopSinhVien.Ma_Lop = Lop.Ma_Lop
            WHERE Lop.Ten_Lop = ?
        ''', (class_name,))
        total_students = cursor.fetchone()[0]

        if total_students == 0:
            conn.close()
            return f"Không tìm thấy thông tin lớp {class_name}."

        # Lấy số lượng học sinh vắng mặt
        cursor.execute('''
            SELECT COUNT(*)
            FROM Tong_Cong,Lop
            WHERE Tong_Cong.Ma_Lop = Lop.Ma_Lop AND Lop.Ten_Lop = ? AND Tong_Cong.Vang_Phan_Tram > 0
        ''', (class_name,))
        absent_students = cursor.fetchone()[0]
        conn.close()

        # Tính tỷ lệ vắng mặt
        absence_percentage = (absent_students / total_students) * 100

        return (
            f"Lớp {class_name} có {absent_students}/{total_students} học sinh vắng mặt.\n"
            f"Tỷ lệ vắng mặt: {absence_percentage:.2f}%."
        )
    def extract_id(self, query):
        words = query.split()
        for word in words:
            if word.isdigit():
                return word
        return None

    def extract_class(self, query):
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() == "lớp" and i + 1 < len(words):
                return words[i + 1]
        return None


# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    obj = Chat_Bot(root)
    root.mainloop()
