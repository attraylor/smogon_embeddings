import os
dir = "tokenized_text"
concat_dir = "documents"
if not os.path.exists(concat_dir):
    os.makedirs(concat_dir)


def get_threadstring(s):
    try:
        reg_string = ".".join(s.split(".")[:-2])
        page_num = int(s.split(".")[-2][5:])
        next_page = reg_string + ".page-{}.txt".format(page_num + 1)
        return reg_string, page_num, next_page
    except IndexError:
        return "", 0, ""



list_of_files = os.listdir(dir)
threads = []
for f in list_of_files:
    if "page-1.txt" in f:
        title, page_num, next_page = get_threadstring(f)
        with open(os.path.join(concat_dir, title), "w+") as wf:
            with open(os.path.join(dir, f)) as rf:
                wf.write(rf.read())
                wf.write("\n")
                wf.flush()
            while next_page in list_of_files and not next_page == "":
                with open(os.path.join(dir, next_page)) as rf:
                    wf.write(rf.read())
                    wf.write("\n")
                    wf.flush()
                title, page_num, next_page = get_threadstring(next_page)
            wf.close()
