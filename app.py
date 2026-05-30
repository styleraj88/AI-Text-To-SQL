from flask import Flask,render_template,request,send_file,redirect
from flask_login import (
LoginManager,
UserMixin,
login_user,
logout_user,
login_required,
current_user
)
import time
import mysql.connector
import requests
from deep_translator import GoogleTranslator
from langdetect import detect

from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
Table,
TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = Flask(__name__)
app = Flask(__name__)

app.secret_key = "mysecretkey123"
ADMIN_PASSWORD="admin123"

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"
# DASHBOARD STATS

total_queries = 0
success_queries = 0
failed_queries = 0
most_used_db = "None"

last_question=""
last_sql=""
last_explanation=""
last_result=[]
last_headers=[]

all_databases = []
database_tables = {}
all_tables = []
translator = GoogleTranslator(source='auto', target='en')
class User(UserMixin):

    def __init__(
        self,
        id,
        username,
        password,
        email
    ):

        self.id=id

        self.username=username

        self.password=password

        self.email=email
@login_manager.user_loader
def load_user(user_id):

    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naveen@6302",
        database="login_system"
    )

    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )

    user=cursor.fetchone()

    conn.close()

    if user:

        return User(
            user[0],
            user[3],
            user[4],
            user[2]
        )

    return None        

# MYSQL CONNECTION
@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]

        password=request.form["password"]

        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naveen@6302",
            database="login_system"
        )

        cursor=conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=%s
            AND password=%s
            """,
            (username,password)
        )

        user=cursor.fetchone()

        conn.close()

        if user:

            user_obj=User(
                user[0],
                user[3],
                user[4],
                user[2]
            )

            login_user(user_obj)

            return redirect("/")

    return render_template("login.html")
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")
@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        name=request.form["name"]

        email=request.form["email"]

        username=request.form["username"]

        password=request.form["password"]

        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naveen@6302",
            database="login_system"
        )

        cursor=conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        existing_user=cursor.fetchone()
        if existing_user:

            conn.close()

            return "Username already exists!"

        cursor.execute(
            """
            INSERT INTO users
            (name,email,username,password)
            VALUES (%s,%s,%s,%s)
            """,
            (name,email,username,password)
        )

        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("register.html")
@app.route(
    "/forgot_password",
    methods=["GET","POST"]
)
def forgot_password():

    if request.method=="POST":

        username=request.form["username"]

        new_password=request.form["password"]

        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naveen@6302",
            database="login_system"
        )

        cursor=conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=%s
            """,
            (username,)
        )

        user=cursor.fetchone()

        if user:

            cursor.execute(
                """
                UPDATE users
                SET password=%s
                WHERE username=%s
                """,
                (
                    new_password,
                    username
                )
            )

            conn.commit()

            conn.close()

            return redirect("/login")

        conn.close()

        return "Username not found!"

    return render_template(
        "forgot_password.html"
    )
# LANGUAGE FUNCTION
def convert_to_english(question):

    try:

        lang = detect(question)

        print("Detected Language:", lang)

        if lang != "en":

            translated = GoogleTranslator(
                source='auto',
                target='en'
            ).translate(question)

            print("Translated:", translated)

            return translated

        return question

    except Exception as e:

        print("Translation Error:", e)

        return question

# DANGEROUS SQL DETECTOR

def is_dangerous_query(sql):

    dangerous_words=[

        "DROP",

        "DELETE",

        "ALTER",

        "TRUNCATE"

    ]

    sql=sql.upper()

    for word in dangerous_words:

        if word in sql:

            return True

    return False
# QUERY LOG FUNCTION

def save_query_log(

    username,

    question,

    generated_sql,

    status

):

    conn=mysql.connector.connect(

        host="localhost",

        user="root",

        password="Naveen@6302",

        database="login_system"

    )

    cursor=conn.cursor()

    cursor.execute(

        """
        INSERT INTO query_logs

        (

            username,

            question,

            generated_sql,

            status

        )

        VALUES

        (%s,%s,%s,%s)
        """,

        (

            username,

            question,

            generated_sql,

            status

        )

    )

    conn.commit()

    conn.close()
# AI SQL FUNCTION
def generate_sql(question, cursor):

    # GET ALL TABLES
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    schema_text = ""

    for table in tables:

        table_name = table[0]

        cursor.execute(f"DESCRIBE {table_name}")

        columns = cursor.fetchall()

        schema_text += f"\nTable: {table_name}\n"

        for col in columns:

            schema_text += f"- {col[0]} ({col[1]})\n"

    prompt = f"""
You are an expert MySQL SQL generator.

Database Schema:

{schema_text}

Rules:

1 Return ONLY SQL.
2 No explanation.
3 Use ONLY available tables.
4 Use correct columns.
5 Generate valid MySQL query.

Question:
{question}
"""

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model":"llama3",
            "prompt":prompt,
            "stream":False

        }

    )

    sql=response.json()["response"]

    sql=sql.replace("```sql","")
    sql=sql.replace("```","")
    sql=sql.strip()

    return sql
def explain_sql(sql_query):

    prompt = f"""
Explain this SQL query in simple English.

SQL:
{sql_query}

Keep explanation short and easy.
"""

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model":"llama3",

            "prompt":prompt,

            "stream":False

        }

    )

    return response.json()["response"]


@app.route("/",methods=["GET","POST"])
@login_required
def home():
    global total_queries
    global success_queries
    global failed_queries
    global most_used_db

    global last_question
    global last_sql
    global last_explanation
    global last_result
    global last_headers

    result=[]
    sql_query=""
    headers=[]

    query_logs=[]
    
    explanation=""
    execution_time=""
    db_name=""
    database_tables={}
    all_databases=[]
    all_tables=[]
    conn2 = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naveen@6302"
    )

    cursor2 = conn2.cursor()

    cursor2.execute("SHOW DATABASES")

    all_databases = [db[0] for db in cursor2.fetchall()]
    for db in all_databases:

        try:

            temp_conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password="Naveen@6302",
                database=db
            )

            temp_cursor=temp_conn.cursor()

            temp_cursor.execute(
                "SHOW TABLES"
            )

            tables=[
                table[0]
                for table in temp_cursor.fetchall()
            ]

            database_tables[db]=tables

            temp_cursor.close()
            temp_conn.close()

        except Exception as e:

            print("Database Error:",e)

            database_tables[db]=[]

             

    cursor2.close()
    conn2.close()
    # LOAD QUERY LOGS

    log_conn=mysql.connector.connect(

        host="localhost",

        user="root",

        password="Naveen@6302",

        database="login_system"

    )

    log_cursor=log_conn.cursor()

    log_cursor.execute(

        """
        SELECT

        username,

        question,

        status,

        created_at

        FROM query_logs

        ORDER BY id DESC

        LIMIT 10
        """
    )

    query_logs=log_cursor.fetchall()

    log_conn.close()
    if request.method=="POST":
        total_queries += 1
        start_time = time.time()
        db_name=request.form["database"]
        admin_password=request.form.get(
            "admin_password",
            ""
        )
        # GET TABLES FROM SELECTED DATABASE

        conn_tables=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naveen@6302",
            database=db_name
        )

        cursor_tables=conn_tables.cursor()

        cursor_tables.execute("SHOW TABLES")

        all_tables=[table[0] for table in cursor_tables.fetchall()]

        cursor_tables.close()
        conn_tables.close()
        most_used_db = db_name
         
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naveen@6302",
            database=db_name
        )

        cursor = conn.cursor()

        user_question=request.form["question"]
        last_question=user_question

        english_question=convert_to_english(
            user_question
        )

        sql_query=generate_sql(
            english_question,
            cursor
        )
        last_sql=sql_query
        if is_dangerous_query(sql_query):

            if admin_password != ADMIN_PASSWORD:
                save_query_log(

                    current_user.username,

                    user_question,

                    sql_query,

                    "BLOCKED"

                )

                result=[

                    ["⚠️ Dangerous Query Detected"],

                    ["❌ Wrong Admin Password"]

                ]

                headers=["SECURITY"]

                return render_template(

                    "index.html",

                    result=result,

                    sql=sql_query,

                    headers=headers,

                    db_name=db_name,

                    total_rows=len(result),

                    status="ADMIN VERIFICATION",

                    total_queries=total_queries,

                    success_queries=success_queries,

                    failed_queries=failed_queries,

                    most_used_db=most_used_db,

                    all_databases=all_databases,

                    database_tables=database_tables,

                    all_tables=all_tables,

                    explanation=
                    "Dangerous SQL detected. Enter Admin Password.",

                    execution_time=execution_time,
                    query_logs=query_logs,

                    show_admin_popup=True

                )


        explanation = explain_sql(
        sql_query
        )
        last_explanation=explanation
        try:

            cursor.execute(sql_query)
            success_queries += 1
            save_query_log(

                current_user.username,

                user_question,

                sql_query,

                "SUCCESS"

            )

            result = cursor.fetchall()

            headers=[]

            if cursor.description:

                headers=[i[0] for i in cursor.description]

            else:

                headers=[]

            last_headers=headers
            last_result=result

        except Exception as e:
            failed_queries += 1
            save_query_log(

                current_user.username,

                user_question,

                sql_query,

                "FAILED"

            )

            result=[[f"Error: {str(e)}"]]
        execution_time = round(
            time.time() - start_time,
            3
    )    
        cursor.close()
        conn.close()
    return render_template(
        "index.html",
        result=result,
        sql=sql_query,
        headers=headers,
        db_name=db_name,
        total_rows=len(result),
        status="Connected",
        total_queries=total_queries,
        success_queries=success_queries,
        failed_queries=failed_queries,
        most_used_db=most_used_db,
        all_databases=all_databases,
        database_tables=database_tables,
        all_tables=all_tables,

        explanation=explanation,
        execution_time=execution_time
        
    )    

@app.route("/download_pdf")
def download_pdf():

    pdf = SimpleDocTemplate("report.pdf")

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI TEXT TO SQL PREMIUM REPORT",
            styles['Heading1']
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            f"<b>Database:</b> {most_used_db}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"<b>User Question:</b> {last_question}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"<b>Generated SQL:</b> {last_sql}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"<b>Explanation:</b> {last_explanation}",
            styles['Normal']
        )
    )

    content.append(
        Spacer(1,20)
    )

    if last_headers:

        data=[last_headers]

        for row in last_result:

            data.append(
                [str(x) for x in row]
            )

        table=Table(data)

        table.setStyle(

            TableStyle([

                ('BACKGROUND',(0,0),(-1,0),colors.blue),

                ('TEXTCOLOR',(0,0),(-1,0),colors.white),

                ('GRID',(0,0),(-1,-1),1,colors.black),

                ('BACKGROUND',(0,1),(-1,-1),colors.lightgrey)

            ])

        )

        content.append(table)

    pdf.build(content)

    return send_file(
        "report.pdf",
        as_attachment=True
    )
if __name__=="__main__":
    app.run(debug=True)
     