import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
#Sắp xếp và phân loại sinh viên vắng học theo: tổng buổi vắng, họ tên, lớp, tên môn học ,mssv
from tkinter.ttk import Combobox
from Send_Gmail import Send_Gmail
class Phan_Loai:
    def __init__(self, root):
        self.root = root
        self.root.title("Thông tin sinh viên")
        self.root.geometry("1550x800")

        self.Mssv = StringVar()  # Gán mã sinh viên
        self.So_Ngay_Vang = StringVar()
        self.Lop = StringVar()
        self.TenMonHoc = StringVar()
        self.HoTen = StringVar()

        self.combox_phan_loai = StringVar()

        # Gửi email
        self.receiver = StringVar()
        self.Title = StringVar()
        # ====================== Frame khung đầu tiên ===============================
        label_title = Label(self.root, text="Quản Lý Học Vụ", bg="powder blue", fg="green", bd=10,
                            relief=RIDGE, font=("time new roman", 50, "bold"), padx=2, pady=1)
        label_title.pack(side=TOP, fill=X)
        #======================= Second Frame  ===============================
        Dataframe_top = Frame(self.root, bd=5, relief=RIDGE)
        Dataframe_top.place(x=0, y=100, width=1530, height=50)

        lb_phan_loai = Label(Dataframe_top, font=("arial", 12, "bold"), text="Sắp xếp:", padx=2)
        lb_phan_loai.grid(row=0, column=0, sticky=W)
        self.combox_phan_loai = Combobox(Dataframe_top, state="readonly",
                                          font=("arial", 12, "bold"), width=25)

        self.combox_phan_loai["values"] = ("tổng buổi vắng", "họ tên","lớp","tên môn học")
        self.combox_phan_loai.current(0)
        self.combox_phan_loai.grid(row=0, column=1)

        btn_file = Button(Dataframe_top, text="Tìm kiếm", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=13,
                          height=1, padx=1, pady=1,command =self.Sort_student)  # command=self.load_excel_file)
        btn_file.grid(row=0, column=2)
        btn_CanhCao = Button(Dataframe_top, text="Cảnh cáo", bg="green", fg="white", font=("arial", 13, "bold"),
                          width=13,
                          height=1, padx=1, pady=1, command=self.Canh_Cao)  # command=self.load_excel_file)
        btn_CanhCao.grid(row=0, column=3)

        # ================= table view =======
        Dataframe_view = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_view.place(x=0, y=154, width=1530, height=500)

        # ========================================Scrollbar =======================================
        scroll_x = ttk.Scrollbar(Dataframe_view, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Dataframe_view, orient=VERTICAL)
        self.InforStudent_table = ttk.Treeview(Dataframe_view, column=("MSSV","Tong_Buoi_Vang","Ho_Ten","Lop","Ten_Mon_Hoc"),
                                               xscrollcommand=scroll_x.set,
                                               yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.InforStudent_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.InforStudent_table.xview)
        scroll_y.config(command=self.InforStudent_table.yview)
        self.InforStudent_table.heading("MSSV", text="Mã sinh viên")
        self.InforStudent_table.heading("Tong_Buoi_Vang", text="Tổng buổi vắng")
        self.InforStudent_table.heading("Ho_Ten", text="Họ và tên")
        self.InforStudent_table.heading("Lop", text="Lớp")
        self.InforStudent_table.heading("Ten_Mon_Hoc", text="Tên môn học")
        self.InforStudent_table["show"] = "headings"

        self.InforStudent_table.column("MSSV", width=100)
        self.InforStudent_table.column("Tong_Buoi_Vang", width=100)
        self.InforStudent_table.column("Ho_Ten", width=100)
        self.InforStudent_table.column("Lop", width=100)
        self.InforStudent_table.column("Ten_Mon_Hoc", width=100)

        self.InforStudent_table.pack(fill=BOTH, expand=1)

        self.fetch_data()
        self.InforStudent_table.bind("<ButtonRelease-1>", self.get_cursor)


    def fetch_data(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''Select 
            StudentDB.MSSV,
            SUM(CASE WHEN DiemDanh.ST > 0 THEN 1 ELSE 0 END) AS So_Ngay_Vang,
             StudentDB.Ho_Ten,
                Lop.Ten_Lop,
             Lop.Ten_Mon_Hoc
    
FROM 
    StudentDB,Lop,DiemDanh
Where
     Lop.Ma_Lop = DiemDanh.Ma_Lop AND StudentDB.MSSV = DiemDanh.student_id
GROUP BY 
    StudentDB.MSSV, StudentDB.Ho_Ten, Lop.Ten_Lop, Lop.Ten_Mon_Hoc;

        ''')
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
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
            self.Mssv.set(selected_data[0])
            self.So_Ngay_Vang.set(str(selected_data[1]))  # Đảm bảo giữ nguyên chuỗi
            self.Lop.set(selected_data[2])
            self.TenMonHoc.set(selected_data[3])
            self.HoTen.set(selected_data[4])


        else:
            # Nếu không có hàng nào được chọn, bạn có thể đặt các trường về giá trị mặc định
            self.clear_entry()
    def get_student_data(self):
        # Kết nối tới cơ sở dữ liệu SQLite
        connection = sqlite3.connect(
            r'test_du_lieu_chay_thu.db')  # Đặt tên đúng cho cơ sở dữ liệu của bạn
        cursor = connection.cursor()
        # Thực hiện truy vấn SQL
        cursor.execute("""
            SELECT 
                (Vang_P + Vang_K) AS Tong_Ngay_Vang
            FROM 
                Tong_Cong
            WHERE 
                student_id = ?  -- Cần thêm điều kiện để chỉ lấy dữ liệu của một sinh viên cụ thể
        """, (self.Mssv.get(),))  # Đặt student_id cụ thể vào đây
        # Lấy hàng đầu tiên từ kết quả (vì chúng ta chỉ cần một giá trị)
        data = cursor.fetchone()
        # Đóng kết nối sau khi lấy dữ liệu
        cursor.close()
        connection.close()
        # Cập nhật giá trị cho self.So_Ngay_Vang
        if data:
            self.So_Ngay_Vang.set(data[0])  # Nếu có dữ liệu, gán giá trị cho self.So_Ngay_Vang

    def Sort_student(self):
        # Kết nối tới cơ sở dữ liệu SQLite
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()

        # Lấy giá trị sắp xếp từ combobox
        sort_by = self.combox_phan_loai.get()

        # Xác định cột cần sắp xếp dựa trên lựa chọn
        order_column = None
        if sort_by == "tổng buổi vắng":
            order_column = "So_Ngay_Vang"
        elif sort_by == "họ tên":
            order_column = "StudentDB.Ho_Ten"
        elif sort_by == "lớp":
            order_column = "Lop.Ten_Lop"
        elif sort_by == "tên môn học":
            order_column = "Lop.Ten_Mon_Hoc"

        if order_column is None:
            # Nếu không có cột hợp lệ, có thể thông báo lỗi hoặc thoát hàm
            print("Không có cột nào để sắp xếp.")
            return

        # Thực hiện truy vấn SQL với ORDER BY
        query = f'''
        SELECT 
            StudentDB.MSSV,
            SUM(CASE WHEN DiemDanh.ST > 0 THEN 1 ELSE 0 END) AS So_Ngay_Vang,
            StudentDB.Ho_Ten,
            Lop.Ten_Lop,
            Lop.Ten_Mon_Hoc
        FROM 
            StudentDB,Lop,DiemDanh
        Where
            Lop.Ma_Lop = DiemDanh.Ma_Lop AND StudentDB.MSSV = DiemDanh.student_id
        GROUP BY 
            StudentDB.MSSV, StudentDB.Ho_Ten, Lop.Ten_Lop, Lop.Ten_Mon_Hoc
        ORDER BY {order_column} DESC
        '''

        cursor.execute(query)

        # Lấy tất cả các hàng kết quả từ truy vấn
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ khỏi bảng trước khi thêm dữ liệu mới
        if rows:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            for row in rows:
                self.InforStudent_table.insert("", END, values=row)

        # Đóng kết nối sau khi lấy dữ liệu
        conn.close()





    def Canh_Cao(self):
        self.root.withdraw()  # Ẩn cửa sổ chính
        root_gmail = Toplevel(self.root)  # Tạo một cửa sổ mới
        Send_Gmail(root_gmail)  # Khởi tạo lớp Phan_Loai với cửa sổ mới
        root_gmail.protocol("WM_DELETE_WINDOW", self.on_closing)  # Đặt hàm đóng khi cửa sổ bị đóng
        root_gmail.mainloop()

    def on_closing(self):
        self.root.deiconify()  # Hiện lại cửa sổ chính khi cửa sổ Phan_Loai bị đóng

if __name__ == "__main__":
    root = Tk()
    obj = Phan_Loai(root)
    root.mainloop()