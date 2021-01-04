import praw
import datetime
import random

REPLY_MESSAGES = ["Happy cake day /u/{}! 🍰",
                  "Happy Reddit birthday /u/{}!",
                  "Hope you have a nice cake day /u/{}! 🎂",
                  "It's your cake day /u/{}! Congrats! 🎉"]


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit("Birth-Day-Bot", user_agent="Birthday Bot v1.0")
    return reddit


def main():
    reddit = authenticate()
    congratulated_users = get_congratulated_users()

    remove_downvoted_comments(reddit)
    run_bot(reddit, congratulated_users)


def run_bot(reddit, congratulated_users):
    current_date = datetime.datetime.today().strftime('%y/%m/%d')

    print("Getting comments...")
    for comment in reddit.subreddit("RandomKindness+happy").comments(limit=300):

        account_created_date = datetime.datetime.fromtimestamp(int(comment.author.created)).strftime('%y/%m/%d')

        print("Checking...")
        if current_date != account_created_date \
                and current_date[3:] == account_created_date[3:] \
                and comment.author not in congratulated_users:
            print("Cake day found!")
            comment.reply(random.choice(REPLY_MESSAGES).format(comment.author)).clear_vote()

            congratulated_users.append(comment.author)
            with open("congratulated_users.txt", "a") as file:
                file.write("{}\n".format(comment.author.name))


def get_congratulated_users():
    with open("congratulated_users.txt", "r") as file:
        return file.read().split("\n")


def remove_downvoted_comments(reddit):
    print("Checking for comments with negative karma...")

    for comment in reddit.redditor("Birth-Day-Bot").comments.new(limit=20):
        print("Comment Score: {}".format(comment.score))
        if comment.score <= 0:
            print("Deleting comment...")
            comment.delete()


if __name__ == "__main__":
    main()
