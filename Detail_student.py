import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk


class Detail_student:
    def __init__(self, root, ma_sinh_vien):
        self.root = root
        self.root.title("Thông tin sinh viên")
        self.root.geometry("700x700")
        self.Mssv = StringVar(value=ma_sinh_vien)  # Gán mã sinh viên
        self.So_Ngay_Vang = StringVar()
        self.Hoten = StringVar()
        self.GioiTinh = StringVar()
        self.NgaySinh = StringVar()
        # ==================Frame đầu =======================
        Dataframe_information = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_information.place(x=0, y=0, width=680, height=200)

        # =================== Labels in The first Frame ==================
        lb_Masv = Label(Dataframe_information, font=("arial", 12, "bold"), text="Mã sinh viên:", padx=2)
        lb_Masv.grid(row=0, column=0, sticky=W)

        # Entry hiển thị mã sinh viên, sử dụng self.Mssv
        txt_Masv = Entry(Dataframe_information, textvariable=self.Mssv, font=("arial", 13, "bold"), width=25,
                         state="readonly")
        txt_Masv.grid(row=0, column=1)

        lb_so_ngay_vang = Label(Dataframe_information, font=("arial", 12, "bold"), text="Tổng ngày vắng:", padx=2)
        lb_so_ngay_vang.grid(row=2, column=0, sticky=W)

        # Entry hiển thị tổng số ngày vắng, sử dụng self.So_Ngay_Vang
        txt_so_ngay_vang = Entry(Dataframe_information, textvariable=self.So_Ngay_Vang, font=("arial", 13, "bold"),
                                 width=25,
                                 state="readonly")
        txt_so_ngay_vang.grid(row=2, column=1)

        lb_hoten = Label(Dataframe_information, font=("arial", 12, "bold"), text="Họ tên:", padx=2)
        lb_hoten.grid(row=3, column=0, sticky=W)

        txt_hoten = Entry(Dataframe_information, textvariable=self.Hoten, font=("arial", 13, "bold"),
                                 width=25,
                                 state="readonly")
        txt_hoten.grid(row=3, column=1)

        lb_gioitinh = Label(Dataframe_information, font=("arial", 12, "bold"), text="Giới tính:", padx=2)
        lb_gioitinh.grid(row=4, column=0, sticky=W)
        txt_gioitinh = Entry(Dataframe_information, textvariable=self.GioiTinh, font=("arial", 13, "bold"),
                                 width=25,
                                 state="readonly")
        txt_gioitinh.grid(row=4, column=1)

        lb_birthday = Label(Dataframe_information, font=("arial", 12, "bold"), text="Ngày sinh:", padx=2)
        lb_birthday.grid(row=5, column=0, sticky=W)
        txt_ngaysinh = Entry(Dataframe_information, textvariable=self.NgaySinh, font=("arial", 13, "bold"),
                                 width=25,
                                 state="readonly")
        txt_ngaysinh.grid(row=5, column=1)
        # ================= table view =======
        Dataframe_view = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_view.place(x=0, y=220, width=690, height=400)

        # ========================================Scrollbar =======================================
        scroll_x = ttk.Scrollbar(Dataframe_view, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Dataframe_view, orient=VERTICAL)
        self.InforStudent_table = ttk.Treeview(Dataframe_view, column=("NgayVang"),
                                               xscrollcommand=scroll_x.set,
                                               yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.InforStudent_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.InforStudent_table.xview)
        scroll_y.config(command=self.InforStudent_table.yview)
        self.InforStudent_table.heading("NgayVang", text="Ngày Vắng")
        self.InforStudent_table["show"] = "headings"

        self.InforStudent_table.column("NgayVang", width=100)
        self.InforStudent_table.pack(fill=BOTH, expand=1)

        self.fetch_data()
        self.get_student_data()
        self.get_student_dat()

    def fetch_data(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ngay_id FROM DiemDanh WHERE student_id = ? AND ST > 0
        ''', (self.Mssv.get(),))  # Thêm dấu phẩy để biến thành tuple
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def get_student_data(self):
        # Kết nối tới cơ sở dữ liệu SQLite
        connection = sqlite3.connect(
            r'test_du_lieu_chay_thu.db')
        cursor = connection.cursor()

        # Thực hiện truy vấn SQL
        cursor.execute("""
            SELECT 
                StudentDB.Ho_Ten ,StudentDB.Gender ,StudentDB.Birth_Date
            FROM 
                DiemDanh ,StudentDB
            WHERE 
                StudentDB.MSSV = DiemDanh.student_id AND
                student_id = ? 
        """, (self.Mssv.get(),))

        # Lấy hàng đầu tiên từ kết quả
        data = cursor.fetchone()

        # Đóng kết nối sau khi lấy dữ liệu
        cursor.close()
        connection.close()

        # Cập nhật giá trị cho self.So_Ngay_Vang

        self.Hoten.set(data[0] if data else 0)
        self.GioiTinh.set(data[1] if data else 0)
        self.NgaySinh.set(data[2] if data else 0)
    def get_student_dat(self):
        # Kết nối tới cơ sở dữ liệu SQLite
        connection = sqlite3.connect(
            r'test_du_lieu_chay_thu.db')
        cursor = connection.cursor()

        # Thực hiện truy vấn SQL
        cursor.execute("""
            SELECT 
                COUNT(*) 
            FROM 
                DiemDanh 
            WHERE 
                student_id = ? AND ST > 0
        """, (self.Mssv.get(),))

        # Lấy hàng đầu tiên từ kết quả
        data = cursor.fetchone()

        # Đóng kết nối sau khi lấy dữ liệu
        cursor.close()
        connection.close()

        # Cập nhật giá trị cho self.So_Ngay_Vang
        self.So_Ngay_Vang.set(data[0] if data else 0)


if __name__ == "__main__":
    root = Tk()
    ma_sinh_vien = "SV12345"  # Ví dụ về mã sinh viên, bạn có thể thay đổi giá trị này
    obj = Detail_student(root, ma_sinh_vien)  # Truyền giá trị ma_sinh_vien khi khởi tạo
    root.mainloop()
