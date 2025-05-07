from Detail_student import Detail_student
from Chat_Bot import Chat_Bot
from Phan_Loai import Phan_Loai
from tkinter import *
import sqlite3
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xlrd
from datetime import datetime
from datetime import datetime, timedelta


class TrangChu:
    def __init__(self, root):

        self.root = root
        self.root.title("Trang hiển thị thông tin")
        self.root.geometry("1550x800")
        self.connect_db()

        #===================== Lấy dữ liệu từ entry ===========================
        self.Dot = StringVar()
        self.MaLop= StringVar()
        self.TenMonHoc = StringVar()
        self.HoTen = StringVar()
        self.Mssv = StringVar()

        self.FindHoten =StringVar() # này là tìm  kiếm
        self.FindMasv =IntVar() # này là mã sinh viên

        #====================== Frame khung đầu tiên ===============================
        label_title = Label(self.root, text="Hiển thị thông tin", bg="powder blue", fg="green", bd=10,
                            relief=RIDGE, font=("time new roman", 50, "bold"), padx=2, pady=1)
        label_title.pack(side=TOP, fill=X)


        #===========Frame information======================
        Dataframe_information = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_information.place(x=0, y=100, width=1530, height=200)

        #================= inside Frame information================

        lb_Dot = Label(Dataframe_information, font=("arial", 12, "bold"), text="Đợt:", padx=2)
        lb_Dot.grid(row=0, column=0, sticky=W)
        self.txt_Dot = Entry(Dataframe_information,textvariable= self.Dot, font=("arial", 13, "bold"), width=25)
        self.txt_Dot.grid(row=0, column=1)

        lb_MaLop = Label(Dataframe_information, font=("arial", 12, "bold"), text="Mã lớp:", padx=2, pady=4)
        lb_MaLop.grid(row=1, column=0, sticky=W)
        self.txt_MaLop = Entry(Dataframe_information,textvariable=self.MaLop, font=("arial", 13, "bold"), width=25)
        self.txt_MaLop.grid(row=1, column=1)

        lb_NameSubject = Label(Dataframe_information, font=("arial", 12, "bold"), text="Tên môn học:", padx=2, pady=6)
        lb_NameSubject.grid(row=2, column=0, sticky=W)
        self.txt_NameSubject = Entry(Dataframe_information,textvariable=self.TenMonHoc, font=("arial", 13, "bold"), width=25)
        self.txt_NameSubject.grid(row=2, column=1)

        lb_name = Label(Dataframe_information, font=("arial", 12, "bold"), text="họ tên SV:", padx=2, pady=6)
        lb_name.grid(row=3, column=0, sticky=W)
        self.txt_name = Entry(Dataframe_information,textvariable=self.HoTen, font=("arial", 13, "bold"), width=25)
        self.txt_name.grid(row=3, column=1)

        lb_MSSV = Label(Dataframe_information, font=("arial", 12, "bold"), text="Mã số sinh viên:", padx=2, pady=6)
        lb_MSSV.grid(row=4, column=0, sticky=W)
        self.txt_MSSV = Entry(Dataframe_information,textvariable=self.Mssv, font=("arial", 13, "bold"), width=25)
        self.txt_MSSV.grid(row=4, column=1)


        #======================BUTTON FRAME=====================
        Buttonframe = Frame(self.root, bd=5, relief=RIDGE)
        Buttonframe.place(x=0, y=280, width=1530, height=50)

        btn_file = Button(Buttonframe, text="Import", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=14,
                          height=1, padx=1, pady=1 ,command = self.select_excel_file)#command=self.load_excel_file)
        btn_file.grid(row=0, column=0)
        btn_add = Button(Buttonframe, text="Thêm", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=14, height=1, padx=1, pady=1,command = self.add_student)
        btn_add.grid(row=0, column=1)
        btn_remove = Button(Buttonframe, text="Xóa", bg="green", fg="white", font=("arial", 13, "bold"),
                         width=14,
                         height=1, padx=1, pady=1 , command=self.delete_student)
        btn_remove.grid(row=0, column=2)
        btn_reset = Button(Buttonframe, text="Resets", bg="green", fg="white", font=("arial", 13, "bold"),
                         width=14,
                         height=1, padx=1, pady=1 ,command = self.clear_entry)
        btn_reset.grid(row=0, column=3)
        btn_view = Button(Buttonframe, text="Hiển thị", bg="green", fg="white", font=("arial", 13, "bold"),
                         width=14,
                         height=1, padx=1, pady=1, command = self.fetch_data)
        btn_view.grid(row=0, column=4)
        btn_view = Button(Buttonframe, text="Thông tin SV", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=14,
                          height=1, padx=1, pady=1, command=self.show_detail)
        btn_view.grid(row=0, column=5)
        btn_view = Button(Buttonframe, text="Học vụ", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=14,
                          height=1, padx=1, pady=1,command=self.open_phan_loai)
        btn_view.grid(row=0, column=6)

        btn_chatbot = Button(Buttonframe, text="Hỗ trợ", bg="green", fg="white", font=("arial", 13, "bold"),
                         width=14, height=1, padx=1, pady=1, command=self.chat_bot)
        btn_chatbot.grid(row=0, column=7)
        #======================== BUTTON FIND ================================
        FindFrame = Frame(self.root, bd=5, relief=RIDGE)
        FindFrame.place(x=0, y=330, width=1530, height=50)

        lb_TimKiemHoTen = Label(FindFrame, font=("arial", 12, "bold"), text="Họ/Tên:", padx=2)
        lb_TimKiemHoTen.grid(row=0, column=0, sticky=W)
        txt_TimKiemHoTen = Entry(FindFrame, textvariable=self.FindHoten, font=("arial", 13, "bold"), width=25)
        txt_TimKiemHoTen.grid(row=0, column=1)

        lb_TimKiemMasv = Label(FindFrame, font=("arial", 12, "bold"), text="Massv:", padx=2)
        lb_TimKiemMasv.grid(row=0, column=2, sticky=W)
        txt_TimKiemMasv = Entry(FindFrame, textvariable=self.FindMasv, font=("arial", 13, "bold"), width=25)
        txt_TimKiemMasv.grid(row=0, column=3)

        btn_file = Button(FindFrame, text="Tìm kiếm", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=15,
                          height=1, padx=1, pady=1,command=self.find_student)  # command=self.load_excel_file)
        btn_file.grid(row=0, column=4)

        # ================= table view=======
        #Dataframe_view = Frame(self.root, bd=10, relief=RIDGE)
        #Dataframe_view.place(x=0, y=330, width=1530, height=400)

        # ================= table view=======
        Dataframe_view = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_view.place(x=0, y=380, width=1530, height=400)

        # ========================================Scrollbar =======================================
        scroll_x = ttk.Scrollbar(Dataframe_view, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Dataframe_view, orient=VERTICAL)
        self.InforStudent_table = ttk.Treeview(Dataframe_view, column=("Dot","Malop","Tenmonhoc","HotenSV","MaSV"), xscrollcommand=scroll_x.set,
                                           yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = ttk.Scrollbar(command=self.InforStudent_table.xview)
        scroll_y = ttk.Scrollbar(command=self.InforStudent_table.yview)


        self.InforStudent_table.heading("Dot", text="Đợt")
        self.InforStudent_table.heading("Malop", text="Mã lớp")
        self.InforStudent_table.heading("Tenmonhoc", text="Tên môn học")
        self.InforStudent_table.heading("HotenSV", text="Họ tên SV")
        self.InforStudent_table.heading("MaSV", text="Mã sinh viên")
        self.InforStudent_table["show"] = "headings"

        self.InforStudent_table.column("MaSV", width=100)
        self.InforStudent_table.column("Dot", width=100)
        self.InforStudent_table.column("Malop", width=100)
        self.InforStudent_table.column("Tenmonhoc", width=100)
        self.InforStudent_table.column("HotenSV", width=100)

        self.InforStudent_table.pack(fill=BOTH, expand=1)
        self.InforStudent_table.bind("<ButtonRelease-1>",self.get_cursor)



    def connect_db(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS StudentDB (
                        MSSV VARCHAR(20) PRIMARY KEY,
                        Ho_Ten VARCHAR(50),
                        Gender TEXT,
                        Birth_Date TEXT
                    )
                ''')
        conn.commit()
        conn.close()

    def fetch_data(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Lop.Dot, Lop.Ma_Lop, Lop.Ten_Mon_Hoc, StudentDB.Ho_Ten,  StudentDB.MSSV FROM StudentDB,LopSinhVien,Lop WHERE StudentDB.MSSV = LopSinhVien.MSSV AND LopSinhVien.Ma_Lop = Lop.Ma_Lop")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            self.data_list = []  # Khởi tạo danh sách để lưu trữ dữ liệu
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
                self.data_list.append(i)  # Thêm từng hàng vào danh sách

            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.InforStudent_table.focus()
        if cursor_row:  # Kiểm tra xem có hàng nào được chọn không
            content = self.InforStudent_table.item(cursor_row)
            row = content["values"]

            # Lấy chỉ số của hàng được chọn
            index = self.InforStudent_table.index(cursor_row)
            selected_data = self.data_list[index]  # Lấy dữ liệu từ danh sách
            #messagebox.showinfo("Thông tin dong_2", f"dong_2: {selected_data[1]}, Type: {type(selected_data[1])}")

            # Gán giá trị vào Entry, giữ nguyên định dạng của Ma_Lop
            self.Dot.set(selected_data[0])
            self.MaLop.set(str(selected_data[1]))  # Đảm bảo giữ nguyên chuỗi
            self.TenMonHoc.set(selected_data[2])
            self.HoTen.set(selected_data[3])
            self.Mssv.set(selected_data[4])
        else:
            # Nếu không có hàng nào được chọn, bạn có thể đặt các trường về giá trị mặc định
            self.clear_entry()

    def add_student(self):

        db_path = r'test_du_lieu_chay_thu.db'
        try:
            # Kết nối tới cơ sở dữ liệu SQLite
            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            # Kiểm tra các trường không được để trống
            if not self.Dot.get() or not self.MaLop.get() or not self.TenMonHoc.get() or not self.HoTen.get() or not self.Mssv.get():
                messagebox.showwarning("Nhập lỗi", "Vui lòng nhập vào tất cả các ô!")
                return
            cursor.execute("SELECT COUNT(*) FROM StudentDB WHERE MSSV = ?", (self.Mssv.get(),))
            result = cursor.fetchone()
            if result[0] > 0:
                messagebox.showwarning("Trùng lặp", "Sinh viên đã tồn tại trong cơ sở dữ liệu!")
                return


            # Thực hiện câu lệnh SQL để thêm dữ liệu vào bảng studentDB
            cursor.execute("INSERT INTO StudentDB (MSSV,Ho_Ten,Gender,Birth_Date) VALUES (?, ?, ?, ?)",
                           ( self.Mssv.get(), self.HoTen.get(),"Nam","24/10/2003"))


            # Thực hiện truy vấn để kiểm tra mã  lớp
            cursor.execute("SELECT 1 FROM Lop WHERE Ma_Lop = ?", (self.MaLop.get(),))
            result_2 = cursor.fetchone()  # Lấy kết quả truy vấn
            # Kiểm tra nếu không có kết quả, nghĩa là Lớp đó  không tồn tại
            if result_2 is None:
                cursor.execute("INSERT INTO Lop(Ma_Lop,Ten_Lop,Ten_Mon_Hoc,Dot) VALUES (?, ?, ?, ?)",
                           (self.MaLop.get(),"DCT121C5",self.TenMonHoc.get(), self.Dot.get()))
            cursor.execute("INSERT INTO LopSinhVien(Ma_Lop,MSSV) VALUES (?, ?)",
                               (self.MaLop.get(), self.Mssv.get(),))


            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm sinh viên thành công!")

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")



        #self.connect_db()
    def delete_student(self):
        db_path = r'test_du_lieu_chay_thu.db'

        try:
            # Kết nối tới cơ sở dữ liệu SQLite
            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()
            if not self.Dot.get() or not self.MaLop.get() or not self.TenMonHoc.get() or not self.HoTen.get() or not self.Mssv.get():
                messagebox.showwarning("Xóa lỗi", "Vui lòng chọn vào ô!")
                return
            cursor.execute(f"DELETE FROM StudentDB WHERE MSSV= {self.Mssv.get()}")

            cursor.execute(f"DELETE FROM LopSinhVien WHERE MSSV= {self.Mssv.get()}")

            cursor.execute(f"DELETE FROM DiemDanh WHERE student_id= {self.Mssv.get()}")

            cursor.execute(f"DELETE FROM Tong_Cong WHERE student_id= {self.Mssv.get()}")
            messagebox.showinfo("Thành công", "Đã xóa sinh viên thành công!")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")
        finally:
            if conn:
                conn.commit()
                conn.close()
    def clear_entry(self):
        self.Dot.set("")
        self.MaLop.set("")
        self.TenMonHoc.set("")
        self.HoTen.set("")
        self.Mssv.set(0)
    #def show(self):

    #=================== Find student by name and MSSV ========================
    def find_student(self):
        db_path = r'test_du_lieu_chay_thu.db'

        try:
            # Kết nối tới cơ sở dữ liệu SQLite
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Kiểm tra xem người dùng có nhập vào cả MSSV hoặc họ tên sinh viên hay không
            if not self.FindHoten.get() and not self.FindMasv.get():
                messagebox.showwarning("Cảnh báo!", "Vui lòng nhập vào MSSV hoặc họ tên để tìm kiếm!")
                return

            if self.FindMasv.get() and self.FindMasv.get() != "0":
                cursor.execute("SELECT * FROM StudentDB WHERE MSSV = ?", (self.FindMasv.get(),))

                # Nếu họ tên có giá trị thì tìm theo họ tên

            elif self.FindHoten.get():
                cursor.execute("SELECT * FROM StudentDB WHERE Ho_Ten LIKE ?  ", ('%' + self.FindHoten.get() + '%',))
            # Lấy kết quả tìm kiếm
            rows = cursor.fetchall()

            if len(rows) != 0:
                self.InforStudent_table.delete(*self.InforStudent_table.get_children())
                for row in rows:
                    self.InforStudent_table.insert("", tk.END, values=row)
                messagebox.showinfo("Thành công", "Tìm kiếm thành công!")
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy sinh viên phù hợp.")

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

        finally:
            if conn:
                conn.close()

    import sqlite3
    import xlrd
    from datetime import datetime

    def import_Student_excel_to_db(self, file_path):
        # Kết nối tới cơ sở dữ liệu
        db_path = r'test_du_lieu_chay_thu.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Mở file Excel
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)

        # Lấy thông tin lớp học
        Ma_Lop = sheet.cell_value(7, 2)  # Ví dụ: Row 8, Column 3
        Ten_Lop = sheet.cell_value(9, 2)
        Ten_Mon_Hoc = sheet.cell_value(8, 2)
        Dot = sheet.cell_value(5, 2)

        # Tạo bảng Lop nếu chưa tồn tại và chèn dữ liệu vào bảng Lop
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Lop (
                Ma_Lop VARCHAR(20) PRIMARY KEY,
                Ten_Lop VARCHAR(50),
                Ten_Mon_Hoc VARCHAR(50),
                Dot VARCHAR(50)
            )
        ''')
        cursor.execute("INSERT OR IGNORE INTO Lop (Ma_Lop, Ten_Lop, Ten_Mon_Hoc, Dot) VALUES (?, ?, ?, ?)",
                       (Ma_Lop, Ten_Lop, Ten_Mon_Hoc, Dot))

        # Tạo bảng StudentDB nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS StudentDB (
                MSSV VARCHAR(20) PRIMARY KEY,
                Ho_Ten VARCHAR(50),
                Gender TEXT,
                Birth_Date TEXT
            )
        ''')

        # Tạo bảng LopSinhVien nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LopSinhVien (
                Ma_Lop VARCHAR(20),
                MSSV VARCHAR(20),
                FOREIGN KEY (Ma_Lop) REFERENCES Lop(Ma_Lop) ON DELETE CASCADE,
                FOREIGN KEY (MSSV) REFERENCES StudentDB(MSSV) ON DELETE CASCADE
            )
        ''')

        # Lấy dữ liệu sinh viên từ file Excel
        data = []
        columns_indices = [2, 3, 4, 5,6]  # Cột chứa MSSV, Ho_Ten, Gender, Birth_Date
        row_number = 13

        while row_number < sheet.nrows:
            row_data = [sheet.cell_value(row_number, col- 1) for col in columns_indices]

            if all(value == '' for value in row_data):
                break

            data.append(row_data)
            row_number += 1

        for row in data:
            MSSV, Ho_Ten, Gender,  = row[0], f"{row[1]} {row[2]}", row[3]
            Ngay_Sinh = row[4]

            datetime_str  = self.excel_date_to_datetime(Ngay_Sinh)
            # Định dạng lại chỉ lấy ngày
            formatted_date = datetime_str.strftime("%Y-%m-%d")

            # Chèn vào bảng StudentDB nếu chưa tồn tại
            cursor.execute("INSERT OR IGNORE INTO StudentDB (MSSV, Ho_Ten, Gender, Birth_Date) VALUES (?, ?, ?, ?)",
                           (MSSV, Ho_Ten, Gender, formatted_date))

            # Kiểm tra nếu cặp Ma_Lop và MSSV chưa tồn tại trong LopSinhVien trước khi chèn
            cursor.execute("SELECT 1 FROM LopSinhVien WHERE Ma_Lop = ? AND MSSV = ?", (Ma_Lop, MSSV))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute("INSERT INTO LopSinhVien (Ma_Lop, MSSV) VALUES (?, ?)", (Ma_Lop, MSSV))

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()

        print("Dữ liệu đã được chèn vào cơ sở dữ liệu thành công!")

    # Gọi hàm để lấy dữ liệu
    import sqlite3
    import xlrd

    def convert_to_float(self, value):
        """Chuyển đổi giá trị sang float, xử lý dấu phẩy và dấu chấm."""
        if isinstance(value, str):
            # Thay thế dấu phẩy bằng dấu chấm nếu có
            value = value.replace(',', '.')
            try:
                # Chuyển đổi chuỗi thành float
                return float(value)
            except ValueError:
                return 0.0  # Nếu không thể chuyển đổi, trả về 0.0
        elif isinstance(value, int):
            # Chuyển đổi số nguyên thành chuỗi và thêm .0
            return float(f"{value}.0")  # Ví dụ: 100 -> '100.0' -> 100.0
        elif isinstance(value, float):
            return value  # Nếu đã là float thì giữ nguyên
        return 0.0  # Giá trị không hợp lệ trả về 0.0

    def import_tong_cong_sv(self, file_path):
        # Mở file Excel với định dạng .xls
        db_path = r'test_du_lieu_chay_thu.db'
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)  # Lấy sheet đầu tiên
        Ma_Lop_C5 = sheet.cell_value(7, 2)  # Lấy giá trị tại vị trí C7

        # Các cột cần lấy dữ liệu (Mã sinh viên, Số ngày vắng mặt, Số ngày có mặt, Tổng số ngày, Tỷ lệ vắng mặt)
        columns_indices = [1, 24, 25, 26,
                           27]  # Cột Mã sinh viên, Số ngày vắng mặt, Số ngày có mặt, Tổng số ngày, Tỷ lệ vắng mặt

        data = []
        row_number = 13  # Dòng dữ liệu bắt đầu từ dòng 14 (trong xlrd, chỉ số bắt đầu từ 0)

        # Duyệt qua các hàng cho đến khi hết dữ liệu
        while row_number < sheet.nrows:
            row_data = []
            for col in columns_indices:
                cell_value = sheet.cell_value(row_number, col)
                row_data.append(cell_value)  # Lưu giá trị vào danh sách

            # Kiểm tra xem dòng có trống hay không
            if all(value == '' or value is None for value in row_data):
                break  # Dừng vòng lặp nếu tất cả các giá trị đều trống

            data.append(row_data)  # Thêm dữ liệu dòng vào danh sách
            row_number += 1  # Tăng dòng lên để lấy dòng tiếp theo

        # Kết nối tới cơ sở dữ liệu
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Tạo bảng Tong_Cong nếu chưa tồn tại
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tong_Cong (
                student_id VARCHAR(20),     -- Khóa ngoại là Mã sinh viên
                Ma_Lop VARCHAR(20),
                Vang_P INTEGER,             -- Số ngày vắng mặt
                Vang_K INTEGER,             -- Số ngày có mặt
                Tong_T INTEGER,             -- Tổng số ngày
                Vang_Phan_Tram FLOAT,       -- Tỷ lệ vắng mặt (dưới dạng phần trăm)
                FOREIGN KEY (student_id) REFERENCES student_DB(student_id) ON DELETE CASCADE,
                FOREIGN KEY (Ma_Lop) REFERENCES Lop(Ma_Lop) ON DELETE CASCADE
            )
            ''')

            # Chèn dữ liệu vào bảng Tong_Cong
            for row in data:
                try:
                    # Chuyển đổi và xử lý giá trị
                    student_id = row[0]  # Mã sinh viên
                    Vang_P = row[1]  # Số ngày vắng mặt
                    Vang_K = row[2] # Số ngày có mặt
                    Tong_T = row[3]  # Tổng số ngày
                    Vang_Phan_Tram = self.convert_to_float(row[4])  # Tỷ lệ vắng mặt

                    cursor.execute('''
                        INSERT INTO Tong_Cong (student_id, Ma_Lop, Vang_P, Vang_K, Tong_T, Vang_Phan_Tram) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (student_id, Ma_Lop_C5, Vang_P, Vang_K, Tong_T, Vang_Phan_Tram))
                except sqlite3.IntegrityError as e:
                    print(f"Đã xảy ra lỗi khi chèn dữ liệu cho tổng cộng của sinh viên {row[0]}: {e}")
                except Exception as e:
                    print(f"Đã xảy ra lỗi khác: {e}")

        print("Dữ liệu đã được chèn vào cơ sở dữ liệu thành công!")

    def import_data_to_db(self,file_path ):
        # Kết nối đến cơ sở dữ liệu
        # Kết nối đến cơ sở dữ liệu
        db_path = r'test_du_lieu_chay_thu.db'
        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        # Mở file Excel
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)  # Lấy sheet đầu tiên

        Ma_Lop_C5 = sheet.cell_value(7, 2)  # lấy vị trí C7

        # Các cột cần lấy dữ liệu
        columns_to_extract = [7, 10, 13, 16, 19, 22]
        start_row = 14
        fixed_column = 2

        for base_col in columns_to_extract:
            row_number = start_row
            date_info = sheet.cell(11, base_col - 1).value  # Sửa cú pháp để lấy đúng giá trị

            while True:
                if row_number > sheet.nrows:  # Kiểm tra vượt quá số dòng trong sheet
                    break

                # Lấy dữ liệu từ cột cố định (cột số 2)
                fixed_col_value = sheet.cell(row_number - 1, fixed_column - 1).value  # Điều chỉnh chỉ số dòng và cột
                ld_value = []  # Khởi tạo ld_value cho mỗi dòng

                # Lấy dữ liệu từ cột base_col và các cột tiếp theo
                for offset in range(0, 3):  # Lấy từ cột base_col và 2 cột sau
                    cell_value = sheet.cell(row_number - 1, base_col + offset - 1).value  # Điều chỉnh chỉ số
                    ld_value.append(cell_value)

                # Kiểm tra xem dòng có trống hay không
                if all(value is None for value in ld_value):
                    break  # Dừng vòng lặp nếu tất cả các giá trị đều là None

                # Kiểm tra và lấy giá trị từ ld_value
                ld_values_to_insert = [str(value) if value is not None else None for value in ld_value]

                # Giả sử giá trị P_K nằm ở ld_value[0] (hoặc vị trí nào mà bạn xác định)
                p_k_value = ld_values_to_insert[0] if len(ld_values_to_insert) > 0 else None
                st_value = ld_values_to_insert[1] if len(ld_values_to_insert) > 1 else None

                # Câu lệnh SQL để tạo bảng DiemDanh nếu chưa tồn tại
                create_table_sql = '''
                    CREATE TABLE IF NOT EXISTS DiemDanh (
                        student_id VARCHAR(20),  -- Khóa ngoại tới student_DB
                        Ma_Lop VARCHAR(20),
                        ngay_id VARCHAR(50),  -- Ngày từ Ngay_DB
                        P_K VARCHAR(5),  -- P/K để lưu trạng thái
                        ST INTEGER,  -- ST để lưu số thứ tự
                        LD TEXT,  -- LD để lưu thông tin liên quan,
                        FOREIGN KEY (Ma_Lop) REFERENCES Lop(Ma_Lop) ON DELETE CASCADE,
                        FOREIGN KEY (student_id) REFERENCES student_DB(student_id) ON DELETE CASCADE
                    );
                    '''

                # Thực hiện câu lệnh tạo bảng
                cursor.execute(create_table_sql)

                # Kiểm tra xem student_id và ngay_id đã tồn tại trong cơ sở dữ liệu chưa
                cursor.execute('''
                    SELECT 1 FROM DiemDanh WHERE student_id = ? AND ngay_id = ?
                ''', (fixed_col_value, date_info))
                exists = cursor.fetchone()

                # Nếu chưa tồn tại thì thực hiện chèn dữ liệu
                if exists is None:
                    cursor.execute('''
                        INSERT INTO DiemDanh (student_id,Ma_Lop, ngay_id, P_K, ST, LD)
                        VALUES (?,?, ?, ?, ?, ?)
                    ''', (fixed_col_value,Ma_Lop_C5, date_info, p_k_value, st_value,
                          ld_values_to_insert[2] if len(ld_values_to_insert) > 2 else None))

                row_number += 1  # Tăng dòng lên để lấy dòng tiếp theo

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()

    def select_excel_file(self):
        # Khởi tạo giao diện tkinter (ẩn cửa sổ chính)
        root = Tk()
        root.withdraw()  # Ẩn cửa sổ tkinter

        # Hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            title="Chọn file Excel",
            filetypes=[("Excel files", "*.xls")]  # Chỉ file .xls
        )

        if file_path:  # Kiểm tra nếu file_path không rỗng
            # Gọi các hàm nhập dữ liệu và truyền file_path vào
            self.import_Student_excel_to_db(file_path)
            self.import_data_to_db(file_path)
            self.import_tong_cong_sv(file_path)

    def check_ma_sv(self, mssv):
        # Kết nối đến cơ sở dữ liệu
        connection = sqlite3.connect('test_du_lieu_chay_thu.db')  # Thay thế bằng tên cơ sở dữ liệu của bạn
        cursor = connection.cursor()

        # Thực hiện truy vấn để kiểm tra mã số sinh viên (MSSV)
        cursor.execute("SELECT COUNT(*) FROM StudentDB WHERE MSSV = ?", (mssv,))
        result = cursor.fetchone()  # Lấy kết quả truy vấn

        # Kiểm tra nếu không có kết quả, nghĩa là sinh viên không tồn tại
        if result is None or result[0] == 0:
            count = 0  # Mã sinh viên không tồn tại, trả về 0
        else:
            count = 1  # Mã sinh viên tồn tại, trả về 1

        # Đóng kết nối
        cursor.close()
        connection.close()

        return count

    def excel_date_to_datetime(self,serial):
        base_date = datetime(1900, 1, 1)  # Ngày gốc trong Excel
        delta = timedelta(days=serial - 2)  # Trừ 2 vì Excel tính sai năm nhuận 1900
        return base_date + delta
    def show_detail(self):
        # Kiểm tra xem mã sinh viên có tồn tại
        if self.Mssv.get() == "":
            messagebox.showwarning("Thông báo", "Vui lòng chọn dữ liệu trong bảng!")
            return  # Ngưng thực hiện nếu mã sinh viên không hợp lệ

        if self.check_ma_sv(self.Mssv.get()) == 0:
            messagebox.showwarning("Thông báo", "Mã sinh viên không tồn tại, vui lòng chọn dữ liệu trong bảng!")
            return  # Ngưng thực hiện nếu mã sinh viên không tồn tại

        # Truyền dữ liệu cho lớp Detail_student
        detail_window = Toplevel(self.root)  # Tạo một cửa sổ mới với Toplevel
        Detail_student(detail_window, self.Mssv.get())  # Truyền mã sinh viên cho Detail_student

    def open_phan_loai(self):
        self.root.withdraw()  # Ẩn cửa sổ chính
        self.root_phan_loai = Toplevel(self.root)  # Tạo một cửa sổ mới
        self.root_phan_loai.title("Phan Loai")
        Phan_Loai(self.root_phan_loai)  # Khởi tạo lớp Phan_Loai với cửa sổ mới
        self.root_phan_loai.protocol("WM_DELETE_WINDOW", self.Phan_Loai_on_closing)  # Đặt hàm đóng khi cửa sổ bị đóng
        self.root_phan_loai.mainloop()

    def chat_bot(self):
        self.root.withdraw()  # Ẩn cửa sổ chính

        self.chatbot_window = Toplevel(self.root)
        self.chatbot_window.title("Chat Box")

        # Thêm nội dung vào ChatBox
        Chat_Bot( self.chatbot_window)  # Khởi tạo lớp Phan_Loai với cửa sổ mới

        # Đặt sự kiện khi đóng cửa sổ ChatBox
        self.chatbot_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.chatbot_window.mainloop()

    def on_closing(self):
        self.chatbot_window.destroy()
        self.root.deiconify()  # Hiện lại cửa sổ chính khi cửa sổ Phan_Loai bị đóng
    def Phan_Loai_on_closing(self):
        self.root_phan_loai.destroy()
        self.root.deiconify()  # Hiện lại cửa sổ chính khi cửa sổ Phan_Loai bị đóng
if __name__ == "__main__":
    root = Tk()
    obj = TrangChu(root)
    root.mainloop()