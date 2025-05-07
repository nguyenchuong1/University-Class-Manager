from GUI import TrangChu
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.root.geometry("400x200")

        label_title = Label(self.root, text="Đăng nhập", bg="powder blue", fg="green", bd=10,
                            relief=RIDGE, font=("time new roman", 30, "bold"), padx=2, pady=1)
        label_title.pack(side=TOP, fill=X)

        Dataframe = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe.place(x=0, y=70, width=400, height=200)

        lb_user = Label(Dataframe, font=("arial", 12, "bold"), text="User:", padx=2)
        lb_user.grid(row=1, column=0, sticky=W)
        self.txt_user = Entry(Dataframe, font=("arial", 13, "bold"), width=25)
        self.txt_user.grid(row=1, column=1)

        lb_password = Label(Dataframe, font=("arial", 12, "bold"), text="Password:", padx=2)
        lb_password.grid(row=2, column=0, sticky=W)
        self.txt_pw = Entry(Dataframe, font=("arial", 13, "bold"), width=25, show="*")
        self.txt_pw.grid(row=2, column=1)

        btn_add = Button(Dataframe, text="Đăng nhập", bg="green", fg="white", font=("arial", 10, "bold"), width=15,
                         height=1, padx=1, pady=1, command=self.check_login)
        btn_add.grid(row=3, column=1)

    def check_login(self):
        conn = sqlite3.connect('userDB.db')
        cursor = conn.cursor()
        username = self.txt_user.get()
        password = self.txt_pw.get()

        cursor.execute("SELECT position FROM user WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            if result[0] == 'admin':
                messagebox.showinfo("Success", "Đăng nhập thành công!")
                self.root.destroy()  # Đóng cửa sổ đăng nhập
                self.open_trang_chu()  # Mở trang hiển thị thông tin
            else:
                messagebox.showwarning("Error", "Bạn không có quyền truy cập!")
        else:
            messagebox.showerror("Error", "Tài khoản hoặc mật khẩu không đúng!")

    def open_trang_chu(self):
        root_trang_chu = Tk()
        TrangChu(root_trang_chu)
        root_trang_chu.mainloop()





if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
