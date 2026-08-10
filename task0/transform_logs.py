
import re
import random

def transform_logs(text:str)->str:
    lines=text.split('\n')

    email=re.compile(r'\w+@\w+\.\w+')
    timestamp = re.compile(
    r'\b(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})\b'
)

    months=["January","February","March","April","May","June",
            "July","August","September","October","November","December"]

    remarks=[
        "(as expected)",
        "(skill issue)",
        "(shocking, truly)",
        "(nobody could've predicted this)",
        "(classic)",
        "(as usual)"
    ]

    def fmt_time(m):
        d,mo,y,h,mi=map(int,m.groups())
        period="AM" if h<12 else "PM"
        h=h%12 or 12
        return f"{d} {months[mo-1]} {y}, {h}:{mi:02d} {period}"

    def tag_err(m):
        return f"🛑ERROR {random.choice(remarks)}"

    err=warn=success=hidden=done=0
    out=[]

    for line in lines:
        if line.strip()=="":
            out.append(line)
            continue

        done+=1

        found=email.findall(line)
        hidden+=len(found)
        line=email.sub("[HIDDEN]",line)

        line=timestamp.sub(fmt_time,line)

        err+=len(re.findall(r'\bERROR\b',line))
        line=re.sub(r'\bERROR\b',tag_err,line)

        warn+=len(re.findall(r'\bWARNING\b',line))
        success+=len(re.findall(r'\bSUCCESS\b',line))
        success+=len(re.findall(r'\bOK\b',line))

        out.append(line)

    summary=f"Processed {done} lines, {err} errors, {warn} warnings, {success} successes, {hidden} emails hidden."

    out.append("")
    out.append(summary)

    return '\n'.join(out)


test_log="""System startup completed at 01/01/2026 00:05.
User john.doe@example.com logged in at 01/01/2026 09:30.
WARNING: High memory usage detected at 01/01/2026 11:45.
Database connection SUCCESS at 01/01/2026 12:15.
Status check returned OK at 01/01/2026 14:20.
ERROR: Failed to connect to database.
ERROR: Authentication service unavailable.
Contact admin@company.com for assistance.

Backup SUCCESS at 02/01/2026 23:59.
WARNING: Disk space below 20 percent.
User alice@test.org logged out at 03/01/2026 08:10."""

print(transform_logs(test_log))
