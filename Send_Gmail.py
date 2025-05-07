import sqlite3
from email.mime.application import MIMEApplication

import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
class Send_Gmail:
    def __init__(self, root):
        self.root = root
        self.root.title("Bảng Cảnh cáo")
        self.root.geometry("1550x800")

        self.Mssv = StringVar()  # Gán mã sinh viên
        self.HoTen = StringVar()
        self.Ma_Lop = StringVar() #Gán mã lớp
        self.Lop = StringVar()
        self.TenMonHoc = StringVar()
        self.Dot = StringVar()
        self.Vang_P = StringVar()
        self.Vang_K = StringVar()
        self.Tong_t = StringVar()
        self.Phan_tram_vang = StringVar()

        self.So_Ngay_Vang = StringVar()


        # ======================= First Frame  ===============================
        Dataframe_top = Frame(self.root, bd=5, relief=RIDGE)
        Dataframe_top.place(x=0, y=0, width=1530, height=50)


        btn_Vang20 = Button(Dataframe_top, text="Hiển thị vắng(20-49%) ", bg="green", fg="white", font=("arial", 13, "bold"),
                             width=20,
                             height=1, padx=1, pady=1,command=self.show_20)  # command=self.load_excel_file)
        btn_Vang20.grid(row=0, column=0)

        btn_Vang50 = Button(Dataframe_top, text="Hiển thị vắng(>=50%) ", bg="green", fg="white",
                             font=("arial", 13, "bold"),
                             width=20,
                             height=1, padx=1, pady=1,command=self.show_50)  # command=self.load_excel_file)
        btn_Vang50.grid(row=0, column=1)
        btn_send_mail = Button(Dataframe_top, text="Gửi email", bg="green", fg="white",
                            font=("arial", 13, "bold"),
                            width=20,
                            height=1, padx=1, pady=1, command=self.send_gmail)  # command=self.load_excel_file)
        btn_send_mail.grid(row=0, column=2)
        btn_file_vang_nhieu = Button(Dataframe_top, text="Gửi File vắng", bg="green", fg="white",
                               font=("arial", 13, "bold"),
                               width=20,
                               height=1, padx=1, pady=1, command=self.select_excel_file)  # command=self.load_excel_file)
        btn_file_vang_nhieu.grid(row=0, column=3)

        # ================= table view =======
        Dataframe_view = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_view.place(x=0, y=50, width=1530, height=500)

        # ========================================Scrollbar =======================================
        scroll_x = ttk.Scrollbar(Dataframe_view, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Dataframe_view, orient=VERTICAL)
        self.InforStudent_table = ttk.Treeview(Dataframe_view,
                                               column=("MSSV",  "Ho_Ten","Ma_Lop","Lop", "Ten_Mon_Hoc","Dot","Vang_P","Vang_K","Tong_T","Phan_Tram_Vang"),
                                               xscrollcommand=scroll_x.set,
                                               yscrollcommand=scroll_y.set)
        # Cấu hình các thanh cuộn ngang và dọc
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.InforStudent_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.InforStudent_table.xview)
        scroll_y.config(command=self.InforStudent_table.yview)

        # Thiết lập tiêu đề cột cho bảng
        self.InforStudent_table.heading("MSSV", text="Mã sinh viên")
        self.InforStudent_table.heading("Ho_Ten", text="Họ và tên")
        self.InforStudent_table.heading("Ma_Lop", text="Mã lớp")
        self.InforStudent_table.heading("Lop", text="Lớp")
        self.InforStudent_table.heading("Ten_Mon_Hoc", text="Tên môn học")
        self.InforStudent_table.heading("Dot", text="Đợt")
        self.InforStudent_table.heading("Vang_P", text="Vắng có phép")
        self.InforStudent_table.heading("Vang_K", text="Vắng không phép")
        self.InforStudent_table.heading("Tong_T", text="Tổng tiết vắng")

        self.InforStudent_table.heading("Phan_Tram_Vang", text="Phần trăm vắng")

        # Chỉ hiển thị phần tiêu đề
        self.InforStudent_table["show"] = "headings"

        # Đặt độ rộng cho từng cột
        self.InforStudent_table.column("MSSV", width=50)
        self.InforStudent_table.column("Ho_Ten", width=50)
        self.InforStudent_table.column("Ma_Lop", width=50)
        self.InforStudent_table.column("Lop", width=50)
        self.InforStudent_table.column("Ten_Mon_Hoc", width=50)
        self.InforStudent_table.column("Dot", width=50)
        self.InforStudent_table.column("Vang_P", width=50)
        self.InforStudent_table.column("Vang_K", width=50)
        self.InforStudent_table.column("Tong_T", width=50)

        self.InforStudent_table.column("Phan_Tram_Vang", width=50)

        # Hiển thị bảng trong khung
        self.InforStudent_table.pack(fill=BOTH, expand=1)
        self.fetch_data()
        self.InforStudent_table.bind("<ButtonRelease-1>", self.get_cursor)

        #======================= dataframe check
        Dataframe_check = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe_check.place(x=0, y=600, width=1530, height=500)
        lb_Dot = Label(Dataframe_check, font=("arial", 12, "bold"), text="Mã sinh viên:", padx=2)
        lb_Dot.grid(row=0, column=0, sticky=W)
        self.txt_Dot = Entry(Dataframe_check, textvariable=self.Mssv, font=("arial", 13, "bold"), width=25)
        self.txt_Dot.grid(row=0, column=1)

        lb_MaLop = Label(Dataframe_check, font=("arial", 12, "bold"), text="Số ngày vắng:", padx=2, pady=4)
        lb_MaLop.grid(row=1, column=0, sticky=W)
        self.txt_MaLop = Entry(Dataframe_check, textvariable=self.So_Ngay_Vang, font=("arial", 13, "bold"), width=25)
        self.txt_MaLop.grid(row=1, column=1)




    def fetch_data(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT
    Tong_Cong.student_id,
    StudentDB.Ho_Ten,
    Lop.Ma_Lop, 
    Lop.Ten_Lop, 
    Lop.Ten_Mon_Hoc, 
    Lop.Dot,
    Tong_Cong.Vang_P, 
    Tong_Cong.Vang_K, 
    Tong_Cong.Tong_T,
    Tong_Cong.Vang_Phan_Tram
FROM 
    StudentDB
JOIN 
    DiemDanh ON StudentDB.MSSV = DiemDanh.student_id
JOIN 
    Lop ON Lop.Ma_Lop = DiemDanh.Ma_Lop 
JOIN 
    Tong_Cong ON Tong_Cong.student_id = StudentDB.MSSV AND Tong_Cong.Ma_Lop = Lop.Ma_Lop AND Tong_Cong.Vang_Phan_Tram >0

                ''')
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            self.data_list = []  # Khởi tạo danh sách để lưu trữ dữ liệu
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
                self.data_list.append(i)  # Thêm từng hàng vào danh sách
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
                COUNT(*)
            FROM 
                DiemDanh
            WHERE 
                student_id = ? AND Ma_Lop = ? AND (P_K = 'K' OR P_K = 'P')
        """, (self.Mssv.get(),self.Ma_Lop.get()))

        # Lấy hàng đầu tiên từ kết quả
        data = cursor.fetchone()

        # Đóng kết nối sau khi lấy dữ liệu
        cursor.close()
        connection.close()

        # Cập nhật giá trị cho self.So_Ngay_Vang
        self.So_Ngay_Vang.set(data[0] if data else 0)

    def get_cursor(self, event=""):
        cursor_row = self.InforStudent_table.focus()
        if cursor_row:  # Kiểm tra xem có hàng nào được chọn không
            content = self.InforStudent_table.item(cursor_row)
            row = content["values"]

            # Lấy chỉ số của hàng được chọn
            index = self.InforStudent_table.index(cursor_row)
            selected_data = self.data_list[index]  # Lấy dữ liệu từ danh sách
            # messagebox.showinfo("Thông tin dong_2", f"dong_2: {selected_data[1]}, Type: {type(selected_data[1])}")

            # Gán giá trị vào Entry, giữ nguyên định dạng của Ma_Lop
            self.Mssv.set(selected_data[0])
            self.HoTen.set(selected_data[1])
            self.Ma_Lop.set(str(selected_data[2]))  # Đảm bảo giữ nguyên chuỗi
            self.Lop.set(selected_data[3])
            self.TenMonHoc.set(selected_data[4])
            self.Dot.set(selected_data[5])
            self.Vang_P.set(selected_data[6])
            self.Vang_K.set(selected_data[7])
            self.Tong_t.set(selected_data[8])
            self.Phan_tram_vang.set(selected_data[9])
            self.get_student_data()
        else:
            # Nếu không có hàng nào được chọn, bạn có thể đặt các trường về giá trị mặc định
            self.clear_entry()

    def show_20(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT
            Tong_Cong.student_id,
            StudentDB.Ho_Ten,
            Lop.Ma_Lop, 
            Lop.Ten_Lop, 
            Lop.Ten_Mon_Hoc, 
            Lop.Dot,
            Tong_Cong.Vang_P, 
            Tong_Cong.Vang_K, 
            Tong_Cong.Tong_T,
            Tong_Cong.Vang_Phan_Tram
        FROM 
            StudentDB
        JOIN 
            DiemDanh ON StudentDB.MSSV = DiemDanh.student_id
        JOIN 
            Lop ON Lop.Ma_Lop = DiemDanh.Ma_Lop 
        JOIN 
            Tong_Cong ON Tong_Cong.student_id = StudentDB.MSSV AND Tong_Cong.Ma_Lop = Lop.Ma_Lop AND
             Tong_Cong.Vang_Phan_Tram BETWEEN 20 AND 49

                        ''')
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            self.data_list = []  # Khởi tạo danh sách để lưu trữ dữ liệu
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
                self.data_list.append(i)  # Thêm từng hàng vào danh sách
            conn.commit()
        conn.close()
    def show_50(self):
        conn = sqlite3.connect(r'test_du_lieu_chay_thu.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT
            Tong_Cong.student_id,
            StudentDB.Ho_Ten,
            Lop.Ma_Lop, 
            Lop.Ten_Lop, 
            Lop.Ten_Mon_Hoc, 
            Lop.Dot,
            Tong_Cong.Vang_P, 
            Tong_Cong.Vang_K, 
            Tong_Cong.Tong_T,
            Tong_Cong.Vang_Phan_Tram
        FROM 
            StudentDB
        JOIN 
            DiemDanh ON StudentDB.MSSV = DiemDanh.student_id
        JOIN 
            Lop ON Lop.Ma_Lop = DiemDanh.Ma_Lop 
        JOIN 
            Tong_Cong ON Tong_Cong.student_id = StudentDB.MSSV AND Tong_Cong.Ma_Lop = Lop.Ma_Lop AND Tong_Cong.Vang_Phan_Tram >=50

                        ''')
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.InforStudent_table.delete(*self.InforStudent_table.get_children())
            self.data_list = []  # Khởi tạo danh sách để lưu trữ dữ liệu
            for i in rows:
                self.InforStudent_table.insert("", END, values=i)
                self.data_list.append(i)  # Thêm từng hàng vào danh sách
            conn.commit()
        conn.close()



    def send_gmail(self):
        # Kết nối đến cơ sở dữ liệu
        if self.Mssv.get() == "" and self.Ma_Lop.get() == "":
            messagebox.showwarning("Lỗi", "Vui lòng chọn Sinh viên trong bảng.")
            return

        conn = sqlite3.connect('test_du_lieu_chay_thu.db')
        cursor = conn.cursor()

        # Truy vấn để lấy %_Vang của sinh viên dựa vào MSSV và Ma_Lop
        cursor.execute("""
                    SELECT Vang_Phan_Tram FROM Tong_Cong 
                    WHERE  Tong_Cong.student_id = ? AND Tong_Cong.Ma_Lop = ?
                """, (self.Mssv.get(), self.Ma_Lop.get()))

        result = cursor.fetchone()

        # Kiểm tra kết quả và thực hiện hành động
        if result:
            vang_phan_tram = result[0]

            # Thay thế dấu phẩy bằng dấu chấm trước khi chuyển đổi sang float
            if isinstance(vang_phan_tram, str):
                vang_phan_tram = vang_phan_tram.replace(',', '.')

            # Chuyển đổi vang_phan_tram sang kiểu float
            try:
                vang_phan_tram_float = float(vang_phan_tram)
            except ValueError:
                messagebox.showwarning("Lỗi", f"Giá trị vắng mặt không hợp lệ: {vang_phan_tram}")
                return
            # bắt đầu phân loại gửi mail
            if vang_phan_tram_float >= 20.0 and vang_phan_tram_float < 50:
                sender_email = 'nguyenchuong010866az@gmail.com'
                password = 'dxtp joup rxfu xtan'  # Mật khẩu ứng dụng
                receiver_email = 'nguyenchuong891569@gmail.com'
                subject = f'Cảnh Cáo học vụ - Sinh Viên {self.HoTen.get()} - Mã Lớp {self.Ma_Lop.get()} ,  vắng >= 20% thời lượng học  '
                body = f"""
                Kính gửi em {self.HoTen.get()} (MSSV: {self.Mssv.get()}),

                Chúng tôi xin thông báo về tình trạng học tập của bạn trong môn học {self.TenMonHoc.get()} thuộc lớp {self.Lop.get()}. Dựa vào số liệu điểm danh và kết quả học tập, phòng Công tác Sinh viên nhận thấy rằng tỷ lệ vắng mặt của bạn đã vượt quá mức cho phép. Thông tin chi tiết như sau:

                - Mã lớp: {self.Ma_Lop.get()}
                - Tên lớp: {self.Lop.get()}
                - Tên môn học: {self.TenMonHoc.get()}
                - Đợt học: {self.Dot.get()}
                - Số tiết vắng có phép: {self.Vang_P.get()} tiết
                - Số tiết vắng không phép: {self.Vang_K.get()} tiết
                - Tổng số tiết: {self.Tong_t.get()} tiết
                - Số ngày vắng: {self.So_Ngay_Vang.get()}
                - Tỷ lệ vắng mặt: {self.Phan_tram_vang.get()}%

                Với tỷ lệ vắng mặt {self.Phan_tram_vang.get()}%, bạn đã vi phạm quy định của nhà trường. Nếu không có sự thay đổi tích cực trong việc duy trì sự có mặt và hoàn thành học phần, bạn sẽ có nguy cơ đối mặt buộc thôi học 1 tháng.

                Vui lòng liên hệ với phòng Công tác Sinh viên để được tư vấn và tìm cách khắc phục. Chúng tôi mong rằng bạn sẽ có những nỗ lực cần thiết để duy trì tình trạng học tập của mình.

                Trân trọng,

                Phòng Công tác Sinh viên. """
                # Tạo email
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = receiver_email
                message['Subject'] = subject

                # Thêm nội dung văn bản vào email
                message.attach(MIMEText(body, 'plain'))

                # Gửi email qua SMTP
                try:
                    # Kết nối đến server SMTP của Gmail
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, password)

                    # Gửi email
                    server.sendmail(sender_email, receiver_email, message.as_string())
                    print("Email sent successfully!")
                    server.quit()
                except Exception as e:
                    print(f"Error: {e}")

                messagebox.showwarning("Thông báo",
                                       f"[THÔNG TIN] Sinh viên MSSV {self.Mssv.get()} vắng mặt {vang_phan_tram_float}%, đã gửi mail.")
                return

            elif vang_phan_tram_float>=50:
                sender_email = 'nguyenchuong010866az@gmail.com'
                password = 'dxtp joup rxfu xtan'  # Mật khẩu ứng dụng
                receiver_email = 'nguyenchuong891569@gmail.com'  #kensava3005@gmail.com
                receiver_email_parent = 'nguyenchuong891569@gmail.com'
                receiver_email_teacher = 'nguyenchuong891569@gmail.com'
                receiver_email_department_head = 'nguyenchuong891569@gmail.com'
                #Thằng sinh viên
                subject_sv = f'Cảnh Cáo học vụ - Sinh Viên {self.HoTen.get()} - Mã Lớp {self.Ma_Lop.get()} ,  vắng >= 50% thời lượng học  '
                body_sinhvien = f"""
                                Kính gửi em {self.HoTen.get()} (MSSV: {self.Mssv.get()}),

                                Chúng tôi xin thông báo về tình trạng học tập của bạn trong môn học {self.TenMonHoc.get()} thuộc lớp {self.Lop.get()}. Dựa vào số liệu điểm danh và kết quả học tập, phòng Công tác Sinh viên nhận thấy rằng tỷ lệ vắng mặt của bạn đã vượt quá mức cho phép. Thông tin chi tiết như sau:

                                - Mã lớp: {self.Ma_Lop.get()}
                                - Tên lớp: {self.Lop.get()}
                                - Tên môn học: {self.TenMonHoc.get()}
                                - Đợt học: {self.Dot.get()}
                                - Số tiết vắng có phép: {self.Vang_P.get()} tiết
                                - Số tiết vắng không phép: {self.Vang_K.get()} tiết
                                - Tổng số tiết: {self.Tong_t.get()} tiết
                                - Số ngày vắng: {self.So_Ngay_Vang.get()}
                                - Tỷ lệ vắng mặt: {self.Phan_tram_vang.get()}%

                                Với tỷ lệ vắng mặt {self.Phan_tram_vang.get()}%, bạn đã vi phạm quy định của nhà trường . Bạn bị cấm thi môn học {self.TenMonHoc.get()}.

                                Vui lòng liên hệ với phòng Công tác Sinh viên để được tư vấn . Chúng tôi mong rằng bạn sẽ có những nỗ lực cần thiết để duy trì tình trạng học tập của mình vào kì tới.

                                Trân trọng,

                                Phòng Công tác Sinh viên. """
                # Tạo email
                message_sv = MIMEMultipart()
                message_sv['From'] = sender_email
                message_sv['To'] = receiver_email
                message_sv['Subject'] = subject_sv
                # Thêm nội dung văn bản vào email
                message_sv.attach(MIMEText(body_sinhvien, 'plain'))

                # Phụ huynh
                subject_parent = f'Cảnh báo học vụ về tình hình Sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}) - Vắng học > 50%'
                body_parent = f"""
                Kính gửi quý phụ huynh của sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}),

                Chúng tôi là Phòng Công tác Sinh viên, xin được thông báo về tình trạng học tập của con quý vị trong môn {self.TenMonHoc.get()} thuộc lớp {self.Lop.get()}. Theo thống kê, con quý vị đã nghỉ học với số buổi vượt mức quy định của nhà trường. Chi tiết như sau:

                - Mã lớp: {self.Ma_Lop.get()}
                - Tên lớp: {self.Lop.get()}
                - Tên môn học: {self.TenMonHoc.get()}
                - Đợt học: {self.Dot.get()}
                - Số tiết vắng có phép: {self.Vang_P.get()} tiết
                - Số tiết vắng không phép: {self.Vang_K.get()} tiết
                - Tổng số tiết: {self.Tong_t.get()} tiết
                - Số ngày vắng: {self.So_Ngay_Vang.get()}
                - Tỷ lệ vắng mặt: {self.Phan_tram_vang.get()}%                

                Với tỷ lệ vắng trên 50%, con quý vị bị đinh chỉ thi. Quý phụ huynh vui lòng liên hệ với chúng tôi hoặc với giáo viên chủ nhiệm để được tư vấn thêm và cùng hỗ trợ con quý vị cải thiện tình hình học tập.

                Trân trọng,

                Phòng Công tác Sinh viên.
                """
                message_parent = MIMEMultipart()
                message_parent['From'] = sender_email
                message_parent['To'] = receiver_email_parent
                message_parent['Subject'] = subject_parent
                # Thêm nội dung văn bản vào email
                message_parent.attach(MIMEText(body_parent, 'plain'))


                #Giáo viên chủ nhiệm
                subject_teacher = f'Cảnh báo học vụ - Sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}) - Vắng học > 50% của lớp {self.Lop.get()}'
                body_teacher = f"""
                Kính gửi thầy/cô (Giáo viên chủ nhiệm lớp {self.Lop.get()}),

                Chúng tôi xin thông báo về tình trạng học tập của sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}) trong môn {self.TenMonHoc.get()} thuộc lớp {self.Lop.get()}. Dựa vào số liệu điểm danh và kết quả học tập, phòng Công tác Sinh viên nhận thấy rằng tỷ lệ vắng mặt của sinh viên đã vượt quá mức cho phép. Thông tin chi tiết như sau:

                - Mã lớp: {self.Ma_Lop.get()}
                - Tên lớp: {self.Lop.get()}
                - Tên môn học: {self.TenMonHoc.get()}
                - Đợt học: {self.Dot.get()}
                - Số ngày vắng: {self.Vang_P.get()} ngày
                - Số ngày có mặt: {self.Vang_K.get()} ngày
                - Tổng số ngày: {self.Tong_t.get()} ngày
                - Tỷ lệ vắng mặt: {self.Phan_tram_vang.get()}%

                Chúng tôi hy vọng quý thầy cô sẽ hỗ trợ sinh viên cải thiện tình trạng học tập của mình.

                Trân trọng,

                Phòng Công tác Sinh viên.
                """
                message_teacher = MIMEMultipart()
                message_teacher['From'] = sender_email
                message_teacher['To'] = receiver_email_teacher
                message_teacher['Subject'] = subject_teacher
                message_teacher.attach(MIMEText(body_teacher, 'plain'))


                #Trưởng bộ môn
                subject_department_head = f'Tình trạng học tập - Sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}) - Vắng học > 50%'
                body_department_head = f"""
                Kính gửi Trưởng bộ môn,

                Chúng tôi xin thông báo về tình trạng học tập của sinh viên {self.HoTen.get()} (MSSV: {self.Mssv.get()}) trong môn {self.TenMonHoc.get()} thuộc lớp {self.Lop.get()}. Theo dữ liệu điểm danh, sinh viên đã vắng mặt với tỷ lệ vượt mức cho phép. Chi tiết như sau:

                - Mã lớp: {self.Ma_Lop.get()}
                - Tên lớp: {self.Lop.get()}
                - Tên môn học: {self.TenMonHoc.get()}
                - Đợt học: {self.Dot.get()}
                - Số ngày vắng: {self.Vang_P.get()} ngày
                - Số ngày có mặt: {self.Vang_K.get()} ngày
                - Tổng số ngày: {self.Tong_t.get()} ngày
                - Tỷ lệ vắng mặt: {self.Phan_tram_vang.get()}%

                Chúng tôi mong nhận được sự hỗ trợ từ bộ môn để có những giải pháp kịp thời cho sinh viên.

                Trân trọng,

                Phòng Công tác Sinh viên.
                """
                message_department_head = MIMEMultipart()
                message_department_head['From'] = sender_email
                message_department_head['To'] = receiver_email_department_head
                message_department_head['Subject'] = subject_department_head
                message_department_head.attach(MIMEText(body_department_head, 'plain'))
                # Gửi email qua SMTP
                try:
                    # Kết nối đến server SMTP của Gmail
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, password)

                    # Gửi email
                    server.sendmail(sender_email, receiver_email, message_sv.as_string())
                    server.sendmail(sender_email, receiver_email_parent, message_parent.as_string())
                    server.sendmail(sender_email, receiver_email_teacher, message_teacher.as_string())
                    server.sendmail(sender_email, receiver_email_department_head, message_department_head.as_string())
                    print("Email sent successfully!")
                    server.quit()
                except Exception as e:
                    print(f"Error: {e}")

                messagebox.showwarning("Thông báo",
                                       f"[THÔNG TIN] Sinh viên MSSV {self.Mssv.get()} vắng mặt {vang_phan_tram_float}%, đã gửi mail.")
                return


            else:
                messagebox.showwarning("Thông báo",
                                       f"[THÔNG BÁO] Sinh viên MSSV {self.Mssv.get()}: Chưa đủ điều kiện cảnh cáo học vụ.")
                return
        else:
            messagebox.showwarning("Lỗi", "Sinh viên này không có trong cơ sở dữ liệu.")
            return

        # Đóng kết nối
        conn.close()

    def generate_report(self):
        connection = sqlite3.connect("test_du_lieu_chay_thu.db")
        query = """
            SELECT DISTINCT
    Tong_Cong.student_id,
    StudentDB.Ho_Ten,
    Lop.Ma_Lop, 
    Lop.Ten_Lop, 
    Lop.Ten_Mon_Hoc, 
    Lop.Dot,
    Tong_Cong.Vang_P, 
    Tong_Cong.Vang_K, 
    Tong_Cong.Tong_T,
    Tong_Cong.Vang_Phan_Tram
FROM 
    StudentDB
JOIN 
    DiemDanh ON StudentDB.MSSV = DiemDanh.student_id
JOIN 
    Lop ON Lop.Ma_Lop = DiemDanh.Ma_Lop 
JOIN 
    Tong_Cong ON Tong_Cong.student_id = StudentDB.MSSV AND Tong_Cong.Ma_Lop = Lop.Ma_Lop AND Tong_Cong.Vang_Phan_Tram >=20
        """
        df = pd.read_sql_query(query, connection)
        file_name = f'Bao_Cao_Vang_Mat_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        df.to_excel(file_name, index=False)
        connection.close()
        return file_name

    def send_email_file(self, file_path):

        sender_email = "nguyenchuong010866az@gmail.com"
        receiver_emails = ["nguyenchuong891569@gmail.com", "chuongnguyen24102003@gmail.com"]
        subject = "Tổng hợp file  sinh viên vắng mặt nhiều của từng lớp"
        body = "Xin chào,\n\nDưới đây là báo cáo về sinh viên vắng mặt.\n\nTrân trọng!"

        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Đính kèm file Excel
        with open(file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=file_path)
        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
        msg.attach(part)

        # Gửi email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Cập nhật thông tin máy chủ SMTP
            server.starttls()
            server.login(sender_email, "dxtp joup rxfu xtan")  # Đăng nhập
            server.sendmail(sender_email, receiver_emails, msg.as_string())
    def select_excel_file(self):
        # Khởi tạo giao diện tkinter (ẩn cửa sổ chính)
        self.generate_report()
        root = Tk()
        root.withdraw()  # Ẩn cửa sổ tkinter

        # Hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            title="Chọn file Excel",
            filetypes=[("Excel files", "*.xlsx")]  # Chỉ file .xls
        )

        if file_path:  # Kiểm tra nếu file_path không rỗng
            # Gọi các hàm nhập dữ liệu và truyền file_path vào
           self.send_email_file(file_path)
           messagebox.showwarning("Thông báo",
                                   f"[THÔNG BÁO]  đã gửi mail file thành ông.")
if __name__ == "__main__":
    root = Tk()
    obj = Send_Gmail(root)
    root.mainloop()