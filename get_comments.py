import praw
import time
import os

# Given a comment, returns its root
def get_root(comment):
    while not comment.is_root:
        comment = comment.parent()
    return comment

# Gets all comments starting from root
def get_comments(root):
    string_out = ""

    spacing = "     "
    indent = "-----"
    string_out += root.body + "\n"
    comment_forest = root.replies.list()
    for comment in comment_forest:
        lines = comment.body.split("\n")
        string_out += indent * comment.depth + lines[0] + "\n"
        for line in lines[1:]:
            string_out += spacing * comment.depth + line + "\n"
    return string_out

# Gets comments from every root
def get_all_comments(root_comments):
    comments = ""
    while root_comments:
        comments += get_comments(root_comments.pop()) + "\n"
    return comments

def write_to_file(strings):
    with open(file_name, "a") as output:
        for s in strings:
            try:
                output.write(s)
            except:
                output.write("No new comments found")

# Get the root comments of the newest comments in a given submission
def get_root_comments(id_str):
    submission = reddit.submission(id=id_str)
    submission.comment_sort = 'new'
    root_comments = set()
    all_comments = submission.comments.list()
    # Gets roots of comments within the last 24 hours
    for comment in all_comments:
        if comment.created_utc < yesterday_utc:
            break
        root_comments.add(get_root(comment))
    return root_comments
        

current_time = time.time()
day_in_seconds = 86400
yesterday_utc = current_time - day_in_seconds

reddit = praw.Reddit(username = os.environ["username"],
                password = os.environ["password"],
                client_id = os.environ["client_id"],
                client_secret = os.environ["client_secret"],
                user_agent = "Comment Digest Bot 0.1")

submission_ids = [
    "corh54", 
    "corghm"
    ] # SPECIFY THREADS HERE

file_name = "comments.txt" # SPECIFY FILE NAME
if os.path.exists(file_name):
    os.remove(file_name)

for id_str in submission_ids:
    root_comments = get_root_comments(id_str)
    comments = get_all_comments(root_comments)
    write_to_file([reddit.submission(id=id_str).title + "\n", comments])
