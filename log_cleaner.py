
import re
import random

def transform_logs(text:str)->str:
    lines=text.split('\n')

    email=re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
    timestamp=re.compile(r'\b(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})\b')

    months=["January","February","March","April","May","June","July",
            "August","September","October","November","December"]

    remarks=[
        "(as expected)",
        "(skill issue)",
        "(shocking, truly)",
        "(nobody could've predicted this)",
        "(classic)",
        "(it's always something)"
    ]

    def ordinal(n:int)->str:
        if 11<=n%100<=13:
            suf="th"
        else:
            suf={1:"st",2:"nd",3:"rd"}.get(n%10,"th")
        return f"{n}{suf}"

    def fmt_time(m):
        d,mo,y,h,mi=map(int,m.groups())
        period="AM" if h<12 else "PM"
        h=h%12 or 12
        return f"{ordinal(d)} {months[mo-1]} {y}, {h}:{mi:02d} {period}"

    def tag_err(m):
        return f"🛑ERROR🛑 {random.choice(remarks)}"

    err=warn=success=hidden=done=0
    out=[]

    for line in lines:
        if line.strip()=="":
            out.append(line)
            continue

        done+=1

        found=email.findall(line)
        hidden+=len(found)
        line=email.sub('[HIDDEN]',line)

        line=timestamp.sub(fmt_time,line)

        err+=len(re.findall(r'\bERROR\b',line))
        line=re.sub(r'\bERROR\b',tag_err,line)

        warn+=len(re.findall(r'\bWARNING\b',line))
        line=re.sub(r'\bWARNING\b','⚠️ WARNING',line)

        success+=len(re.findall(r'\bSUCCESS\b',line))
        line=re.sub(r'\bSUCCESS\b','✅ SUCCESS',line)

        success+=len(re.findall(r'\bOK\b',line))
        line=re.sub(r'\bOK\b','✅ OK',line)

        out.append(line)

    summary=f"Processed {done} lines, {err} errors, {warn} warnings, {success} successes, {hidden} emails hidden."

    out.append("")
    out.append(summary)

    return '\n'.join(out)

test_log = """User john@mail.com logged in at 23/08/2025 14:05.
ERROR: session timeout. ERROR: database unreachable.
WARNING: low disk space at 01/01/2026 09:30.

Login SUCCESS for jane@company.org.
Status check returned OK at 05/12/2025 23:59.
Contact admin@site.io or backup@site.io for help.
"""

print(transform_logs(test_log))

